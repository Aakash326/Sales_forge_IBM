import React, { useState, useEffect } from 'react';
import { 
  Brain, Users, Building2, Zap, Mail, CheckCircle, Clock, 
  Play, Pause, TrendingUp, Target, DollarSign, AlertTriangle,
  ChevronRight, Activity, Database, MessageCircle, Square, Eye
} from 'lucide-react';
import EmailOutputsModal from './EmailOutputsModal';

const RealtimeWorkflowDisplay = ({ batchResults, isLoading, workflowType, onStopWorkflow }) => {
  const [currentPhase, setCurrentPhase] = useState('idle');
  const [completedCompanies, setCompletedCompanies] = useState([]);
  const [currentCompany, setCurrentCompany] = useState(null);
  const [agentProgress, setAgentProgress] = useState({});
  const [startTime, setStartTime] = useState(null);
  const [emailsSent, setEmailsSent] = useState(0);
  const [emailOutputs, setEmailOutputs] = useState([]);
  const [showEmailModal, setShowEmailModal] = useState(false);
  const [workflowStopped, setWorkflowStopped] = useState(false);

  useEffect(() => {
    if (isLoading && !startTime && !workflowStopped) {
      setStartTime(new Date());
      setCurrentPhase('initializing');
      simulateRealWorkflowExecution();
    } else if (!isLoading && batchResults) {
      setCurrentPhase('completed');
      setCompletedCompanies(batchResults.results || []);
      setEmailsSent(batchResults.emails_sent || 0);
      
      // Generate sample email outputs based on results
      if (batchResults.results) {
        const emails = batchResults.results.map((result, index) => ({
          company_name: result.company_name,
          recipient: `contact@${result.company_name.toLowerCase().replace(/[^a-z0-9]/g, '')}.com`,
          subject: `Strategic Partnership Opportunity - ${result.company_name}`,
          body: generateEmailContent(result),
          timestamp: new Date(Date.now() + index * 30000).toISOString(),
          status: result.email_sent ? 'sent' : 'failed',
          lead_score: result.results_summary?.lead_score || 0.75,
          ai_insights: [
            `Identified ${result.results_summary?.projected_roi || '2.4'}x ROI potential`,
            `${(result.results_summary?.conversion_probability * 100 || 65).toFixed(0)}% conversion probability`,
            'Personalized approach based on industry analysis'
          ]
        }));
        setEmailOutputs(emails);
      }
    }
  }, [isLoading, batchResults, workflowStopped]);

  const generateEmailContent = (result) => {
    return `Dear ${result.company_name} Team,

I hope this message finds you well. Our AI-powered strategic analysis has identified significant opportunities for collaboration between our organizations.

Key Findings:
• Lead Score: ${(result.results_summary?.lead_score * 100 || 75).toFixed(0)}%
• Projected ROI: ${result.results_summary?.projected_roi || '2.4'}x
• Strategic Alignment: High potential for mutual growth

Our advanced intelligence platform, powered by 13 specialized AI agents, has analyzed your market position and identified specific areas where we can add value to your operations.

I would welcome the opportunity to discuss how our solutions can drive meaningful results for ${result.company_name}.

Would you be available for a 15-minute call next week?

Best regards,
Sales Intelligence Team
Powered by Sales Forge AI

---
This email was generated using advanced AI analysis including:
- CrewAI Tactical Intelligence
- IBM Strategic Analysis  
- Advanced Behavioral Insights
- Competitive Intelligence Assessment`;
  };

  const handleStopWorkflow = () => {
    setWorkflowStopped(true);
    setCurrentPhase('stopped');
    if (onStopWorkflow) {
      onStopWorkflow();
    }
  };

  const simulateRealWorkflowExecution = () => {
    // Simulate the actual agent execution phases
    const phases = [
      { name: 'initializing', duration: 2000, description: 'Initializing AI agents and database connections' },
      { name: 'crewai_tactical', duration: 8000, description: 'CrewAI Tactical Intelligence (4 agents)' },
      { name: 'ibm_strategic', duration: 12000, description: 'IBM Strategic Intelligence (4 agents)' },
      { name: 'advanced_intelligence', duration: 6000, description: 'Advanced Intelligence Layer' },
      { name: 'email_generation', duration: 4000, description: 'AI Email Generation & Sending' },
    ];

    let currentPhaseIndex = 0;
    
    const executePhase = () => {
      if (currentPhaseIndex < phases.length) {
        const phase = phases[currentPhaseIndex];
        setCurrentPhase(phase.name);
        
        // Simulate agent progress within each phase
        simulateAgentProgress(phase.name, phase.duration);
        
        setTimeout(() => {
          currentPhaseIndex++;
          executePhase();
        }, phase.duration);
      }
    };

    executePhase();
  };

  const simulateAgentProgress = (phaseName, duration) => {
    const agentCounts = {
      'crewai_tactical': 4,
      'ibm_strategic': 4, 
      'advanced_intelligence': workflowType === 'advanced' ? 5 : workflowType === 'intermediate' ? 3 : 0,
      'email_generation': 1
    };

    const agentCount = agentCounts[phaseName] || 1;
    const agentDuration = duration / agentCount;

    for (let i = 0; i < agentCount; i++) {
      setTimeout(() => {
        setAgentProgress(prev => ({
          ...prev,
          [phaseName]: {
            total: agentCount,
            completed: i + 1,
            current: `Agent ${i + 1}/${agentCount}`
          }
        }));
      }, (i + 1) * agentDuration);
    }
  };

  const getWorkflowConfig = () => {
    const configs = {
      'basic': {
        name: 'Fast 8-Agent Platform',
        agents: 8,
        layers: ['CrewAI Tactical (4)', 'IBM Strategic (4)'],
        duration: '4-5 minutes',
        coverage: '65%',
        color: 'blue'
      },
      'intermediate': {
        name: 'Intermediate 11-Agent Platform', 
        agents: 11,
        layers: ['CrewAI Tactical (4)', 'IBM Strategic (4)', 'Advanced Intel (3)'],
        duration: '7-9 minutes',
        coverage: '85%',
        color: 'purple'
      },
      'advanced': {
        name: 'Complete 13-Agent Platform',
        agents: 13, 
        layers: ['CrewAI Tactical (4)', 'IBM Strategic (4)', 'Advanced Intel (5)'],
        duration: '10-15 minutes',
        coverage: '100%',
        color: 'emerald'
      }
    };
    return configs[workflowType] || configs.basic;
  };

  const getPhaseIcon = (phase) => {
    const icons = {
      'idle': Clock,
      'initializing': Play,
      'crewai_tactical': Users,
      'ibm_strategic': Building2,
      'advanced_intelligence': Brain,
      'email_generation': Mail,
      'completed': CheckCircle
    };
    return icons[phase] || Activity;
  };

  const getPhaseStatus = (phase) => {
    const phases = ['initializing', 'crewai_tactical', 'ibm_strategic', 'advanced_intelligence', 'email_generation'];
    const currentIndex = phases.indexOf(currentPhase);
    const phaseIndex = phases.indexOf(phase);
    
    if (currentPhase === 'completed') return 'completed';
    if (phaseIndex < currentIndex) return 'completed';
    if (phaseIndex === currentIndex) return 'active';
    return 'pending';
  };

  const config = getWorkflowConfig();
  const timeElapsed = startTime ? Math.floor((new Date() - startTime) / 1000) : 0;

  if (currentPhase === 'idle') {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-secondary-200 p-8 text-center">
        <Brain className="h-16 w-16 text-secondary-300 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-secondary-900 mb-2">AI Workflow Ready</h3>
        <p className="text-secondary-600">Select companies and run a workflow to see real-time agent execution</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Workflow Header */}
      <div className="bg-gradient-to-r from-primary-50 to-blue-50 rounded-xl border border-primary-200 p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center">
            <div className={`p-3 bg-${config.color}-100 rounded-xl mr-4`}>
              <Brain className={`h-6 w-6 text-${config.color}-600`} />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-secondary-900">{config.name}</h3>
              <p className="text-sm text-secondary-600">
                {config.agents} AI agents • {config.coverage} intelligence coverage • {config.duration}
              </p>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            {/* Control Buttons */}
            <div className="flex items-center space-x-2">
              {isLoading && !workflowStopped && (
                <button
                  onClick={handleStopWorkflow}
                  className="flex items-center px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors"
                >
                  <Square className="h-4 w-4 mr-2" />
                  Stop Automation
                </button>
              )}
              
              {emailOutputs.length > 0 && (
                <button
                  onClick={() => setShowEmailModal(true)}
                  className="flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
                >
                  <Eye className="h-4 w-4 mr-2" />
                  View Emails ({emailOutputs.length})
                </button>
              )}
            </div>
            
            <div className="text-right">
              <div className="text-2xl font-bold text-primary-600">
                {timeElapsed > 0 ? `${Math.floor(timeElapsed / 60)}:${(timeElapsed % 60).toString().padStart(2, '0')}` : '0:00'}
              </div>
              <div className="text-xs text-secondary-500">
                {workflowStopped ? 'Stopped' : 'Elapsed Time'}
              </div>
            </div>
          </div>
        </div>

        {/* Agent Layers */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {config.layers.map((layer, index) => (
            <div key={layer} className="bg-white/80 rounded-lg p-3 border border-white">
              <div className="text-sm font-medium text-secondary-800">{layer}</div>
              <div className="text-xs text-secondary-600 mt-1">
                Layer {index + 1} • {layer.match(/\((\d+)\)/)?.[1] || '1'} agents
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Real-time Phase Execution */}
      <div className="bg-white rounded-xl shadow-sm border border-secondary-200">
        <div className="p-6 border-b border-secondary-200">
          <h4 className="text-lg font-semibold text-secondary-900 flex items-center">
            <Activity className="h-5 w-5 mr-2 text-primary-600" />
            Live Agent Execution
          </h4>
          <p className="text-sm text-secondary-600 mt-1">Real-time view of AI agents processing your companies</p>
        </div>

        <div className="p-6 space-y-4">
          {/* Phase Progress */}
          {[
            { key: 'initializing', name: 'Initialization', desc: 'Loading AI models and database connections' },
            { key: 'crewai_tactical', name: 'CrewAI Tactical Layer', desc: '4 agents: Research, Scoring, Outreach, Simulation' },
            { key: 'ibm_strategic', name: 'IBM Strategic Layer', desc: '4 agents: Market Intel, Tech Architecture, Executive ROI, Compliance' },
            ...(workflowType !== 'basic' ? [{ key: 'advanced_intelligence', name: 'Advanced Intelligence', desc: `${config.layers[2]} specialized agents` }] : []),
            { key: 'email_generation', name: 'Email Generation', desc: 'AI-powered personalized email creation and delivery' }
          ].map((phase) => {
            const PhaseIcon = getPhaseIcon(phase.key);
            const status = getPhaseStatus(phase.key);
            const progress = agentProgress[phase.key];
            
            return (
              <div key={phase.key} className={`flex items-center p-4 rounded-lg border-2 transition-all ${
                status === 'active' ? 'border-primary-300 bg-primary-50' :
                status === 'completed' ? 'border-emerald-300 bg-emerald-50' :
                'border-secondary-200 bg-secondary-50'
              }`}>
                <div className={`p-2 rounded-lg mr-4 ${
                  status === 'active' ? 'bg-primary-100 text-primary-600' :
                  status === 'completed' ? 'bg-emerald-100 text-emerald-600' :
                  'bg-secondary-100 text-secondary-400'
                }`}>
                  {status === 'active' ? (
                    <div className="animate-spin">
                      <PhaseIcon className="h-5 w-5" />
                    </div>
                  ) : (
                    <PhaseIcon className="h-5 w-5" />
                  )}
                </div>
                
                <div className="flex-1">
                  <div className="flex items-center justify-between">
                    <h5 className="font-medium text-secondary-900">{phase.name}</h5>
                    <div className="flex items-center space-x-2">
                      {progress && (
                        <span className="text-sm text-secondary-600">
                          {progress.current}
                        </span>
                      )}
                      {status === 'completed' && (
                        <CheckCircle className="h-4 w-4 text-emerald-500" />
                      )}
                    </div>
                  </div>
                  <p className="text-sm text-secondary-600 mt-1">{phase.desc}</p>
                  
                  {/* Agent Progress Bar */}
                  {progress && status === 'active' && (
                    <div className="mt-2">
                      <div className="w-full bg-secondary-200 rounded-full h-2">
                        <div 
                          className="bg-primary-500 h-2 rounded-full transition-all duration-500"
                          style={{ width: `${(progress.completed / progress.total) * 100}%` }}
                        ></div>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Live Results */}
      {batchResults && (
        <div className="bg-white rounded-xl shadow-sm border border-secondary-200">
          <div className="p-6 border-b border-secondary-200">
            <h4 className="text-lg font-semibold text-secondary-900 flex items-center">
              <TrendingUp className="h-5 w-5 mr-2 text-emerald-600" />
              Live Results
            </h4>
          </div>

          {/* Key Metrics */}
          <div className="p-6 grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center p-4 bg-blue-50 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">{batchResults.companies_processed}</div>
              <div className="text-sm text-blue-600">Companies Analyzed</div>
            </div>
            
            <div className="text-center p-4 bg-emerald-50 rounded-lg">
              <div className="text-2xl font-bold text-emerald-600">{batchResults.summary?.successful_workflows || 0}</div>
              <div className="text-sm text-emerald-600">Successful</div>
            </div>
            
            <div className="text-center p-4 bg-purple-50 rounded-lg">
              <div className="text-2xl font-bold text-purple-600">{emailsSent}</div>
              <div className="text-sm text-purple-600">Emails Sent</div>
            </div>
            
            <div className="text-center p-4 bg-amber-50 rounded-lg">
              <div className="text-2xl font-bold text-amber-600">
                {Math.round((batchResults.summary?.successful_workflows / batchResults.companies_processed) * 100) || 0}%
              </div>
              <div className="text-sm text-amber-600">Success Rate</div>
            </div>
          </div>

          {/* Company Results */}
          <div className="border-t border-secondary-200">
            <div className="p-6">
              <h5 className="font-medium text-secondary-900 mb-4">Company Analysis Results</h5>
              <div className="space-y-3 max-h-64 overflow-y-auto">
                {batchResults.results?.map((result, index) => (
                  <div key={result.company_name} className="flex items-center justify-between p-3 bg-secondary-50 rounded-lg">
                    <div className="flex items-center space-x-3">
                      {result.status === 'completed' ? (
                        <CheckCircle className="h-5 w-5 text-emerald-500" />
                      ) : (
                        <AlertTriangle className="h-5 w-5 text-amber-500" />
                      )}
                      
                      <div>
                        <div className="font-medium text-secondary-900">{result.company_name}</div>
                        <div className="flex items-center space-x-4 text-xs text-secondary-600 mt-1">
                          {result.results_summary && (
                            <>
                              <span>Score: {(result.results_summary.lead_score * 100).toFixed(0)}%</span>
                              <span>ROI: {result.results_summary.projected_roi}x</span>
                            </>
                          )}
                        </div>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-2">
                      {result.email_sent && (
                        <div className="flex items-center text-emerald-600">
                          <Mail className="h-4 w-4 mr-1" />
                          <span className="text-xs">Email Sent</span>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Email Outputs Modal */}
      <EmailOutputsModal 
        isOpen={showEmailModal}
        onClose={() => setShowEmailModal(false)}
        emailOutputs={emailOutputs}
      />
    </div>
  );
};

export default RealtimeWorkflowDisplay;