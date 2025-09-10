import React, { useState } from 'react';
import { 
  Building2, CheckCircle, XCircle, Mail, MailCheck, MailX, 
  TrendingUp, Target, DollarSign, Users, ChevronDown, ChevronRight,
  AlertCircle, Clock, Brain
} from 'lucide-react';

const BatchResultsDisplay = ({ batchResults, workflowName }) => {
  const [expandedResults, setExpandedResults] = useState({});

  if (!batchResults) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-secondary-200 p-8 text-center">
        <Brain className="h-16 w-16 text-secondary-300 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-secondary-900 mb-2">Ready for Batch Analysis</h3>
        <p className="text-secondary-600">Select companies and run a workflow to see results here</p>
      </div>
    );
  }

  const toggleExpanded = (companyName) => {
    setExpandedResults(prev => ({
      ...prev,
      [companyName]: !prev[companyName]
    }));
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="h-5 w-5 text-emerald-500" />;
      case 'failed':
        return <XCircle className="h-5 w-5 text-red-500" />;
      default:
        return <Clock className="h-5 w-5 text-amber-500" />;
    }
  };

  const getEmailStatusIcon = (emailSent) => {
    if (emailSent) {
      return <MailCheck className="h-4 w-4 text-emerald-500" />;
    }
    return <MailX className="h-4 w-4 text-secondary-400" />;
  };

  return (
    <div className="space-y-6">
      {/* Batch Summary */}
      <div className="bg-white rounded-xl shadow-sm border border-secondary-200 p-6">
        <div className="flex items-center mb-4">
          <div className="p-2 bg-primary-100 rounded-lg mr-3">
            <Building2 className="h-6 w-6 text-primary-600" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-secondary-900">Batch Workflow Results</h3>
            <p className="text-sm text-secondary-600">{workflowName} - Batch ID: {batchResults.batch_id}</p>
          </div>
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-blue-50 p-4 rounded-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-blue-600 font-medium">Companies Processed</p>
                <p className="text-2xl font-bold text-blue-900">{batchResults.companies_processed}</p>
              </div>
              <Users className="h-8 w-8 text-blue-500" />
            </div>
          </div>

          <div className="bg-emerald-50 p-4 rounded-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-emerald-600 font-medium">Successful</p>
                <p className="text-2xl font-bold text-emerald-900">{batchResults.summary.successful_workflows}</p>
              </div>
              <CheckCircle className="h-8 w-8 text-emerald-500" />
            </div>
          </div>

          <div className="bg-amber-50 p-4 rounded-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-amber-600 font-medium">Emails Sent</p>
                <p className="text-2xl font-bold text-amber-900">{batchResults.emails_sent}</p>
              </div>
              <Mail className="h-8 w-8 text-amber-500" />
            </div>
          </div>

          <div className="bg-red-50 p-4 rounded-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-red-600 font-medium">Failed</p>
                <p className="text-2xl font-bold text-red-900">{batchResults.summary.failed_workflows}</p>
              </div>
              <XCircle className="h-8 w-8 text-red-500" />
            </div>
          </div>
        </div>

        {/* Success Rate */}
        <div className="bg-secondary-50 p-4 rounded-lg">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-secondary-700">Success Rate</span>
            <span className="text-sm font-bold text-secondary-900">
              {Math.round((batchResults.summary.successful_workflows / batchResults.companies_processed) * 100)}%
            </span>
          </div>
          <div className="w-full bg-secondary-200 rounded-full h-2">
            <div 
              className="bg-emerald-500 h-2 rounded-full"
              style={{ 
                width: `${(batchResults.summary.successful_workflows / batchResults.companies_processed) * 100}%` 
              }}
            ></div>
          </div>
        </div>
      </div>

      {/* Individual Results */}
      <div className="bg-white rounded-xl shadow-sm border border-secondary-200">
        <div className="p-6 border-b border-secondary-200">
          <h4 className="text-lg font-semibold text-secondary-900">Individual Company Results</h4>
          <p className="text-sm text-secondary-600 mt-1">Click on any company to see detailed analysis</p>
        </div>

        <div className="divide-y divide-secondary-200">
          {batchResults.results.map((result, index) => (
            <div key={result.company_name} className="p-4">
              <div 
                className="flex items-center justify-between cursor-pointer hover:bg-secondary-50 p-2 rounded-lg transition-colors"
                onClick={() => toggleExpanded(result.company_name)}
              >
                <div className="flex items-center space-x-4">
                  {getStatusIcon(result.status)}
                  
                  <div>
                    <h5 className="font-semibold text-secondary-900">{result.company_name}</h5>
                    <div className="flex items-center space-x-3 mt-1">
                      <span className={`text-xs px-2 py-1 rounded-full ${
                        result.status === 'completed' 
                          ? 'bg-emerald-100 text-emerald-800'
                          : result.status === 'failed'
                          ? 'bg-red-100 text-red-800'  
                          : 'bg-amber-100 text-amber-800'
                      }`}>
                        {result.status}
                      </span>
                      
                      <div className="flex items-center space-x-1">
                        {getEmailStatusIcon(result.email_sent)}
                        <span className="text-xs text-secondary-600">
                          {result.email_sent ? 'Email Sent' : 'No Email'}
                        </span>
                      </div>
                      
                      {result.workflow_id && (
                        <span className="text-xs text-secondary-500">
                          ID: {result.workflow_id.slice(-8)}
                        </span>
                      )}
                    </div>
                  </div>
                </div>

                <div className="flex items-center space-x-2">
                  {result.results_summary && result.status === 'completed' && (
                    <div className="text-right text-xs text-secondary-600 mr-4">
                      <div>Score: {(result.results_summary.lead_score * 100).toFixed(0)}%</div>
                      <div>ROI: {result.results_summary.projected_roi}x</div>
                    </div>
                  )}
                  
                  {expandedResults[result.company_name] ? (
                    <ChevronDown className="h-5 w-5 text-secondary-400" />
                  ) : (
                    <ChevronRight className="h-5 w-5 text-secondary-400" />
                  )}
                </div>
              </div>

              {/* Expanded Details */}
              {expandedResults[result.company_name] && (
                <div className="mt-4 pl-6 space-y-4">
                  {result.status === 'completed' && result.results_summary ? (
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div className="bg-blue-50 p-3 rounded-lg">
                        <div className="flex items-center">
                          <Target className="h-4 w-4 text-blue-600 mr-2" />
                          <span className="text-sm font-medium text-blue-900">Lead Score</span>
                        </div>
                        <p className="text-lg font-bold text-blue-900 mt-1">
                          {(result.results_summary.lead_score * 100).toFixed(0)}%
                        </p>
                        <div className="mt-2 w-full bg-blue-200 rounded-full h-1.5">
                          <div 
                            className="bg-blue-600 h-1.5 rounded-full"
                            style={{ width: `${result.results_summary.lead_score * 100}%` }}
                          ></div>
                        </div>
                      </div>

                      <div className="bg-emerald-50 p-3 rounded-lg">
                        <div className="flex items-center">
                          <TrendingUp className="h-4 w-4 text-emerald-600 mr-2" />
                          <span className="text-sm font-medium text-emerald-900">Conversion</span>
                        </div>
                        <p className="text-lg font-bold text-emerald-900 mt-1">
                          {(result.results_summary.conversion_probability * 100).toFixed(0)}%
                        </p>
                        <div className="mt-2 w-full bg-emerald-200 rounded-full h-1.5">
                          <div 
                            className="bg-emerald-600 h-1.5 rounded-full"
                            style={{ width: `${result.results_summary.conversion_probability * 100}%` }}
                          ></div>
                        </div>
                      </div>

                      <div className="bg-purple-50 p-3 rounded-lg">
                        <div className="flex items-center">
                          <DollarSign className="h-4 w-4 text-purple-600 mr-2" />
                          <span className="text-sm font-medium text-purple-900">Projected ROI</span>
                        </div>
                        <p className="text-lg font-bold text-purple-900 mt-1">
                          {result.results_summary.projected_roi}x
                        </p>
                        <p className="text-xs text-purple-600 mt-1">Return on Investment</p>
                      </div>
                    </div>
                  ) : result.status === 'failed' ? (
                    <div className="bg-red-50 border border-red-200 rounded-lg p-3">
                      <div className="flex items-center">
                        <AlertCircle className="h-4 w-4 text-red-500 mr-2" />
                        <span className="text-sm font-medium text-red-900">Error Details</span>
                      </div>
                      <p className="text-sm text-red-700 mt-1">{result.error || 'Unknown error occurred'}</p>
                    </div>
                  ) : null}

                  {result.email_sent && (
                    <div className="bg-emerald-50 border border-emerald-200 rounded-lg p-3">
                      <div className="flex items-center">
                        <MailCheck className="h-4 w-4 text-emerald-600 mr-2" />
                        <span className="text-sm font-medium text-emerald-900">Email Delivered</span>
                      </div>
                      <p className="text-sm text-emerald-700 mt-1">
                        Personalized email sent successfully based on AI analysis
                      </p>
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Action Summary */}
      <div className="bg-gradient-to-r from-primary-50 to-blue-50 border border-primary-200 rounded-xl p-6">
        <div className="flex items-center">
          <CheckCircle className="h-6 w-6 text-primary-600 mr-3" />
          <div>
            <h4 className="text-lg font-semibold text-primary-900">Batch Processing Complete</h4>
            <p className="text-sm text-primary-700 mt-1">
              Processed {batchResults.companies_processed} companies with {workflowName}.
              {batchResults.emails_sent > 0 && ` ${batchResults.emails_sent} personalized emails sent automatically.`}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BatchResultsDisplay;