import React from 'react';
import { 
  TrendingUp, 
  Target, 
  Clock, 
  DollarSign, 
  Users, 
  Mail, 
  CheckCircle, 
  AlertCircle,
  BarChart3,
  Brain,
  Zap
} from 'lucide-react';
import { 
  formatCurrency, 
  formatPercentage, 
  formatDuration, 
  getStatusColor,
  formatNumber 
} from '../utils/formatters';

const ResultsDisplay = ({ results, workflowName }) => {
  if (!results) return null;

  const StatusBadge = ({ status }) => {
    const colorClass = getStatusColor(status);
    const iconMap = {
      'completed': CheckCircle,
      'pending_user_approval': AlertCircle,
      'running': Clock
    };
    const Icon = iconMap[status] || CheckCircle;

    return (
      <span className={`status-badge status-${colorClass} flex items-center`}>
        <Icon className="h-3 w-3 mr-1" />
        {status.replace('_', ' ').toUpperCase()}
      </span>
    );
  };

  const MetricCard = ({ icon: Icon, title, value, subtitle, color = 'primary' }) => (
    <div className="metric-card">
      <div className="flex items-center justify-between">
        <div className={`p-2 bg-${color}-100 rounded-lg`}>
          <Icon className={`h-5 w-5 text-${color}-600`} />
        </div>
        <div className="text-right">
          <div className="text-2xl font-bold text-secondary-900">{value}</div>
          {subtitle && <div className="text-xs text-secondary-500">{subtitle}</div>}
        </div>
      </div>
      <div className="mt-3">
        <h4 className="text-sm font-medium text-secondary-700">{title}</h4>
      </div>
    </div>
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-xl shadow-sm border border-secondary-200 p-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-2xl font-bold text-secondary-900">
              Analysis Results
            </h2>
            <p className="text-secondary-600 mt-1">
              {workflowName} • Workflow ID: {results.workflow_id.slice(0, 8)}
            </p>
          </div>
          <div className="text-right">
            <StatusBadge status={results.status} />
            <div className="text-sm text-secondary-500 mt-1">
              Completed in {formatDuration(results.execution_time_seconds)}
            </div>
          </div>
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <MetricCard
            icon={Users}
            title="Agents Executed"
            value={results.platform_metrics.agents_executed}
            subtitle="AI Agents"
            color="primary"
          />
          <MetricCard
            icon={Clock}
            title="Processing Time"
            value={formatDuration(results.execution_time_seconds)}
            subtitle="Total Duration"
            color="emerald"
          />
          <MetricCard
            icon={Brain}
            title="Intelligence Depth"
            value={results.platform_metrics.intelligence_depth}
            subtitle="Coverage"
            color="purple"
          />
          <MetricCard
            icon={DollarSign}
            title="Estimated Cost"
            value={results.platform_metrics.cost_estimate}
            subtitle={`${formatNumber(results.platform_metrics.tokens_used)} tokens`}
            color="orange"
          />
        </div>
      </div>

      {/* Tactical Intelligence */}
      {results.tactical_intelligence && (
        <div className="bg-white rounded-xl shadow-sm border border-secondary-200 p-6">
          <div className="flex items-center mb-4">
            <div className="p-2 bg-blue-100 rounded-lg mr-3">
              <Target className="h-6 w-6 text-blue-600" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-secondary-900">
                Tactical Intelligence
              </h3>
              <p className="text-sm text-secondary-600">
                Lead qualification and tactical insights
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
            <MetricCard
              icon={TrendingUp}
              title="Lead Score"
              value={`${(results.tactical_intelligence.lead_score * 100).toFixed(0)}%`}
              subtitle="Quality Rating"
              color="blue"
            />
            <MetricCard
              icon={Target}
              title="Conversion Probability"
              value={formatPercentage(results.tactical_intelligence.conversion_probability)}
              subtitle="Success Likelihood"
              color="green"
            />
            <MetricCard
              icon={BarChart3}
              title="Engagement Level"
              value={formatPercentage(results.tactical_intelligence.engagement_level)}
              subtitle="Current Interest"
              color="indigo"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-medium text-secondary-900 mb-3">Identified Pain Points</h4>
              <ul className="space-y-2">
                {results.tactical_intelligence.pain_points_identified.map((point, index) => (
                  <li key={index} className="flex items-start">
                    <AlertCircle className="h-4 w-4 text-orange-500 mt-0.5 mr-2 flex-shrink-0" />
                    <span className="text-sm text-secondary-700">{point}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div>
              <h4 className="font-medium text-secondary-900 mb-3">Technology Stack</h4>
              <div className="flex flex-wrap gap-2">
                {results.tactical_intelligence.tech_stack_analyzed.map((tech, index) => (
                  <span 
                    key={index}
                    className="px-3 py-1 bg-secondary-100 text-secondary-700 rounded-full text-sm font-medium"
                  >
                    {tech}
                  </span>
                ))}
              </div>
            </div>
          </div>

          <div className="mt-6 p-4 bg-blue-50 rounded-lg">
            <h4 className="font-medium text-blue-900 mb-2">Recommended Strategy</h4>
            <p className="text-sm text-blue-800">{results.tactical_intelligence.outreach_strategy}</p>
            <div className="mt-3 grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
              <div>
                <span className="font-medium text-blue-900">Best Contact Time:</span>
                <br />
                <span className="text-blue-700">{results.tactical_intelligence.best_contact_time}</span>
              </div>
              <div>
                <span className="font-medium text-blue-900">Budget Authority:</span>
                <br />
                <span className="text-blue-700">{results.tactical_intelligence.budget_authority}</span>
              </div>
              <div>
                <span className="font-medium text-blue-900">Timeline:</span>
                <br />
                <span className="text-blue-700">{results.tactical_intelligence.timeline_urgency}</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Strategic Intelligence */}
      {results.strategic_intelligence && (
        <div className="bg-white rounded-xl shadow-sm border border-secondary-200 p-6">
          <div className="flex items-center mb-4">
            <div className="p-2 bg-purple-100 rounded-lg mr-3">
              <Brain className="h-6 w-6 text-purple-600" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-secondary-900">
                Strategic Intelligence
              </h3>
              <p className="text-sm text-secondary-600">
                Business case and strategic analysis
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
            <MetricCard
              icon={DollarSign}
              title="Investment Required"
              value={formatCurrency(results.strategic_intelligence.investment_required)}
              subtitle="Total Investment"
              color="purple"
            />
            <MetricCard
              icon={TrendingUp}
              title="Projected ROI"
              value={`${results.strategic_intelligence.projected_roi}x`}
              subtitle="Return Multiple"
              color="green"
            />
            <MetricCard
              icon={Clock}
              title="Payback Period"
              value={`${results.strategic_intelligence.payback_period_months}`}
              subtitle="Months"
              color="blue"
            />
            <MetricCard
              icon={BarChart3}
              title="Market Size"
              value={formatCurrency(results.strategic_intelligence.market_size)}
              subtitle={`${formatPercentage(results.strategic_intelligence.market_growth_rate)} growth`}
              color="emerald"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-4">
              <div>
                <h4 className="font-medium text-secondary-900 mb-2">Implementation</h4>
                <p className="text-sm text-secondary-600">
                  Timeline: <span className="font-medium">{results.strategic_intelligence.implementation_timeline}</span>
                </p>
                <p className="text-sm text-secondary-600">
                  Feasibility: <span className="font-medium">{formatPercentage(results.strategic_intelligence.technical_feasibility)}</span>
                </p>
              </div>
              
              <div>
                <h4 className="font-medium text-secondary-900 mb-2">Risk Assessment</h4>
                <p className="text-sm text-secondary-600">
                  Risk Level: <span className="font-medium">{results.strategic_intelligence.risk_level}</span>
                </p>
                <p className="text-sm text-secondary-600">
                  Compliance: <span className="font-medium">{formatPercentage(results.strategic_intelligence.compliance_readiness)}</span>
                </p>
              </div>
            </div>

            <div>
              <h4 className="font-medium text-secondary-900 mb-2">Executive Recommendation</h4>
              <div className="p-4 bg-purple-50 rounded-lg">
                <p className="text-sm text-purple-800">
                  {results.strategic_intelligence.executive_recommendation}
                </p>
                <div className="mt-3">
                  <span className="text-xs font-medium text-purple-600">
                    Confidence: {formatPercentage(results.strategic_intelligence.confidence_score)}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Advanced Intelligence */}
      {results.advanced_intelligence && (
        <div className="bg-white rounded-xl shadow-sm border border-secondary-200 p-6">
          <div className="flex items-center mb-4">
            <div className="p-2 bg-indigo-100 rounded-lg mr-3">
              <Zap className="h-6 w-6 text-indigo-600" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-secondary-900">
                Advanced Intelligence
              </h3>
              <p className="text-sm text-secondary-600">
                Specialized behavioral and competitive insights
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <h4 className="font-medium text-secondary-900 mb-3">Behavioral Profile</h4>
              <div className="p-3 bg-indigo-50 rounded-lg">
                <p className="text-sm font-medium text-indigo-800">
                  {results.advanced_intelligence.behavioral_profile}
                </p>
                {results.advanced_intelligence.psychological_insights && (
                  <div className="mt-2 space-y-1 text-xs text-indigo-600">
                    <p>Communication: {results.advanced_intelligence.psychological_insights.communication_preference}</p>
                    <p>Decision Style: {results.advanced_intelligence.psychological_insights.decision_making_style}</p>
                    <p>Risk Tolerance: {results.advanced_intelligence.psychological_insights.risk_tolerance}</p>
                  </div>
                )}
              </div>
            </div>

            <div>
              <h4 className="font-medium text-secondary-900 mb-3">Market Analysis</h4>
              <div className="space-y-3">
                <div className="p-3 bg-orange-50 rounded-lg">
                  <p className="text-sm text-orange-800">
                    <span className="font-medium">Competitive Threats:</span> {results.advanced_intelligence.competitive_threats}
                  </p>
                </div>
                <div className="p-3 bg-blue-50 rounded-lg">
                  <p className="text-sm text-blue-800">
                    <span className="font-medium">Economic Climate:</span> {results.advanced_intelligence.economic_climate_impact}
                  </p>
                </div>
                <div className="p-3 bg-green-50 rounded-lg">
                  <p className="text-sm text-green-800">
                    <span className="font-medium">Success Probability:</span> {formatPercentage(results.advanced_intelligence.predictive_success_probability)}
                  </p>
                </div>
              </div>
            </div>

            <div>
              <h4 className="font-medium text-secondary-900 mb-3">Recommended Actions</h4>
              <ul className="space-y-2">
                {results.advanced_intelligence.recommended_actions.map((action, index) => (
                  <li key={index} className="flex items-start">
                    <CheckCircle className="h-4 w-4 text-green-500 mt-0.5 mr-2 flex-shrink-0" />
                    <span className="text-sm text-secondary-700">{action}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}

      {/* Email Preview */}
      {results.email_preview && (
        <div className="bg-white rounded-xl shadow-sm border border-secondary-200 p-6">
          <div className="flex items-center mb-4">
            <div className="p-2 bg-emerald-100 rounded-lg mr-3">
              <Mail className="h-6 w-6 text-emerald-600" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-secondary-900">
                Generated Email Preview
              </h3>
              <p className="text-sm text-secondary-600">
                AI-powered personalized outreach • {results.email_preview.personalization_level}
              </p>
            </div>
          </div>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-secondary-700 mb-2">Subject</label>
              <div className="p-3 bg-secondary-50 rounded-lg border">
                <p className="text-sm font-medium text-secondary-900">
                  {results.email_preview.subject}
                </p>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-secondary-700 mb-2">Message Body</label>
              <div className="p-4 bg-secondary-50 rounded-lg border">
                <pre className="text-sm text-secondary-800 whitespace-pre-wrap font-sans leading-relaxed">
                  {results.email_preview.body}
                </pre>
              </div>
            </div>

            <div className="flex items-center justify-between pt-4 border-t border-secondary-200">
              <div className="flex items-center text-sm text-secondary-600">
                <CheckCircle className="h-4 w-4 text-emerald-500 mr-2" />
                Email ready for review and sending
              </div>
              <div className="flex space-x-3">
                <button className="btn-secondary text-sm">
                  Edit Email
                </button>
                <button className="btn-primary text-sm">
                  <Mail className="h-4 w-4 mr-2" />
                  Send Email
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Recommendations */}
      {results.recommendations && results.recommendations.length > 0 && (
        <div className="bg-white rounded-xl shadow-sm border border-secondary-200 p-6">
          <h3 className="text-lg font-semibold text-secondary-900 mb-4">
            Strategic Recommendations
          </h3>
          <div className="space-y-3">
            {results.recommendations.map((recommendation, index) => (
              <div key={index} className="flex items-start p-3 bg-primary-50 rounded-lg">
                <div className="flex-shrink-0 w-6 h-6 bg-primary-600 text-white rounded-full flex items-center justify-center text-xs font-bold mr-3 mt-0.5">
                  {index + 1}
                </div>
                <p className="text-sm text-primary-800">{recommendation}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ResultsDisplay;