import React, { useState } from 'react';
import { Building2, User, Mail, MapPin, DollarSign, Users, Briefcase } from 'lucide-react';

const LeadForm = ({ onSubmit, isLoading }) => {
  const [formData, setFormData] = useState({
    company_name: '',
    contact_name: '',
    contact_email: '',
    company_size: 100,
    industry: '',
    location: '',
    annual_revenue: 1000000,
    pain_points: ['Manual processes', 'Data silos', 'Scalability challenges'],
    tech_stack: ['React', 'Node.js', 'Python', 'PostgreSQL', 'AWS']
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'company_size' || name === 'annual_revenue' 
        ? parseInt(value) || 0 
        : value
    }));
  };

  const handleArrayChange = (name, value) => {
    const items = value.split(',').map(item => item.trim()).filter(item => item);
    setFormData(prev => ({
      ...prev,
      [name]: items
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-secondary-200 p-6">
      <div className="flex items-center mb-6">
        <div className="p-2 bg-primary-100 rounded-lg mr-3">
          <Building2 className="h-6 w-6 text-primary-600" />
        </div>
        <div>
          <h3 className="text-lg font-semibold text-secondary-900">Lead Information</h3>
          <p className="text-sm text-secondary-600">Enter company and contact details for AI analysis</p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Company Information */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-secondary-700 mb-2">
              <Building2 className="inline h-4 w-4 mr-1" />
              Company Name *
            </label>
            <input
              type="text"
              name="company_name"
              value={formData.company_name}
              onChange={handleChange}
              required
              className="w-full px-3 py-2 border border-secondary-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
              placeholder="Enter company name"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-secondary-700 mb-2">
              <Briefcase className="inline h-4 w-4 mr-1" />
              Industry *
            </label>
            <select
              name="industry"
              value={formData.industry}
              onChange={handleChange}
              required
              className="w-full px-3 py-2 border border-secondary-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
            >
              <option value="">Select industry</option>
              <option value="Finance">Finance</option>
              <option value="Healthcare">Healthcare</option>
              <option value="Technology">Technology</option>
            </select>
          </div>
        </div>

        {/* Contact Information */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-secondary-700 mb-2">
              <User className="inline h-4 w-4 mr-1" />
              Contact Name *
            </label>
            <input
              type="text"
              name="contact_name"
              value={formData.contact_name}
              onChange={handleChange}
              required
              className="w-full px-3 py-2 border border-secondary-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
              placeholder="Enter contact name"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-secondary-700 mb-2">
              <Mail className="inline h-4 w-4 mr-1" />
              Contact Email *
            </label>
            <input
              type="email"
              name="contact_email"
              value={formData.contact_email}
              onChange={handleChange}
              required
              className="w-full px-3 py-2 border border-secondary-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
              placeholder="Enter email address"
            />
          </div>
        </div>

        {/* Company Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <label className="block text-sm font-medium text-secondary-700 mb-2">
              <Users className="inline h-4 w-4 mr-1" />
              Company Size *
            </label>
            <input
              type="number"
              name="company_size"
              value={formData.company_size}
              onChange={handleChange}
              required
              min="1"
              className="w-full px-3 py-2 border border-secondary-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
              placeholder="Number of employees"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-secondary-700 mb-2">
              <DollarSign className="inline h-4 w-4 mr-1" />
              Annual Revenue
            </label>
            <input
              type="number"
              name="annual_revenue"
              value={formData.annual_revenue}
              onChange={handleChange}
              min="0"
              className="w-full px-3 py-2 border border-secondary-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
              placeholder="Annual revenue (USD)"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-secondary-700 mb-2">
              <MapPin className="inline h-4 w-4 mr-1" />
              Location
            </label>
            <input
              type="text"
              name="location"
              value={formData.location}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-secondary-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
              placeholder="City, State/Country"
            />
          </div>
        </div>

        {/* Pain Points and Tech Stack */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-secondary-700 mb-2">
              Pain Points
            </label>
            <textarea
              value={formData.pain_points.join(', ')}
              onChange={(e) => handleArrayChange('pain_points', e.target.value)}
              rows={3}
              className="w-full px-3 py-2 border border-secondary-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
              placeholder="Enter pain points separated by commas"
            />
            <p className="text-xs text-secondary-500 mt-1">Separate multiple pain points with commas</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-secondary-700 mb-2">
              Tech Stack
            </label>
            <textarea
              value={formData.tech_stack.join(', ')}
              onChange={(e) => handleArrayChange('tech_stack', e.target.value)}
              rows={3}
              className="w-full px-3 py-2 border border-secondary-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
              placeholder="Enter technologies separated by commas"
            />
            <p className="text-xs text-secondary-500 mt-1">Separate multiple technologies with commas</p>
          </div>
        </div>

        {/* Submit Button */}
        <div className="flex justify-end pt-4 border-t border-secondary-200">
          <button
            type="submit"
            disabled={isLoading}
            className={`
              btn-primary px-8 py-3 font-semibold
              ${isLoading 
                ? 'opacity-50 cursor-not-allowed' 
                : 'hover:shadow-lg transform hover:-translate-y-0.5 transition-all duration-200'
              }
            `}
          >
            {isLoading ? (
              <span className="flex items-center">
                <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent mr-2" />
                Running Analysis...
              </span>
            ) : (
              <span className="flex items-center">
                <Building2 className="h-4 w-4 mr-2" />
                Analyze Lead
              </span>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default LeadForm;