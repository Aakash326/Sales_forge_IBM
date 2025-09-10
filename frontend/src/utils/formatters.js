// Utility functions for formatting data

export const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount);
};

export const formatNumber = (number) => {
  return new Intl.NumberFormat('en-US').format(number);
};

export const formatPercentage = (decimal, decimals = 1) => {
  return `${(decimal * 100).toFixed(decimals)}%`;
};

export const formatDuration = (seconds) => {
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);
  
  if (hours > 0) {
    const remainingMinutes = minutes % 60;
    return `${hours}h ${remainingMinutes}m`;
  } else if (minutes > 0) {
    const remainingSeconds = Math.floor(seconds % 60);
    return `${minutes}m ${remainingSeconds}s`;
  } else {
    return `${Math.floor(seconds)}s`;
  }
};

export const formatTimestamp = (isoString) => {
  return new Date(isoString).toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  });
};

export const getStatusColor = (status) => {
  const statusColors = {
    'completed': 'success',
    'running': 'warning',
    'pending': 'warning',
    'failed': 'error',
    'pending_user_approval': 'warning',
  };
  return statusColors[status] || 'secondary';
};

export const getWorkflowIcon = (workflowName) => {
  const iconMap = {
    'Advanced': '🚀',
    'Intermediate': '⚡',
    'Basic': '💨',
    'Enhanced': '🤖',
  };
  
  const name = workflowName.split(' ')[0]; // Get first word
  return iconMap[name] || '🔧';
};

export const truncateText = (text, maxLength = 100) => {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
};