"""Security scanning and audit API endpoints."""

import asyncio
import json
import logging
import subprocess  # nosec B404 - Required for security scanning tools
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Union

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

logger = logging.getLogger(__name__)
router = APIRouter()


class SecurityStatus(BaseModel):
    """Security status response model."""

    scan_tools_available: Dict[str, bool]
    last_scan_timestamp: Optional[datetime]
    baseline_exists: bool
    pre_commit_configured: bool
    security_reports_count: int


class SecurityScanRequest(BaseModel):
    """Security scan request model."""

    scan_type: str = "all"  # "secrets", "dependencies", "code", "all"
    target_path: Optional[str] = None
    update_baseline: bool = False


class SecurityScanResult(BaseModel):
    """Security scan result model."""

    scan_type: str
    timestamp: datetime
    status: str  # "success", "warning", "error"
    findings_count: int
    findings: List[Dict]
    recommendations: List[str]


class SecurityAuditResponse(BaseModel):
    """Security audit response model."""

    timestamp: datetime
    overall_status: str  # "secure", "warning", "critical"
    scan_results: List[SecurityScanResult]
    summary: Dict[str, Union[int, str]]
    next_actions: List[str]


def check_tool_availability() -> Dict[str, bool]:
    """Check if security tools are available."""
    tools = {
        "detect-secrets": False,
        "bandit": False,
        "safety": False,
        "pre-commit": False,
    }

    for tool in tools.keys():
        try:
            result = subprocess.run(
                [tool, "--help"], capture_output=True, timeout=10
            )  # nosec B603
            tools[tool] = result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            tools[tool] = False

    return tools


def run_secrets_scan(
    target_path: str = ".", update_baseline: bool = False
) -> SecurityScanResult:
    """Run detect-secrets scan."""
    try:
        baseline_path = Path(".secrets.baseline")
        cmd = ["detect-secrets", "scan"]

        if baseline_path.exists() and not update_baseline:
            cmd.extend(["--baseline", str(baseline_path)])

        cmd.extend(["--all-files", target_path])

        if update_baseline and baseline_path.exists():
            cmd.extend(["--update", str(baseline_path)])

        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=60
        )  # nosec B603

        if result.returncode == 0:
            # Parse output for findings
            findings = []
            if result.stdout:
                try:
                    output_data = json.loads(result.stdout)
                    if "results" in output_data:
                        findings = [
                            {"file": filename, "secrets": list(secrets.keys())}
                            for filename, secrets in output_data["results"].items()
                        ]
                except json.JSONDecodeError:
                    findings = []

            return SecurityScanResult(
                scan_type="secrets",
                timestamp=datetime.utcnow(),
                status="success",
                findings_count=len(findings),
                findings=findings,
                recommendations=(
                    ["Review and audit identified potential secrets"]
                    if findings
                    else []
                ),
            )
        else:
            return SecurityScanResult(
                scan_type="secrets",
                timestamp=datetime.utcnow(),
                status="error",
                findings_count=0,
                findings=[],
                recommendations=[f"Fix detect-secrets scan error: {result.stderr}"],
            )

    except subprocess.TimeoutExpired:
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="Secrets scan timed out"
        )
    except Exception as e:
        logger.error(f"Error running secrets scan: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to run secrets scan: {str(e)}",
        )


def run_bandit_scan(target_paths: List[str] = ["backend", "cli"]) -> SecurityScanResult:
    """Run bandit security scan."""
    try:
        cmd = ["bandit", "-r"] + target_paths + ["-f", "json"]
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=120
        )  # nosec B603

        findings = []
        if result.stdout:
            try:
                output_data = json.loads(result.stdout)
                findings = output_data.get("results", [])
            except json.JSONDecodeError:
                findings = []

        status_level = "success"
        if result.returncode != 0:
            status_level = "warning" if findings else "error"

        recommendations = []
        if findings:
            recommendations.append("Review and fix identified security issues")
            recommendations.append("Consider using bandit-baseline to manage findings")

        return SecurityScanResult(
            scan_type="code",
            timestamp=datetime.utcnow(),
            status=status_level,
            findings_count=len(findings),
            findings=findings[:10],  # Limit to first 10 findings
            recommendations=recommendations,
        )

    except subprocess.TimeoutExpired:
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="Bandit scan timed out"
        )
    except Exception as e:
        logger.error(f"Error running bandit scan: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to run bandit scan: {str(e)}",
        )


