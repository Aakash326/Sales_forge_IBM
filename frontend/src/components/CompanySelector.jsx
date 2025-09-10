import React, { useState, useEffect } from 'react';
import { Building2, Users, MapPin, DollarSign, CheckCircle, Mail, AlertCircle, Loader2 } from 'lucide-react';
import { apiService } from '../services/api';

const CompanySelector = ({ onRunBatchWorkflow, isLoading }) => {
  const [companies, setCompanies] = useState([]);
  const [selectedCompanies, setSelectedCompanies] = useState([]);
  const [workflowType, setWorkflowType] = useState('basic');
  const [sendEmails, setSendEmails] = useState(true);
  const [loadingCompanies, setLoadingCompanies] = useState(true);
  const [error, setError] = useState(null);
  const [filterIndustry, setFilterIndustry] = useState('all');

  useEffect(() => {
    loadCompanies();
  }, []);

  const loadCompanies = async () => {
    try {
      setLoadingCompanies(true);
      const response = await fetch('http://localhost:8000/api/companies');
      const data = await response.json();
      setCompanies(data.companies || []);
    } catch (err) {
      setError('Failed to load companies from database');
      console.error('Error loading companies:', err);
    } finally {
      setLoadingCompanies(false);
    }
  };

  const handleCompanyToggle = (companyName) => {
    setSelectedCompanies(prev => 
      prev.includes(companyName) 
        ? prev.filter(name => name !== companyName)
        : [...prev, companyName]
    );
  };

  const handleSelectAll = () => {
    const filteredCompanies = getFilteredCompanies();
    if (selectedCompanies.length === filteredCompanies.length) {
      setSelectedCompanies([]);
    } else {
      setSelectedCompanies(filteredCompanies.map(comp => comp.company_name));
    }
  };

  const handleRunWorkflow = () => {
    if (selectedCompanies.length === 0) {
      setError('Please select at least one company');
      return;
    }

    const selectionData = {
      company_names: selectedCompanies,
      workflow_type: workflowType,
      send_emails: sendEmails
    };

    onRunBatchWorkflow(selectionData);
  };

  const getFilteredCompanies = () => {
    if (filterIndustry === 'all') {
      return companies;
    }
    return companies.filter(comp => comp.industry === filterIndustry);
  };

  const getWorkflowInfo = (type) => {
    const info = {
      basic: { 
        agents: 8, 
        time: '4-5 minutes', 
        description: 'CrewAI Tactical (4) + IBM Strategic (4)',
        coverage: '65% Intelligence',
        realAgents: ['Lead Research Agent', 'Scoring Agent', 'Outreach Agent', 'Simulation Agent', 'Market Intelligence', 'Technical Architecture', 'Executive Decision', 'Compliance & Risk']
      },
      intermediate: { 
        agents: 11, 
        time: '7-9 minutes', 
        description: 'CrewAI (4) + IBM Strategic (4) + Advanced (3)',
        coverage: '85% Intelligence', 
        realAgents: ['+ Behavioral Psychology', '+ Competitive Intelligence', '+ Predictive Analytics']
      },
      advanced: { 
        agents: 13, 
        time: '10-15 minutes', 
        description: 'CrewAI (4) + IBM Strategic (4) + Advanced (5)',
        coverage: '100% Intelligence',
        realAgents: ['+ Economic Analysis', '+ Document Intelligence', '+ Full Advanced Suite']
      }
    };
    return info[type];
  };

  if (loadingCompanies) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-secondary-200 p-8 text-center">
        <Loader2 className="h-8 w-8 text-primary-600 animate-spin mx-auto mb-4" />
        <h3 className="text-lg font-medium text-secondary-900 mb-2">Loading Companies</h3>
        <p className="text-secondary-600">Fetching companies from database...</p>
      </div>
    );
  }

  const filteredCompanies = getFilteredCompanies();

  return (
    <div className="bg-white rounded-xl shadow-sm border border-secondary-200 p-6">
      <div className="flex items-center mb-6">
        <div className="p-2 bg-primary-100 rounded-lg mr-3">
          <Building2 className="h-6 w-6 text-primary-600" />
        </div>
        <div>
          <h3 className="text-lg font-semibold text-secondary-900">Company Database</h3>
          <p className="text-sm text-secondary-600">Select companies for AI analysis and automatic email campaigns</p>
        </div>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg flex items-center">
          <AlertCircle className="h-5 w-5 text-red-500 mr-2" />
          <span className="text-sm text-red-700">{error}</span>
        </div>
      )}

      {/* Workflow Configuration */}
      <div className="mb-6 p-4 bg-secondary-50 rounded-lg">
        <h4 className="text-sm font-semibold text-secondary-900 mb-3">Workflow Configuration</h4>
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-4">
          {['basic', 'intermediate', 'advanced'].map(type => {
            const info = getWorkflowInfo(type);
            return (
              <label key={type} className={`
                flex flex-col p-4 rounded-lg border-2 cursor-pointer transition-all hover:shadow-md
                ${workflowType === type 
                  ? 'border-primary-500 bg-primary-50 shadow-md' 
                  : 'border-secondary-200 hover:border-secondary-300'
                }
              `}>
                <input
                  type="radio"
                  name="workflowType"
                  value={type}
                  checked={workflowType === type}
                  onChange={(e) => setWorkflowType(e.target.value)}
                  className="sr-only"
                />
                
                {/* Header */}
                <div className="flex items-center justify-between mb-2">
                  <span className="font-semibold text-sm capitalize text-secondary-900">{type} Platform</span>
                  <div className="flex items-center space-x-2">
                    <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full">{info.agents} agents</span>
                  </div>
                </div>
                
                {/* Architecture */}
                <div className="text-xs text-secondary-700 mb-2 font-medium">{info.description}</div>
                
                {/* Coverage & Time */}
                <div className="flex items-center justify-between text-xs text-secondary-600 mb-3">
                  <span>{info.coverage}</span>
                  <span>{info.time}</span>
                </div>
                
                {/* Real Agents Preview */}
                <div className="text-xs text-secondary-500 space-y-1">
                  {type === 'basic' && (
                    <div>
                      <div className="font-medium text-secondary-600 mb-1">Core Agents:</div>
                      <div>• Lead Research & Scoring</div>
                      <div>• Market Intelligence</div>  
                      <div>• Technical Architecture</div>
                      <div>• Executive Decision Support</div>
                    </div>
                  )}
                  {type === 'intermediate' && (
                    <div>
                      <div className="font-medium text-secondary-600 mb-1">Core + Advanced:</div>
                      <div>• All Basic agents</div>
                      <div>• Behavioral Psychology</div>
                      <div>• Competitive Intelligence</div>
                      <div>• Predictive Analytics</div>
                    </div>
                  )}
                  {type === 'advanced' && (
                    <div>
                      <div className="font-medium text-secondary-600 mb-1">Complete Suite:</div>
                      <div>• All Intermediate agents</div>
                      <div>• Economic Analysis</div>
                      <div>• Document Intelligence</div>
                      <div>• Full AI Research Suite</div>
                    </div>
                  )}
                </div>
              </label>
            );
          })}
        </div>

        <label className="flex items-center">
          <input
            type="checkbox"
            checked={sendEmails}
            onChange={(e) => setSendEmails(e.target.checked)}
            className="mr-2 h-4 w-4 text-primary-600 border-secondary-300 rounded focus:ring-primary-500"
          />
          <Mail className="h-4 w-4 mr-1" />
          <span className="text-sm text-secondary-700">Send emails automatically after analysis</span>
        </label>
      </div>

      {/* Company Filter and Selection */}
      <div className="mb-4">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center space-x-4">
            <select
              value={filterIndustry}
              onChange={(e) => setFilterIndustry(e.target.value)}
              className="px-3 py-1 border border-secondary-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            >
              <option value="all">All Industries</option>
              <option value="Finance">Finance</option>
              <option value="Healthcare">Healthcare</option>
              <option value="Technology">Technology</option>
            </select>
            
            <button
              onClick={handleSelectAll}
              className="text-sm text-primary-600 hover:text-primary-700 font-medium"
            >
              {selectedCompanies.length === filteredCompanies.length ? 'Deselect All' : 'Select All'}
            </button>
          </div>
          
          <div className="text-sm text-secondary-600">
            {selectedCompanies.length} of {filteredCompanies.length} companies selected
          </div>
        </div>
      </div>

      {/* Companies Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6 max-h-96 overflow-y-auto">
        {filteredCompanies.map((company) => (
          <div
            key={company.company_name}
            className={`
              p-4 border-2 rounded-lg cursor-pointer transition-all
              ${selectedCompanies.includes(company.company_name)
                ? 'border-primary-500 bg-primary-50 shadow-md'
                : 'border-secondary-200 hover:border-secondary-300 hover:shadow-sm'
              }
            `}
            onClick={() => handleCompanyToggle(company.company_name)}
          >
            <div className="flex items-start justify-between mb-2">
              <h4 className="font-semibold text-sm text-secondary-900 leading-tight">
                {company.company_name}
              </h4>
              {selectedCompanies.includes(company.company_name) && (
                <CheckCircle className="h-5 w-5 text-primary-600 flex-shrink-0 ml-2" />
              )}
            </div>
            
            <div className="space-y-1">
              <div className="flex items-center text-xs text-secondary-600">
                <Building2 className="h-3 w-3 mr-1" />
                <span>{company.industry}</span>
              </div>
              
              <div className="flex items-center text-xs text-secondary-600">
                <MapPin className="h-3 w-3 mr-1" />
                <span>{company.location}</span>
              </div>
              
              <div className="flex items-center text-xs text-secondary-600">
                <Users className="h-3 w-3 mr-1" />
                <span>{company.company_size?.toLocaleString()} employees</span>
              </div>
              
              <div className="flex items-center text-xs text-secondary-600">
                <DollarSign className="h-3 w-3 mr-1" />
                <span>${(company.annual_revenue / 1000000).toFixed(0)}M revenue</span>
              </div>
              
              <div className="mt-2 flex items-center">
                <div className="text-xs font-medium text-primary-600">
                  Score: {company.performance_score}/100
                </div>
                <div className="ml-2 flex-1 bg-secondary-200 rounded-full h-1.5">
                  <div 
                    className="bg-primary-500 h-1.5 rounded-full"
                    style={{ width: `${company.performance_score}%` }}
                  ></div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Run Workflow Button */}
      <div className="flex justify-end pt-4 border-t border-secondary-200">
        <button
          onClick={handleRunWorkflow}
          disabled={isLoading || selectedCompanies.length === 0}
          className={`
            px-8 py-3 font-semibold rounded-lg transition-all duration-200
            ${isLoading || selectedCompanies.length === 0
              ? 'bg-secondary-300 text-secondary-500 cursor-not-allowed'
              : 'bg-primary-600 hover:bg-primary-700 text-white hover:shadow-lg transform hover:-translate-y-0.5'
            }
          `}
        >
          {isLoading ? (
            <span className="flex items-center">
              <Loader2 className="animate-spin h-4 w-4 mr-2" />
              Running Analysis...
            </span>
          ) : (
            <span className="flex items-center">
              <Building2 className="h-4 w-4 mr-2" />
              Run {workflowType.charAt(0).toUpperCase() + workflowType.slice(1)} Workflow ({selectedCompanies.length})
            </span>
          )}
        </button>
      </div>

      {/* Info Box */}
      <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
        <div className="flex items-start">
          <div className="flex-shrink-0">
            <div className="h-5 w-5 text-blue-500">ℹ️</div>
          </div>
          <div className="ml-3">
            <h4 className="text-sm font-medium text-blue-900">Automated Workflow</h4>
            <p className="text-xs text-blue-700 mt-1">
              Selected companies will be analyzed using AI intelligence agents. 
              {sendEmails ? ' Personalized emails will be sent automatically after analysis.' : ' No emails will be sent.'}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CompanySelector;