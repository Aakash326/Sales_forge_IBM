import React, { useState, useEffect } from 'react';
import { 
  X, Mail, Send, Copy, CheckCircle, Clock, AlertCircle, 
  Eye, Download, FileText, User, Building2
} from 'lucide-react';

const EmailOutputsModal = ({ isOpen, onClose, emailOutputs = [] }) => {
  const [selectedEmailIndex, setSelectedEmailIndex] = useState(0);
  const [copiedEmail, setCopiedEmail] = useState(null);

  useEffect(() => {
    if (emailOutputs.length > 0) {
      setSelectedEmailIndex(emailOutputs.length - 1); // Show latest email
    }
  }, [emailOutputs]);

  const copyToClipboard = (text, emailId) => {
    navigator.clipboard.writeText(text).then(() => {
      setCopiedEmail(emailId);
      setTimeout(() => setCopiedEmail(null), 2000);
    });
  };

  const exportEmails = () => {
    const emailData = emailOutputs.map(email => ({
      company: email.company_name,
      recipient: email.recipient,
      subject: email.subject,
      body: email.body,
      timestamp: email.timestamp,
      status: email.status
    }));

    const dataStr = JSON.stringify(emailData, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    
    const exportFileDefaultName = `sales-forge-emails-${new Date().toISOString().split('T')[0]}.json`;
    
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'sent':
        return <CheckCircle className="h-4 w-4 text-emerald-500" />;
      case 'sending':
        return <Clock className="h-4 w-4 text-amber-500" />;
      case 'failed':
        return <AlertCircle className="h-4 w-4 text-red-500" />;
      default:
        return <Mail className="h-4 w-4 text-secondary-400" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'sent':
        return 'text-emerald-600 bg-emerald-50';
      case 'sending':
        return 'text-amber-600 bg-amber-50';
      case 'failed':
        return 'text-red-600 bg-red-50';
      default:
        return 'text-secondary-600 bg-secondary-50';
    }
  };

  if (!isOpen) return null;

  const selectedEmail = emailOutputs[selectedEmailIndex];

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl shadow-2xl max-w-6xl w-full max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-secondary-200">
          <div className="flex items-center">
            <Mail className="h-6 w-6 text-primary-600 mr-3" />
            <div>
              <h3 className="text-lg font-semibold text-secondary-900">
                Email Outputs ({emailOutputs.length})
              </h3>
              <p className="text-sm text-secondary-600">
                Real-time view of AI-generated emails
              </p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <button
              onClick={exportEmails}
              className="flex items-center px-3 py-2 text-sm bg-secondary-100 hover:bg-secondary-200 text-secondary-700 rounded-lg transition-colors"
            >
              <Download className="h-4 w-4 mr-1" />
              Export
            </button>
            <button
              onClick={onClose}
              className="p-2 hover:bg-secondary-100 rounded-lg transition-colors"
            >
              <X className="h-5 w-5 text-secondary-500" />
            </button>
          </div>
        </div>

        <div className="flex h-[600px]">
          {/* Email List Sidebar */}
          <div className="w-1/3 border-r border-secondary-200 overflow-y-auto">
            <div className="p-4 border-b border-secondary-200">
              <h4 className="text-sm font-semibold text-secondary-900 mb-2">Email History</h4>
              <div className="text-xs text-secondary-600">
                {emailOutputs.filter(e => e.status === 'sent').length} sent • 
                {emailOutputs.filter(e => e.status === 'sending').length} sending • 
                {emailOutputs.filter(e => e.status === 'failed').length} failed
              </div>
            </div>
            
            <div className="p-2">
              {emailOutputs.map((email, index) => (
                <div
                  key={`${email.company_name}-${index}`}
                  onClick={() => setSelectedEmailIndex(index)}
                  className={`p-3 mb-2 rounded-lg cursor-pointer transition-all ${
                    selectedEmailIndex === index
                      ? 'bg-primary-50 border-2 border-primary-200'
                      : 'bg-secondary-50 hover:bg-secondary-100 border border-secondary-200'
                  }`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center">
                      <Building2 className="h-4 w-4 text-secondary-500 mr-2" />
                      <span className="text-sm font-medium text-secondary-900">
                        {email.company_name}
                      </span>
                    </div>
                    {getStatusIcon(email.status)}
                  </div>
                  
                  <div className="flex items-center text-xs text-secondary-600 mb-1">
                    <User className="h-3 w-3 mr-1" />
                    {email.recipient}
                  </div>
                  
                  <div className="text-xs text-secondary-500 truncate mb-2">
                    {email.subject}
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <span className={`text-xs px-2 py-1 rounded-full ${getStatusColor(email.status)}`}>
                      {email.status}
                    </span>
                    <span className="text-xs text-secondary-500">
                      {new Date(email.timestamp).toLocaleTimeString()}
                    </span>
                  </div>
                </div>
              ))}
              
              {emailOutputs.length === 0 && (
                <div className="text-center py-8">
                  <Mail className="h-12 w-12 text-secondary-300 mx-auto mb-3" />
                  <p className="text-sm text-secondary-600">No emails generated yet</p>
                  <p className="text-xs text-secondary-500 mt-1">
                    Emails will appear here as they are generated
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Email Content */}
          <div className="flex-1 flex flex-col">
            {selectedEmail ? (
              <>
                {/* Email Header */}
                <div className="p-6 border-b border-secondary-200">
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center">
                      {getStatusIcon(selectedEmail.status)}
                      <span className={`ml-2 px-3 py-1 rounded-full text-sm ${getStatusColor(selectedEmail.status)}`}>
                        {selectedEmail.status.charAt(0).toUpperCase() + selectedEmail.status.slice(1)}
                      </span>
                    </div>
                    
                    <button
                      onClick={() => copyToClipboard(`Subject: ${selectedEmail.subject}\n\nTo: ${selectedEmail.recipient}\n\n${selectedEmail.body}`, selectedEmail.company_name)}
                      className="flex items-center px-3 py-2 text-sm bg-secondary-100 hover:bg-secondary-200 text-secondary-700 rounded-lg transition-colors"
                    >
                      {copiedEmail === selectedEmail.company_name ? (
                        <>
                          <CheckCircle className="h-4 w-4 mr-1" />
                          Copied
                        </>
                      ) : (
                        <>
                          <Copy className="h-4 w-4 mr-1" />
                          Copy Email
                        </>
                      )}
                    </button>
                  </div>

                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="text-secondary-600">Company:</span>
                      <span className="ml-2 font-medium text-secondary-900">{selectedEmail.company_name}</span>
                    </div>
                    <div>
                      <span className="text-secondary-600">Recipient:</span>
                      <span className="ml-2 font-medium text-secondary-900">{selectedEmail.recipient}</span>
                    </div>
                    <div>
                      <span className="text-secondary-600">Generated:</span>
                      <span className="ml-2 font-medium text-secondary-900">
                        {new Date(selectedEmail.timestamp).toLocaleString()}
                      </span>
                    </div>
                    <div>
                      <span className="text-secondary-600">AI Analysis:</span>
                      <span className="ml-2 font-medium text-primary-600">
                        {selectedEmail.lead_score ? `${(selectedEmail.lead_score * 100).toFixed(0)}% Score` : 'Processing...'}
                      </span>
                    </div>
                  </div>

                  <div className="mt-4">
                    <span className="text-secondary-600 text-sm">Subject:</span>
                    <div className="mt-1 p-3 bg-secondary-50 rounded-lg">
                      <span className="font-medium text-secondary-900">{selectedEmail.subject}</span>
                    </div>
                  </div>
                </div>

                {/* Email Body */}
                <div className="flex-1 p-6 overflow-y-auto">
                  <div className="bg-white border border-secondary-200 rounded-lg p-6">
                    <div className="whitespace-pre-wrap text-secondary-800 leading-relaxed">
                      {selectedEmail.body}
                    </div>
                  </div>
                  
                  {selectedEmail.ai_insights && (
                    <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                      <h5 className="text-sm font-semibold text-blue-900 mb-2 flex items-center">
                        <Eye className="h-4 w-4 mr-2" />
                        AI Insights
                      </h5>
                      <div className="text-sm text-blue-800 space-y-1">
                        {selectedEmail.ai_insights.map((insight, idx) => (
                          <div key={idx}>• {insight}</div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </>
            ) : (
              <div className="flex-1 flex items-center justify-center">
                <div className="text-center">
                  <FileText className="h-12 w-12 text-secondary-300 mx-auto mb-3" />
                  <p className="text-secondary-600">Select an email to view its content</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default EmailOutputsModal;