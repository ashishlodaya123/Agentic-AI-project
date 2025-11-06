import {
  BrowserRouter as Router,
  Routes,
  Route,
  NavLink,
} from "react-router-dom";
import { FaBell, FaUser } from "react-icons/fa";
import { GiMedicalPack } from "react-icons/gi";
import TriageDashboard from "./pages/TriageDashboard";
import Results from "./pages/Results";
import Metrics from "./pages/Metrics";
import Home from "./pages/Home";

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-neutral-background">
        {/* Header */}
        <header className="bg-neutral-surface shadow-sm border-b border-neutral-border">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16 items-center">
              <div className="flex items-center">
                <div className="flex-shrink-0 flex items-center">
                  <div className="bg-primary rounded-lg p-2 mr-3">
                    <GiMedicalPack className="h-6 w-6 text-white" />
                  </div>
                  <h1 className="text-xl font-semibold text-neutral-text">
                    Clinical Decision Assistant
                  </h1>
                </div>
              </div>
              <nav className="hidden md:block">
                <div className="ml-10 flex items-baseline space-x-1">
                  <NavLink
                    to="/"
                    className={({ isActive }) =>
                      isActive
                        ? "text-primary bg-blue-50 px-3 py-2 rounded-md text-sm font-medium transition duration-200"
                        : "text-neutral-text-secondary hover:text-primary px-3 py-2 rounded-md text-sm font-medium transition duration-200"
                    }
                  >
                    Home
                  </NavLink>
                  <NavLink
                    to="/triage"
                    className={({ isActive }) =>
                      isActive
                        ? "text-primary bg-blue-50 px-3 py-2 rounded-md text-sm font-medium transition duration-200"
                        : "text-neutral-text-secondary hover:text-primary px-3 py-2 rounded-md text-sm font-medium transition duration-200"
                    }
                  >
                    Triage
                  </NavLink>
                  <NavLink
                    to="/metrics"
                    className={({ isActive }) =>
                      isActive
                        ? "text-primary bg-blue-50 px-3 py-2 rounded-md text-sm font-medium transition duration-200"
                        : "text-neutral-text-secondary hover:text-primary px-3 py-2 rounded-md text-sm font-medium transition duration-200"
                    }
                  >
                    Metrics
                  </NavLink>
                </div>
              </nav>
              <div className="flex items-center">
                <button className="p-1 rounded-full text-neutral-text-secondary hover:text-primary focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary">
                  <span className="sr-only">View notifications</span>
                  <FaBell className="h-6 w-6" />
                </button>
                <div className="ml-3 relative">
                  <div>
                    <button className="flex text-sm rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary">
                      <span className="sr-only">Open user menu</span>
                      <div className="h-8 w-8 rounded-full bg-primary flex items-center justify-center text-white font-medium">
                        <FaUser />
                      </div>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </header>

        {/* Mobile Navigation */}
        <div className="md:hidden bg-neutral-surface border-b border-neutral-border">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 flex justify-center">
            <NavLink
              to="/"
              className={({ isActive }) =>
                isActive
                  ? "text-primary bg-blue-50 px-3 py-2 rounded-md text-sm font-medium"
                  : "text-neutral-text-secondary hover:text-primary px-3 py-2 rounded-md text-sm font-medium"
              }
            >
              Home
            </NavLink>
            <NavLink
              to="/triage"
              className={({ isActive }) =>
                isActive
                  ? "text-primary bg-blue-50 px-3 py-2 rounded-md text-sm font-medium"
                  : "text-neutral-text-secondary hover:text-primary px-3 py-2 rounded-md text-sm font-medium"
              }
            >
              Triage
            </NavLink>
            <NavLink
              to="/metrics"
              className={({ isActive }) =>
                isActive
                  ? "text-primary bg-blue-50 px-3 py-2 rounded-md text-sm font-medium"
                  : "text-neutral-text-secondary hover:text-primary px-3 py-2 rounded-md text-sm font-medium"
              }
            >
              Metrics
            </NavLink>
          </div>
        </div>

        {/* Main Content */}
        <main>
          <div className="max-w-7xl mx-auto sm:px-6 lg:px-8 py-8">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/triage" element={<TriageDashboard />} />
              <Route path="/results/:taskId" element={<Results />} />
              <Route path="/metrics" element={<Metrics />} />
            </Routes>
          </div>
        </main>

        {/* Footer */}
        <footer className="bg-neutral-surface border-t border-neutral-border mt-12">
          <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
            <p className="text-center text-neutral-text-secondary text-sm">
              © {new Date().getFullYear()} Agentic Clinical Decision Assistant.
              All rights reserved.
            </p>
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;
