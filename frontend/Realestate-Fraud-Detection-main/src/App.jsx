import './App.css'
import Pages from "@/pages/index.jsx"
import { Toaster } from "@/components/ui/toaster"

/**
 * Main App Component
 * 
 * This is the root component of the Real Estate Fraud Detection application.
 * It renders the main pages routing and includes a global toaster for notifications.
 * 
 * @returns {JSX.Element} The main app structure
 */
function App() {
  return (
    <>
      {/* Main application pages and routing */}
      <Pages />
      
      {/* Global notification toaster */}
      <Toaster />
    </>
  )
}

export default App 