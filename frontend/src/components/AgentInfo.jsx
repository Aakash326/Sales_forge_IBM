import React from 'react';
import { Users, Building2, Brain, Target, BarChart3, Mail, Shield, Zap } from 'lucide-react';

const AgentInfo = ({ activeTab }) => {
  const agentCategories = {
    'crew-agents': {
      title: 'Crew Agents (4)',
      description: 'Tactical intelligence and lead processing specialists',
      color: 'blue',
      agents: [
        {
          name: 'Research Agent',
          icon: Target,
          description: 'Comprehensive company and industry research',
          capabilities: ['Company profiling', 'Market analysis', 'Competitive landscape', 'Industry trends']
        },
        {
          name: 'Scoring Agent', 
          icon: BarChart3,
          description: 'Lead qualification and scoring algorithms',
          capabilities: ['Lead scoring', 'Qualification metrics', 'Conversion prediction', 'Priority ranking']
        },
        {
          name: 'Outreach Agent',
          icon: Mail,
          description: 'Personalized outreach strategy development',
          capabilities: ['Email personalization', 'Messaging strategy', 'Channel optimization', 'Content generation']
        },
        {
          name: 'Simulation Agent',
          icon: Zap,
          description: 'Sales conversation and outcome simulation',
          capabilities: ['Conversation simulation', 'Objection handling', 'Success probability', 'Strategy validation']
        }
      ]
    },
    'ibm-agents': {
      title: 'IBM Agents (4)',
      description: 'Strategic business intelligence using IBM Granite AI',
      color: 'purple',
      agents: [
        {
          name: 'Market Intelligence',
          icon: BarChart3,
          description: 'Strategic market analysis and opportunity sizing',
          capabilities: ['Market sizing', 'Growth projections', 'Competitive analysis', 'Trend forecasting']
        },
        {
          name: 'Technical Architecture',
          icon: Building2,
          description: 'Solution architecture and implementation planning',
          capabilities: ['Technical feasibility', 'Architecture design', 'Integration planning', 'Timeline estimation']
        },
        {
          name: 'Executive Decision',
          icon: Brain,
          description: 'C-level decision support and ROI modeling',
          capabilities: ['ROI modeling', 'Investment analysis', 'Business case', 'Executive recommendations']
        },
        {
          name: 'Compliance & Risk',
          icon: Shield,
          description: 'Regulatory compliance and risk assessment',
          capabilities: ['Risk assessment', 'Compliance audit', 'Regulatory mapping', 'Mitigation strategies']
        }
      ]
    },
    'advance-agents': {
      title: 'Advanced Intelligence (5)',
      description: 'Specialized advanced intelligence capabilities',
      color: 'emerald',
      agents: [
        {
          name: 'Behavioral Psychology',
          icon: Brain,
          description: 'Decision-maker behavioral analysis and profiling',
          capabilities: ['Psychological profiling', 'Communication preferences', 'Decision patterns', 'Influence mapping']
        },
        {
          name: 'Competitive Intelligence',
          icon: Target,
          description: 'Advanced competitive landscape analysis',
          capabilities: ['Competitor tracking', 'Threat assessment', 'Positioning strategy', 'Market differentiation']
        },
        {
          name: 'Economic Analysis',
          icon: BarChart3,
          description: 'Economic climate and market condition analysis',
          capabilities: ['Economic indicators', 'Market timing', 'Budget cycles', 'Industry health']
        },
        {
          name: 'Predictive Forecasting',
          icon: Zap,
          description: 'Advanced predictive modeling and timeline forecasting',
          capabilities: ['Success prediction', 'Timeline forecasting', 'Outcome modeling', 'Scenario planning']
        },
        {
          name: 'Document Intelligence',
          icon: Building2,
          description: 'Advanced document analysis and insight extraction',
          capabilities: ['Document parsing', 'Insight extraction', 'Knowledge synthesis', 'Information correlation']
        }
      ]
    }
  };

  const category = agentCategories[activeTab];
  
  if (!category) return null;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="text-center mb-8">
        <h2 className={`text-3xl font-bold text-${category.color}-600 mb-2`}>
          {category.title}
        </h2>
        <p className="text-lg text-secondary-600 max-w-3xl mx-auto">
          {category.description}
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {category.agents.map((agent, index) => {
          const Icon = agent.icon;
          return (
            <div 
              key={index}
              className={`
                bg-white rounded-xl border-2 border-${category.color}-200 p-6 
                hover:border-${category.color}-300 hover:shadow-lg transition-all duration-200
                group
              `}
            >
              <div className="flex items-start">
                <div className={`
                  p-3 bg-${category.color}-100 rounded-xl mr-4 
                  group-hover:bg-${category.color}-200 transition-colors duration-200
                `}>
                  <Icon className={`h-8 w-8 text-${category.color}-600`} />
                </div>
                
                <div className="flex-1">
                  <h3 className="text-xl font-bold text-secondary-900 mb-2">
                    {agent.name}
                  </h3>
                  <p className="text-secondary-600 mb-4 leading-relaxed">
                    {agent.description}
                  </p>
                  
                  <div>
                    <h4 className="text-sm font-semibold text-secondary-800 mb-2 uppercase tracking-wide">
                      Core Capabilities
                    </h4>
                    <div className="grid grid-cols-2 gap-2">
                      {agent.capabilities.map((capability, capIndex) => (
                        <div key={capIndex} className="flex items-center">
                          <div className={`w-2 h-2 bg-${category.color}-500 rounded-full mr-2`} />
                          <span className="text-sm text-secondary-700">{capability}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Integration Info */}
      <div className={`mt-12 bg-gradient-to-r from-${category.color}-50 to-white rounded-xl border border-${category.color}-200 p-6`}>
        <div className="flex items-center mb-4">
          <Users className={`h-6 w-6 text-${category.color}-600 mr-3`} />
          <h3 className="text-lg font-semibold text-secondary-900">
            How These Agents Work Together
          </h3>
        </div>
        
        {activeTab === 'crew-agents' && (
          <p className="text-secondary-700 leading-relaxed">
            Crew Agents work in a coordinated tactical sequence: <strong>Research Agent</strong> gathers comprehensive 
            company intelligence, <strong>Scoring Agent</strong> evaluates and prioritizes leads, <strong>Outreach Agent</strong> 
            develops personalized messaging strategies, and <strong>Simulation Agent</strong> validates approaches through 
            conversation modeling. Together they provide complete tactical intelligence in 60-90 seconds.
          </p>
        )}
        
        {activeTab === 'ibm-agents' && (
          <p className="text-secondary-700 leading-relaxed">
            IBM Agents leverage Granite AI for strategic business intelligence: <strong>Market Intelligence</strong> sizes 
            opportunities, <strong>Technical Architecture</strong> designs implementation roadmaps, <strong>Executive Decision</strong> 
            builds business cases with ROI modeling, and <strong>Compliance & Risk</strong> ensures regulatory alignment. 
            This creates C-level strategic recommendations in 2-4 minutes.
          </p>
        )}
        
        {activeTab === 'advance-agents' && (
          <p className="text-secondary-700 leading-relaxed">
            Advanced Intelligence Agents provide specialized deep insights: <strong>Behavioral Psychology</strong> profiles 
            decision-makers, <strong>Competitive Intelligence</strong> maps market threats, <strong>Economic Analysis</strong> 
            assesses market timing, <strong>Predictive Forecasting</strong> models success probabilities, and <strong>Document Intelligence</strong> 
            extracts contextual insights. These agents turn good intelligence into exceptional strategic advantage.
          </p>
        )}
      </div>
    </div>
  );
};

export default AgentInfo;