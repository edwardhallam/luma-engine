import { Routes, Route } from 'react-router-dom'
import { Helmet } from 'react-helmet-async'
import Layout from '@/components/Layout'
import Dashboard from '@/pages/Dashboard'
import WorkflowBoard from '@/pages/WorkflowBoard'
import RequirementAnalysis from '@/pages/RequirementAnalysis'
import IaCGeneration from '@/pages/IaCGeneration'
import TemplateManagement from '@/pages/TemplateManagement'
import DeploymentMonitoring from '@/pages/DeploymentMonitoring'
import SecurityCompliance from '@/pages/SecurityCompliance'
import CostOptimization from '@/pages/CostOptimization'

function App() {
  return (
    <>
      <Helmet>
        <title>LumaEngine - AI Infrastructure Orchestration</title>
        <meta name="description" content="Next-generation AI-powered infrastructure orchestration platform for homelabs and SMBs" />
      </Helmet>

      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/workflow" element={<WorkflowBoard />} />
          <Route path="/requirements" element={<RequirementAnalysis />} />
          <Route path="/iac" element={<IaCGeneration />} />
          <Route path="/templates" element={<TemplateManagement />} />
          <Route path="/deployments" element={<DeploymentMonitoring />} />
          <Route path="/security" element={<SecurityCompliance />} />
          <Route path="/costs" element={<CostOptimization />} />
        </Routes>
      </Layout>
    </>
  )
}

export default App
