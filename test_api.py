#!/usr/bin/env python3
"""
Simple mock API server for testing the frontend
"""

import json
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer


class MockAPIHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header(
            "Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS"
        )
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def send_json_response(self, data, status_code=200):
        """Send a JSON response with CORS headers"""
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())

    def do_GET(self):
        """Handle GET requests"""
        path = urllib.parse.urlparse(self.path).path

        if path == "/health":
            self.send_json_response(
                {
                    "status": "healthy",
                    "version": "0.1.0",
                    "environment": "development",
                    "timestamp": "2024-08-24T23:10:00Z",
                }
            )
        elif path == "/api/v1/test":
            self.send_json_response({"message": "API is working", "status": "ok"})
        elif path.startswith("/api/v1/iac/providers"):
            self.send_json_response(
                {
                    "providers": [
                        {
                            "name": "proxmox",
                            "display_name": "Proxmox VE",
                            "description": "Proxmox Virtual Environment",
                            "supported_formats": ["terraform", "opentofu"],
                            "cost_tier": "self-hosted",
                        },
                        {
                            "name": "aws",
                            "display_name": "Amazon Web Services",
                            "description": "Amazon Web Services cloud platform",
                            "supported_formats": ["terraform", "opentofu", "cdk"],
                            "cost_tier": "cloud",
                        },
                    ]
                }
            )
        elif path.startswith("/api/v1/"):
            # Generic API response for testing
            self.send_json_response(
                {"message": f"Mock response for {path}", "data": [], "success": True}
            )
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

    def do_POST(self):
        """Handle POST requests"""
        path = urllib.parse.urlparse(self.path).path

        # Read request body
        content_length = int(self.headers.get("Content-Length", 0))
        request_body = (
            self.rfile.read(content_length).decode() if content_length > 0 else "{}"
        )

        try:
            request_data = json.loads(request_body)
        except json.JSONDecodeError:
            request_data = {}

        if path.startswith("/api/v1/requirements/analyze"):
            self.send_json_response(
                {
                    "id": "analysis_123",
                    "analysis": {
                        "infrastructure_components": [
                            {
                                "type": "vm",
                                "name": "web-server",
                                "specifications": {
                                    "cpu": "2",
                                    "memory": "4GB",
                                    "disk": "50GB",
                                },
                            }
                        ],
                        "networking_requirements": [],
                        "security_requirements": [],
                        "storage_requirements": [],
                        "compute_requirements": [],
                        "monitoring_requirements": [],
                    },
                    "confidence_score": 0.85,
                    "processing_time": 2.3,
                    "suggestions": [
                        "Consider adding a load balancer for high availability"
                    ],
                }
            )
        elif path.startswith("/api/v1/iac/generate"):
            project_name = request_data.get("project_name", "example")
            requirements = request_data.get("requirements", "Not specified")
            infrastructure_code = f"""# Generated Infrastructure Code
# Requirements: {requirements}

resource "proxmox_vm_qemu" "example" {{
  name = "{project_name}"
  target_node = "pve"
  memory = 2048
  cores = 2
}}"""

            self.send_json_response(
                {
                    "success": True,
                    "infrastructure_code": infrastructure_code,
                    "validation_results": [
                        {
                            "valid": True,
                            "error_count": 0,
                            "warning_count": 1,
                            "issues": [
                                {
                                    "type": "warning",
                                    "message": "Consider adding resource tags",
                                    "line": 5,
                                    "rule": "tagging_policy",
                                }
                            ],
                        }
                    ],
                    "cost_estimate": {
                        "total_monthly_cost": 45.67,
                        "breakdown": [
                            {
                                "resource_type": "VM",
                                "resource_name": "web-server",
                                "monthly_cost": 45.67,
                            }
                        ],
                        "currency": "USD",
                        "confidence": 0.8,
                    },
                    "processing_time": 3.2,
                }
            )
        else:
            # Generic POST response
            self.send_json_response(
                {
                    "message": f"Mock POST response for {path}",
                    "received_data": request_data,
                    "success": True,
                }
            )

    def log_message(self, format, *args):
        """Override to reduce logging noise"""
        print(f"[{self.address_string()}] {format % args}")


if __name__ == "__main__":
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, MockAPIHandler)
    print("Mock API server running on http://localhost:8000")
    print("Available endpoints:")
    print("  GET  /health")
    print("  GET  /api/v1/test")
    print("  GET  /api/v1/iac/providers")
    print("  POST /api/v1/requirements/analyze")
    print("  POST /api/v1/iac/generate")
    print("\nPress Ctrl+C to stop")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        httpd.shutdown()
