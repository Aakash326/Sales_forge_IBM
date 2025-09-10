import React, { useState, useEffect, useRef } from 'react';
import { Brain, Loader2, AlertCircle, CheckCircle } from 'lucide-react';
import TabNavigation from './components/TabNavigation';
import WorkflowMenu from './components/WorkflowMenu';
import LeadForm from './components/LeadForm';
import CompanySelector from './components/CompanySelector';
import ResultsDisplay from './components/ResultsDisplay';
import BatchResultsDisplay from './components/BatchResultsDisplay';
import RealtimeWorkflowDisplay from './components/RealtimeWorkflowDisplay';
import ProgressiveResultsDisplay from './components/ProgressiveResultsDisplay';
import AgentInfo from './components/AgentInfo';
import { apiService } from './services/api';

function App() {
  // State management
  const [activeTab, setActiveTab] = useState('advance-agents');
  const [activeWorkflow, setActiveWorkflow] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [batchResults, setBatchResults] = useState(null);
  const [selectedWorkflowType, setSelectedWorkflowType] = useState('basic');
  const [error, setError] = useState(null);
  const [apiStatus, setApiStatus] = useState('checking');
  const [workflowState, setWorkflowState] = useState(null);
  const [useStreaming, setUseStreaming] = useState(true);
  const [viewMode, setViewMode] = useState('database'); // 'database' or 'manual'
  
  // Ref to store EventSource for cleanup
  const eventSourceRef = useRef(null);

  // Check API health on mount
  useEffect(() => {
    checkApiHealth();
  }, []);

  const checkApiHealth = async () => {
    try {
      await apiService.healthCheck();
      setApiStatus('connected');
    } catch (error) {
      console.error('API health check failed:', error);
      setApiStatus('disconnected');
    }
  };

  const handleTabChange = (tabId) => {
    setActiveTab(tabId);
    // Reset workflow and results when changing tabs
    if (tabId !== 'advance-agents') {
      setActiveWorkflow(null);
      setResults(null);
      setBatchResults(null);
    }
  };

  const handleWorkflowChange = (workflowId) => {
    setActiveWorkflow(workflowId);
    setResults(null);
    setBatchResults(null);
    setError(null);
  };

  // Add workflow tracking for cancellation
  const [currentWorkflowId, setCurrentWorkflowId] = useState(null);
  const heartbeatIntervalRef = useRef(null);

  // Heartbeat mechanism
  const startHeartbeat = (workflowId) => {
    if (heartbeatIntervalRef.current) {
      clearInterval(heartbeatIntervalRef.current);
    }
    
    heartbeatIntervalRef.current = setInterval(async () => {
      try {
        await fetch(`http://localhost:8000/api/heartbeat/${workflowId}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          }
        });
      } catch (error) {
        console.warn('Heartbeat failed:', error);
      }
    }, 30000); // Send heartbeat every 30 seconds
  };

  const stopHeartbeat = () => {
    if (heartbeatIntervalRef.current) {
      clearInterval(heartbeatIntervalRef.current);
      heartbeatIntervalRef.current = null;
    }
  };

  const handleRunBatchWorkflow = async (selectionData) => {
    setIsLoading(true);
    setError(null);
    setResults(null);
    setBatchResults(null);
    setWorkflowState(null);
    setCurrentWorkflowId(null);

    try {
      const response = await fetch('http://localhost:8000/api/run-batch-workflow', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(selectionData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Batch workflow failed');
      }

      const batchResult = await response.json();
      setBatchResults(batchResult);
      setSelectedWorkflowType(selectionData.workflow_type);
      setCurrentWorkflowId(batchResult.batch_id);
      
      // Start heartbeat for this workflow
      startHeartbeat(batchResult.batch_id);
    } catch (error) {
      console.error('Batch workflow failed:', error);
      setError(error.message || 'Batch workflow execution failed');
    } finally {
      setIsLoading(false);
      // Don't clear currentWorkflowId here - let handleStopWorkflow do it
    }
  };

  const handleStopWorkflow = async () => {
    if (currentWorkflowId) {
      try {
        // Stop heartbeat first
        stopHeartbeat();
        
        const response = await fetch(`http://localhost:8000/api/cancel-workflow/${currentWorkflowId}`, {
          method: 'POST',
        });
        
        if (response.ok) {
          setIsLoading(false);
          setError('Workflow stopped by user');
          console.log('Workflow cancelled successfully');
        }
      } catch (error) {
        console.error('Failed to cancel workflow:', error);
        setError('Failed to stop workflow');
      }
      setCurrentWorkflowId(null);
    }
  };

  const handleLeadSubmit = async (leadData) => {
    if (!activeWorkflow) {
      setError('Please select a workflow first');
      return;
    }

    // Cleanup any existing EventSource
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
      eventSourceRef.current = null;
    }

    setIsLoading(true);
    setError(null);
    setResults(null);
    setWorkflowState({
      workflowId: `workflow_${Date.now()}`,
      currentPhase: null,
      completedPhases: [],
      phaseData: {},
      currentMessage: 'Initializing workflow...',
      isComplete: false,
      workflowName: null
    });

    try {
      // Use streaming for supported workflows
      if (useStreaming && ['advanced', 'basic'].includes(activeWorkflow)) {
        const onMessage = (data) => {
          console.log('Received workflow update:', data);
          
          setWorkflowState(prevState => {
            const newState = { ...prevState };
            
            // Update current phase and message
            if (data.phase) {
              newState.currentPhase = data.phase;
            }
            if (data.message) {
              newState.currentMessage = data.message;
            }
            
            // Handle phase completion
            if (data.phase && data.phase.endsWith('_complete')) {
              if (!newState.completedPhases.includes(data.phase)) {
                newState.completedPhases.push(data.phase);
              }
              // Backend sends 'data' field for phase results
              if (data.data) {
                newState.phaseData[data.phase] = data.data;
              }
            }
            
            // Handle workflow completion
            if (data.phase === 'workflow_complete') {
              newState.isComplete = true;
              // Capture the real workflow name from the response
              if (data.workflow_name) {
                newState.workflowName = data.workflow_name;
              }
              setIsLoading(false);
            }
            
            return newState;
          });
        };

        const onError = (error) => {
          console.error('Streaming workflow error:', error);
          setError('Streaming connection failed. Please try again.');
          setIsLoading(false);
        };

        const onComplete = () => {
          console.log('Workflow stream completed');
          setIsLoading(false);
        };

        // Start streaming workflow
        if (activeWorkflow === 'advanced') {
          eventSourceRef.current = await apiService.runAdvancedWorkflowStream(leadData, onMessage, onError, onComplete);
        } else if (activeWorkflow === 'basic') {
          eventSourceRef.current = await apiService.runBasicWorkflowStream(leadData, onMessage, onError, onComplete);
        }
      } else {
        // Fall back to regular API calls for non-streaming workflows
        let result;
        
        switch (activeWorkflow) {
          case 'advanced':
            result = await apiService.runAdvancedWorkflow(leadData);
            break;
          case 'intermediate':
            result = await apiService.runIntermediateWorkflow(leadData);
            break;
          case 'basic':
            result = await apiService.runBasicWorkflow(leadData);
            break;
          case 'enhanced':
            result = await apiService.runEnhancedWorkflow(leadData);
            break;
          default:
            throw new Error('Invalid workflow selected');
        }

        setResults(result);
        setIsLoading(false);
      }
    } catch (error) {
      console.error('Workflow execution failed:', error);
      setError(error.response?.data?.detail || error.message || 'An error occurred');
      setIsLoading(false);
    }
  };

  // Cleanup workflows on unmount and page close
  useEffect(() => {
    const handleBeforeUnload = async (event) => {
      if (currentWorkflowId && isLoading) {
        // Stop heartbeat and cancel the workflow when user closes browser/tab
        stopHeartbeat();
        try {
          await fetch(`http://localhost:8000/api/cancel-workflow/${currentWorkflowId}`, {
            method: 'POST',
            keepalive: true // Ensures request completes even if page is closing
          });
        } catch (error) {
          console.error('Failed to cancel workflow on page close:', error);
        }
      }
    };

    const handleVisibilityChange = async () => {
      if (document.visibilityState === 'hidden' && currentWorkflowId && isLoading) {
        // Stop heartbeat and cancel workflow when tab becomes hidden (user switched tabs or minimized)
        stopHeartbeat();
        try {
          await fetch(`http://localhost:8000/api/cancel-workflow/${currentWorkflowId}`, {
            method: 'POST'
          });
        } catch (error) {
          console.error('Failed to cancel workflow on visibility change:', error);
        }
      }
    };

    // Add event listeners
    window.addEventListener('beforeunload', handleBeforeUnload);
    document.addEventListener('visibilitychange', handleVisibilityChange);

    return () => {
      // Cleanup on component unmount
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
      }
      
      // Stop heartbeat and cancel workflow if still running
      stopHeartbeat();
      if (currentWorkflowId && isLoading) {
        fetch(`http://localhost:8000/api/cancel-workflow/${currentWorkflowId}`, {
          method: 'POST',
          keepalive: true
        }).catch(error => {
          console.error('Failed to cancel workflow on unmount:', error);
        });
      }

      // Remove event listeners
      window.removeEventListener('beforeunload', handleBeforeUnload);
      document.removeEventListener('visibilitychange', handleVisibilityChange);
    };
  }, [currentWorkflowId, isLoading]);

  const getWorkflowName = (workflowId) => {
    const workflowNames = {
      'advanced': 'Advanced 13-Agent Intelligence',
      'intermediate': 'Intermediate 11-Agent Intelligence', 
      'basic': 'Basic 8-Agent Intelligence (Fast)',
      'enhanced': 'Enhanced User-Approved Workflow'
    };
    return workflowNames[workflowId] || workflowId;
  };

  return (
    <div className="min-h-screen bg-secondary-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-secondary-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <div className="p-2 bg-primary-100 rounded-xl mr-3">
                <Brain className="h-8 w-8 text-primary-600" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-secondary-900">Sales Forge</h1>
                <p className="text-sm text-secondary-600">AI-Powered Sales Intelligence Platform</p>
              </div>
            </div>
            
            {/* API Status */}
            <div className="flex items-center space-x-2">
              {apiStatus === 'connected' && (
                <>
                  <CheckCircle className="h-5 w-5 text-emerald-500" />
                  <span className="text-sm text-emerald-700 font-medium">API Connected</span>
                </>
              )}
              {apiStatus === 'disconnected' && (
                <>
                  <AlertCircle className="h-5 w-5 text-red-500" />
                  <span className="text-sm text-red-700 font-medium">API Disconnected</span>
                  <button 
                    onClick={checkApiHealth}
                    className="text-sm text-primary-600 hover:text-primary-700 ml-2"
                  >
                    Retry
                  </button>
                </>
              )}
              {apiStatus === 'checking' && (
                <>
                  <Loader2 className="h-5 w-5 text-secondary-500 animate-spin" />
                  <span className="text-sm text-secondary-600">Connecting...</span>
                </>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Tab Navigation */}
      <TabNavigation activeTab={activeTab} onTabChange={handleTabChange} />

      {/* Workflow Menu and Mode Toggle (only for advance-agents tab) */}
      {activeTab === 'advance-agents' && (
        <div className="bg-white border-b border-secondary-200">
          {/* Mode Toggle */}
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <span className="text-sm font-medium text-secondary-700">Mode:</span>
                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => setViewMode('database')}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                      viewMode === 'database' 
                        ? 'bg-primary-100 text-primary-800 border border-primary-300' 
                        : 'bg-secondary-100 text-secondary-700 hover:bg-secondary-200'
                    }`}
                  >
                    Database Companies (Recommended)
                  </button>
                  <button
                    onClick={() => setViewMode('manual')}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                      viewMode === 'manual' 
                        ? 'bg-primary-100 text-primary-800 border border-primary-300' 
                        : 'bg-secondary-100 text-secondary-700 hover:bg-secondary-200'
                    }`}
                  >
                    Manual Input
                  </button>
                </div>
              </div>
              
              <div className="text-sm text-secondary-600">
                {viewMode === 'database' 
                  ? '🤖 Real AI agents analyze companies from database: CrewAI → IBM Strategic → Advanced Intelligence → Auto-Email'
                  : 'Manual company input for individual AI analysis'
                }
              </div>
            </div>
          </div>
          
          {/* Workflow Menu - only show for manual mode */}
          {viewMode === 'manual' && (
            <WorkflowMenu 
              activeWorkflow={activeWorkflow}
              onWorkflowChange={handleWorkflowChange}
              isLoading={isLoading}
            />
          )}
        </div>
      )}

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'advance-agents' ? (
          <>
            {viewMode === 'database' ? (
              /* Database Mode - Company Selection and Batch Processing */
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Company Selector */}
                <div className="lg:col-span-1">
                  <CompanySelector 
                    onRunBatchWorkflow={handleRunBatchWorkflow}
                    isLoading={isLoading}
                  />
                  
                  {/* Error Display */}
                  {error && (
                    <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
                      <div className="flex items-center">
                        <AlertCircle className="h-5 w-5 text-red-500 mr-2" />
                        <span className="text-sm font-medium text-red-800">Error</span>
                      </div>
                      <p className="text-sm text-red-700 mt-1">{error}</p>
                    </div>
                  )}
                </div>

                {/* Real-time Workflow Display */}
                <div className="lg:col-span-2">
                  <RealtimeWorkflowDisplay 
                    batchResults={batchResults} 
                    isLoading={isLoading}
                    workflowType={selectedWorkflowType}
                    onStopWorkflow={handleStopWorkflow}
                  />
                </div>
              </div>
            ) : (
              /* Manual Mode - Original Lead Form */
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Lead Form */}
                <div className="lg:col-span-1">
                  <LeadForm 
                    onSubmit={handleLeadSubmit}
                    isLoading={isLoading}
                  />
                  
                  {/* Workflow Status */}
                  {activeWorkflow && (
                    <div className="mt-6 p-4 bg-white rounded-lg border border-secondary-200">
                      <h4 className="font-medium text-secondary-900 mb-2">Selected Workflow</h4>
                      <p className="text-sm text-secondary-600">
                        {getWorkflowName(activeWorkflow)}
                      </p>
                      {isLoading && (
                        <div className="mt-3 flex items-center text-sm text-primary-600">
                          <Loader2 className="h-4 w-4 animate-spin mr-2" />
                          Running analysis...
                        </div>
                      )}
                    </div>
                  )}

                  {/* Error Display */}
                  {error && (
                    <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
                      <div className="flex items-center">
                        <AlertCircle className="h-5 w-5 text-red-500 mr-2" />
                        <span className="text-sm font-medium text-red-800">Error</span>
                      </div>
                      <p className="text-sm text-red-700 mt-1">{error}</p>
                    </div>
                  )}
                </div>

                {/* Results */}
                <div className="lg:col-span-2">
                  {workflowState ? (
                    <ProgressiveResultsDisplay 
                      workflowState={workflowState} 
                      workflowName={workflowState.workflowName || getWorkflowName(activeWorkflow)}
                    />
                  ) : results ? (
                    <ResultsDisplay 
                      results={results} 
                      workflowName={getWorkflowName(activeWorkflow)}
                    />
                  ) : (
                    <div className="bg-white rounded-xl shadow-sm border border-secondary-200 p-12 text-center">
                      <Brain className="h-16 w-16 text-secondary-300 mx-auto mb-4" />
                      <h3 className="text-lg font-medium text-secondary-900 mb-2">
                        Ready for Analysis
                      </h3>
                      <p className="text-secondary-600 mb-4">
                        {activeWorkflow 
                          ? `Select a lead and click "Analyze Lead" to run ${getWorkflowName(activeWorkflow)}`
                          : 'Choose a workflow above and enter lead information to get started'
                        }
                      </p>
                      {!activeWorkflow && (
                        <p className="text-sm text-secondary-500">
                          ↑ Select a workflow from the menu above
                        </p>
                      )}
                      
                      {/* Streaming Toggle */}
                      {activeWorkflow && ['advanced', 'basic'].includes(activeWorkflow) && (
                        <div className="mt-6 flex items-center justify-center">
                          <label className="flex items-center text-sm text-secondary-600">
                            <input
                              type="checkbox"
                              checked={useStreaming}
                              onChange={(e) => setUseStreaming(e.target.checked)}
                              className="mr-2 h-4 w-4 text-primary-600 border-secondary-300 rounded focus:ring-primary-500"
                            />
                            Use progressive workflow display
                          </label>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>
            )}
          </>
        ) : (
          /* Show agent information for crew-agents and ibm-agents tabs */
          <AgentInfo activeTab={activeTab} />
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-secondary-200 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <Brain className="h-5 w-5 text-primary-600 mr-2" />
              <span className="text-sm text-secondary-600">
                Sales Forge - Powered by Advanced AI Intelligence
              </span>
            </div>
            <div className="text-sm text-secondary-500">
              FastAPI + React + Tailwind CSS
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;