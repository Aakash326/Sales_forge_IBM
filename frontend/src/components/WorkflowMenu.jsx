import React from 'react';
import { Zap, Target, Rocket, Bot } from 'lucide-react';

const WorkflowMenu = ({ activeWorkflow, onWorkflowChange, isLoading }) => {
  const workflows = [
    {
      id: 'advanced',
      name: 'Advanced',
      agents: 13,
      duration: '10-15 min',
      icon: Rocket,
      description: 'Complete strategic intelligence with all advanced capabilities',
      color: 'from-purple-500 to-indigo-600'
    },
    {
      id: 'intermediate', 
      name: 'Intermediate',
      agents: 11,
      duration: '7-9 min',
      icon: Target,
      description: 'Balanced intelligence with priority advanced features',
      color: 'from-blue-500 to-cyan-600'
    },
    {
      id: 'basic',
      name: 'Basic',
      agents: 8,
      duration: '4-5 min',
      icon: Zap,
      description: 'Fast core strategic intelligence for high-volume processing',
      color: 'from-emerald-500 to-teal-600'
    },
    {
      id: 'enhanced',
      name: 'Enhanced', 
      agents: 'Variable',
      duration: '3-5 min + user',
      icon: Bot,
      description: 'User-controlled workflow with email approval mechanism',
      color: 'from-orange-500 to-red-600'
    }
  ];

  return (
    <div className="bg-gradient-to-r from-secondary-50 to-white border-b border-secondary-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="mb-4">
          <h2 className="text-lg font-semibold text-secondary-900">
            Choose Your Workflow
          </h2>
          <p className="text-sm text-secondary-600 mt-1">
            Select an AI workflow to analyze your lead with different levels of intelligence depth
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {workflows.map((workflow) => {
            const Icon = workflow.icon;
            const isActive = activeWorkflow === workflow.id;
            
            return (
              <button
                key={workflow.id}
                onClick={() => onWorkflowChange(workflow.id)}
                disabled={isLoading}
                className={`
                  relative overflow-hidden rounded-xl border-2 transition-all duration-200 p-5 text-left
                  ${isActive 
                    ? 'border-primary-500 bg-primary-50 shadow-lg scale-105 ring-2 ring-primary-200' 
                    : 'border-secondary-200 bg-white hover:border-primary-300 hover:shadow-md hover:-translate-y-1'
                  }
                  ${isLoading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
                `}
              >
                {/* Background gradient */}
                <div className={`absolute inset-0 bg-gradient-to-br ${workflow.color} opacity-5`} />
                
                {/* Content */}
                <div className="relative">
                  {/* Header */}
                  <div className="flex items-center justify-between mb-3">
                    <div className={`
                      p-2 rounded-lg bg-gradient-to-br ${workflow.color}
                    `}>
                      <Icon className="h-5 w-5 text-white" />
                    </div>
                    <div className="text-right">
                      <div className="text-xs font-medium text-secondary-500">Agents</div>
                      <div className="text-lg font-bold text-secondary-900">
                        {workflow.agents}
                      </div>
                    </div>
                  </div>
                  
                  {/* Title */}
                  <h3 className="text-lg font-bold text-secondary-900 mb-1">
                    {workflow.name}
                  </h3>
                  
                  {/* Duration */}
                  <div className="flex items-center mb-3">
                    <div className="text-xs font-medium text-secondary-500 bg-secondary-100 px-2 py-1 rounded-full">
                      ⏱️ {workflow.duration}
                    </div>
                  </div>
                  
                  {/* Description */}
                  <p className="text-sm text-secondary-600 leading-relaxed">
                    {workflow.description}
                  </p>
                  
                  {/* Active indicator */}
                  {isActive && (
                    <div className="absolute top-3 right-3">
                      <div className="w-3 h-3 bg-primary-500 rounded-full animate-pulse" />
                    </div>
                  )}
                </div>
              </button>
            );
          })}
        </div>
        
        {/* Current selection info */}
        {activeWorkflow && (
          <div className="mt-6 p-4 bg-primary-50 rounded-lg border border-primary-200">
            <div className="flex items-center">
              <div className="w-2 h-2 bg-primary-500 rounded-full mr-3" />
              <span className="text-sm font-medium text-primary-800">
                Selected: <span className="font-bold">{workflows.find(w => w.id === activeWorkflow)?.name}</span>
                {' '}workflow with{' '}
                <span className="font-bold">{workflows.find(w => w.id === activeWorkflow)?.agents}</span>
                {' '}agents
              </span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default WorkflowMenu;