def run_safety_scan() -> SecurityScanResult:
    """Run safety dependency vulnerability scan."""
    try:
        cmd = ["safety", "scan", "--json"]
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=60
        )  # nosec B603

        findings = []
        if result.stdout:
            try:
                # safety scan outputs different format - parse accordingly
                lines = result.stdout.strip().split("\n")
                for line in lines:
                    if line.strip() and not line.startswith("[") and "::" in line:
                        findings.append({"vulnerability": line.strip()})
            except Exception:
                findings = []

        return SecurityScanResult(
            scan_type="dependencies",
            timestamp=datetime.utcnow(),
            status="success" if result.returncode == 0 else "warning",
            findings_count=len(findings),
            findings=findings,
            recommendations=["Update vulnerable packages"] if findings else [],
        )

    except subprocess.TimeoutExpired:
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="Safety scan timed out"
        )
    except Exception as e:
        logger.error(f"Error running safety scan: {e}")
        # Don't fail completely for safety issues
        return SecurityScanResult(
            scan_type="dependencies",
            timestamp=datetime.utcnow(),
            status="error",
            findings_count=0,
            findings=[],
            recommendations=[f"Failed to run safety scan: {str(e)}"],
        )


@router.get("/status", response_model=SecurityStatus)
async def get_security_status() -> SecurityStatus:
    """Get current security scanning status and configuration."""
    tools_available = check_tool_availability()

    # Check if baseline exists
    baseline_exists = Path(".secrets.baseline").exists()

    # Check if pre-commit is configured
    precommit_configured = Path(".pre-commit-config.yaml").exists()

    # Count security reports
    report_files = ["bandit-report.json", "safety-report.json", ".secrets.baseline"]
    reports_count = sum(1 for f in report_files if Path(f).exists())

    # Try to get last scan timestamp from baseline
    last_scan = None
    if baseline_exists:
        try:
            with open(".secrets.baseline") as f:
                baseline_data = json.load(f)
                if "generated_at" in baseline_data:
                    last_scan = datetime.fromisoformat(baseline_data["generated_at"])
        except Exception:  # nosec B110 - Safe to ignore baseline parse errors
            pass

    return SecurityStatus(
        scan_tools_available=tools_available,
        last_scan_timestamp=last_scan,
        baseline_exists=baseline_exists,
        pre_commit_configured=precommit_configured,
        security_reports_count=reports_count,
    )


@router.post("/scan", response_model=SecurityScanResult)
async def run_security_scan(request: SecurityScanRequest) -> SecurityScanResult:
    """Run security scan based on specified type."""
    target_path = request.target_path or "."

    if request.scan_type == "secrets":
        return run_secrets_scan(target_path, request.update_baseline)
    elif request.scan_type == "code":
        return run_bandit_scan(
            ["backend", "cli"] if target_path == "." else [target_path]
        )
    elif request.scan_type == "dependencies":
        return run_safety_scan()
    elif request.scan_type == "all":
        # Run all scans concurrently
        tasks = [
            asyncio.create_task(
                asyncio.to_thread(
                    run_secrets_scan, target_path, request.update_baseline
                )
            ),
            asyncio.create_task(asyncio.to_thread(run_bandit_scan, ["backend", "cli"])),
            asyncio.create_task(asyncio.to_thread(run_safety_scan)),
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Return combined results (for now, return first successful scan)
        for result in results:
            if isinstance(result, SecurityScanResult):
                return result

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="All security scans failed",
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid scan type: {request.scan_type}. Must be one of: secrets, code, dependencies, all",
        )


@router.get("/audit", response_model=SecurityAuditResponse)
async def get_security_audit() -> SecurityAuditResponse:
    """Get comprehensive security audit report."""
    # Run all scans
    scan_tasks = [
        asyncio.create_task(asyncio.to_thread(run_secrets_scan)),
        asyncio.create_task(asyncio.to_thread(run_bandit_scan, ["backend", "cli"])),
        asyncio.create_task(asyncio.to_thread(run_safety_scan)),
    ]

    results = await asyncio.gather(*scan_tasks, return_exceptions=True)

    scan_results = []
    total_findings = 0
    critical_issues = 0

    for result in results:
        if isinstance(result, SecurityScanResult):
            scan_results.append(result)
            total_findings += result.findings_count
            if result.status == "error":
                critical_issues += 1
        else:
            logger.error(f"Security scan failed: {result}")

    # Determine overall status
    overall_status = "secure"
    if critical_issues > 0:
        overall_status = "critical"
    elif total_findings > 0:
        overall_status = "warning"

    # Generate next actions
    next_actions = []
    if total_findings > 0:
        next_actions.append("Review and remediate identified security findings")
    if not Path(".pre-commit-config.yaml").exists():
        next_actions.append("Install and configure pre-commit hooks")
    if not Path(".secrets.baseline").exists():
        next_actions.append("Create secrets baseline with detect-secrets")

    if not next_actions:
        next_actions.append("Continue regular security monitoring")

    return SecurityAuditResponse(
        timestamp=datetime.utcnow(),
        overall_status=overall_status,
        scan_results=scan_results,
        summary={
            "total_scans": len(scan_results),
            "total_findings": total_findings,
            "critical_issues": critical_issues,
            "status": overall_status,
        },
        next_actions=next_actions,
    )
