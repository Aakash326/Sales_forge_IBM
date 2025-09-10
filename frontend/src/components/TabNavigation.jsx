import React from 'react';
import { Brain, Users, Building2 } from 'lucide-react';

const TabNavigation = ({ activeTab, onTabChange }) => {
  const tabs = [
    {
      id: 'advance-agents',
      name: 'Advance-Agents',
      count: 13,
      icon: Brain,
      description: 'Complete AI Intelligence Suite'
    },
    {
      id: 'crew-agents', 
      name: 'Crew Agents',
      count: 4,
      icon: Users,
      description: 'Tactical Intelligence Team'
    },
    {
      id: 'ibm-agents',
      name: 'IBM Agents', 
      count: 4,
      icon: Building2,
      description: 'Strategic Business Intelligence'
    }
  ];

  return (
    <div className="bg-white border-b border-secondary-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <nav className="flex space-x-8" aria-label="Tabs">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            
            return (
              <button
                key={tab.id}
                onClick={() => onTabChange(tab.id)}
                className={`
                  group inline-flex items-center py-4 px-1 border-b-2 font-medium text-sm transition-colors duration-200
                  ${isActive 
                    ? 'border-primary-500 text-primary-600' 
                    : 'border-transparent text-secondary-500 hover:text-secondary-700 hover:border-secondary-300'
                  }
                `}
                aria-current={isActive ? 'page' : undefined}
              >
                <Icon 
                  className={`
                    mr-2 h-5 w-5 transition-colors duration-200
                    ${isActive ? 'text-primary-500' : 'text-secondary-400 group-hover:text-secondary-500'}
                  `}
                />
                <span className="font-semibold">{tab.name}</span>
                <span 
                  className={`
                    ml-2 py-0.5 px-2.5 rounded-full text-xs font-medium transition-colors duration-200
                    ${isActive 
                      ? 'bg-primary-100 text-primary-600' 
                      : 'bg-secondary-100 text-secondary-500 group-hover:bg-secondary-200'
                    }
                  `}
                >
                  {tab.count}
                </span>
                <div className="hidden lg:block ml-2">
                  <span 
                    className={`
                      text-xs transition-colors duration-200
                      ${isActive ? 'text-primary-500' : 'text-secondary-400'}
                    `}
                  >
                    {tab.description}
                  </span>
                </div>
              </button>
            );
          })}
        </nav>
      </div>
    </div>
  );
};

export default TabNavigation;