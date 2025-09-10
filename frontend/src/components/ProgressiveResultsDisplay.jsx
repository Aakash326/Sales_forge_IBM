import React from 'react';
import { 
  Clock, 
  CheckCircle, 
  Target, 
  Brain, 
  Zap, 
  Mail,
  Loader2,
  PlayCircle
} from 'lucide-react';

const ProgressiveResultsDisplay = ({ 
  workflowState, 
  workflowName 
}) => {
  const phases = [
    {
      id: 'tactical',
      name: 'Tactical Intelligence',
      icon: Target,
      description: 'Lead qualification and tactical insights',
      color: 'blue'
    },
    {
      id: 'strategic', 
      name: 'Strategic Intelligence',
      icon: Brain,
      description: 'Business case and strategic analysis',
      color: 'purple'
    },
    {
      id: 'advanced',
      name: 'Advanced Intelligence', 
      icon: Zap,
      description: 'Specialized behavioral and competitive insights',
      color: 'indigo'
    },
    {
      id: 'email',
      name: 'Email Generation',
      icon: Mail,
      description: 'AI-powered personalized outreach',
      color: 'emerald'
    }
  ];

  const getPhaseStatus = (phaseId) => {
    if (workflowState.currentPhase === `${phaseId}_start`) return 'running';
    if (workflowState.completedPhases.includes(`${phaseId}_complete`)) return 'completed';
    if (phases.findIndex(p => p.id === phaseId) < phases.findIndex(p => p.id === workflowState.currentPhase?.replace('_start', '').replace('_complete', ''))) return 'completed';
    return 'pending';
  };

  const PhaseCard = ({ phase, status, data }) => {
    const Icon = phase.icon;
    
    return (
      <div className={`
        bg-white rounded-xl border-2 p-6 transition-all duration-300
        ${status === 'completed' ? `border-${phase.color}-500 bg-${phase.color}-50` : 
          status === 'running' ? `border-${phase.color}-300 bg-${phase.color}-25 shadow-lg` :
          'border-gray-200 bg-gray-50'}
      `}>
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center">
            <div className={`
              p-3 rounded-lg mr-4 transition-colors duration-300
              ${status === 'completed' ? `bg-${phase.color}-500` :
                status === 'running' ? `bg-${phase.color}-400 animate-pulse` :
                'bg-gray-300'}
            `}>
              {status === 'running' ? (
                <Loader2 className="h-6 w-6 text-white animate-spin" />
              ) : (
                <Icon className={`h-6 w-6 ${status === 'completed' ? 'text-white' : 'text-gray-500'}`} />
              )}
            </div>
            <div>
              <h3 className={`text-lg font-semibold transition-colors duration-300 ${
                status === 'completed' ? `text-${phase.color}-800` :
                status === 'running' ? `text-${phase.color}-700` :
                'text-gray-600'
              }`}>
                {phase.name}
              </h3>
              <p className="text-sm text-gray-600">{phase.description}</p>
            </div>
          </div>
          
          <div className="flex items-center">
            {status === 'completed' && (
              <CheckCircle className={`h-6 w-6 text-${phase.color}-500`} />
            )}
            {status === 'running' && (
              <PlayCircle className={`h-6 w-6 text-${phase.color}-500 animate-pulse`} />
            )}
            {status === 'pending' && (
              <Clock className="h-6 w-6 text-gray-400" />
            )}
          </div>
        </div>

        {/* Phase Content */}
        {status === 'running' && (
          <div className="space-y-2">
            <div className={`h-2 bg-${phase.color}-200 rounded-full overflow-hidden`}>
              <div className={`h-full bg-${phase.color}-500 rounded-full animate-pulse transition-all duration-1000`} 
                   style={{width: '70%'}} />
            </div>
            <p className={`text-sm text-${phase.color}-600 animate-pulse`}>
              {workflowState.currentMessage || `Processing ${phase.name.toLowerCase()}...`}
            </p>
          </div>
        )}

        {status === 'completed' && data && (
          <div className="mt-4 space-y-3">
            {phase.id === 'tactical' && (
              <div className="grid grid-cols-2 gap-4">
                <div className={`p-3 bg-${phase.color}-100 rounded-lg`}>
                  <div className={`text-2xl font-bold text-${phase.color}-800`}>
                    {(data.lead_score * 100).toFixed(0)}%
                  </div>
                  <div className={`text-sm text-${phase.color}-600`}>Lead Score</div>
                </div>
                <div className={`p-3 bg-${phase.color}-100 rounded-lg`}>
                  <div className={`text-2xl font-bold text-${phase.color}-800`}>
                    {(data.conversion_probability * 100).toFixed(0)}%
                  </div>
                  <div className={`text-sm text-${phase.color}-600`}>Conversion</div>
                </div>
              </div>
            )}

            {phase.id === 'strategic' && (
              <div className="grid grid-cols-2 gap-4">
                <div className={`p-3 bg-${phase.color}-100 rounded-lg`}>
                  <div className={`text-lg font-bold text-${phase.color}-800`}>
                    ${data.investment_required?.toLocaleString()}
                  </div>
                  <div className={`text-sm text-${phase.color}-600`}>Investment</div>
                </div>
                <div className={`p-3 bg-${phase.color}-100 rounded-lg`}>
                  <div className={`text-lg font-bold text-${phase.color}-800`}>
                    {data.projected_roi}x
                  </div>
                  <div className={`text-sm text-${phase.color}-600`}>ROI</div>
                </div>
              </div>
            )}

            {phase.id === 'advanced' && (
              <div className={`p-3 bg-${phase.color}-100 rounded-lg`}>
                <div className={`text-sm font-medium text-${phase.color}-800`}>
                  Profile: {data.behavioral_profile}
                </div>
                <div className={`text-sm text-${phase.color}-600`}>
                  Success: {(data.predictive_success_probability * 100).toFixed(0)}%
                </div>
              </div>
            )}

            {phase.id === 'email' && (
              <div className={`p-3 bg-${phase.color}-100 rounded-lg`}>
                <div className={`text-sm font-medium text-${phase.color}-800 mb-1`}>
                  📧 {data.subject}
                </div>
                <div className={`text-xs text-${phase.color}-600`}>
                  {data.body?.substring(0, 100)}...
                </div>
              </div>
            )}

            <div className={`text-xs text-${phase.color}-500 flex items-center`}>
              <CheckCircle className="h-3 w-3 mr-1" />
              Completed successfully
            </div>
          </div>
        )}

        {status === 'pending' && (
          <div className="mt-4">
            <div className="text-sm text-gray-500 flex items-center">
              <Clock className="h-4 w-4 mr-2" />
              Waiting to start...
            </div>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">
              Workflow Progress
            </h2>
            <p className="text-gray-600 mt-1">
              {workflowName} • {workflowState.workflowId?.slice(0, 8)}
            </p>
          </div>
          <div className="text-right">
            <div className="text-lg font-semibold text-gray-900">
              {workflowState.completedPhases?.length || 0} / {phases.length}
            </div>
            <div className="text-sm text-gray-500">Phases Complete</div>
          </div>
        </div>

        {/* Overall Progress Bar */}
        <div className="mt-4">
          <div className="flex justify-between text-sm text-gray-600 mb-2">
            <span>Overall Progress</span>
            <span>{Math.round(((workflowState.completedPhases?.length || 0) / phases.length) * 100)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3">
            <div 
              className="bg-gradient-to-r from-blue-500 to-purple-500 h-3 rounded-full transition-all duration-500"
              style={{
                width: `${((workflowState.completedPhases?.length || 0) / phases.length) * 100}%`
              }}
            />
          </div>
        </div>
      </div>

      {/* Phase Cards */}
      <div className="space-y-4">
        {phases.map((phase) => {
          // Skip advanced phase for basic workflow
          if (phase.id === 'advanced' && workflowName?.includes('Basic')) {
            return null;
          }
          
          const status = getPhaseStatus(phase.id);
          const data = workflowState.phaseData?.[`${phase.id}_complete`];
          
          return (
            <PhaseCard
              key={phase.id}
              phase={phase}
              status={status}
              data={data}
            />
          );
        })}
      </div>

      {/* Current Status */}
      <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl border border-blue-200 p-4">
        <div className="flex items-center">
          <div className="w-3 h-3 bg-blue-500 rounded-full mr-3 animate-pulse" />
          <span className="text-sm font-medium text-blue-800">
            {workflowState.currentMessage || 'Processing workflow...'}
          </span>
        </div>
      </div>
    </div>
  );
};

export default ProgressiveResultsDisplay;