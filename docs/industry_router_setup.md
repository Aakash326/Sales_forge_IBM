# IndustryRouter - Supabase Integration Setup Guide

This guide provides complete setup instructions for the IndustryRouter system with Supabase integration.

## 🎯 Overview

The IndustryRouter is an intelligent system that:
- Detects company industry from input data
- Routes queries to appropriate Supabase database tables
- Provides comprehensive filtering and search capabilities
- Tracks performance metrics and statistics

## 📋 Prerequisites

- Python 3.8+ installed
- Supabase account and project
- Basic knowledge of SQL and Python

## 🚀 Quick Start

### 1. Create Supabase Project

1. Go to [Supabase](https://supabase.com) and create an account
2. Create a new project
3. Wait for the project to be fully initialized
4. Go to Settings → API to get your credentials

### 2. Database Setup

Run the SQL commands from `database/supabase_setup.sql` in your Supabase SQL editor:

```sql
-- Run this in Supabase Dashboard → SQL Editor
-- Copy and paste the contents of database/supabase_setup.sql
```

This will create:
- `finance_companies` table with sample financial companies
- `healthcare_companies` table with sample healthcare companies  
- `tech_companies` table with sample technology companies
- Proper indexes, constraints, and sample data

### 3. Environment Configuration

1. Copy the environment template:
```bash
cp .env.example .env
```

2. Edit `.env` with your Supabase credentials:
```env
SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_ANON_KEY=your_anon_key_here
```

### 4. Install Dependencies

```bash
pip install -r requirements_supabase.txt
```

### 5. Test the Installation

```python
from src.agents.industry_router import IndustryRouter

# Test connection
router = IndustryRouter()
status = router.test_connection()
print("Connection Status:", status['connected'])
```

## 📖 Usage Guide

### Basic Usage

```python
from src.agents.industry_router import IndustryRouter

# Initialize router
router = IndustryRouter()

# Query example
input_data = {
    "company_name": "FinTech Corp",
    "industry": "Finance", 
    "query": "What are the top-performing finance companies in NY?"
}

result = router.route_query(input_data)
print(f"Industry: {result['industry']}")
print(f"Results: {len(result['results'])}")
```

### Advanced Filtering

```python
# Advanced query with filters
input_data = {
    "industry": "technology",
    "location": "California",
    "min_performance": 90,
    "max_performance": 98,
    "sort_by": "performance_score",
    "sort_order": "desc",
    "limit": 10
}

result = router.route_query(input_data)
```

### Industry Detection

The router can automatically detect industry from:

1. **Explicit industry field**: `{"industry": "fintech"}`
2. **Company names**: `{"company_name": "Goldman Sachs"}`
3. **Query text**: `{"query": "banking services"}`
4. **Combined analysis**: Multiple fields together

### Utility Functions

```python
from src.agents.industry_router import create_industry_router, quick_query

# Factory function
router = create_industry_router()

# Quick one-off query
result = quick_query({"company_name": "Apple Inc."})
```

## 🏗️ Architecture

### Industry Mappings

- **Finance**: Banks, fintech, investment, trading
- **Healthcare**: Pharmaceutical, biotech, medical devices
- **Technology**: Software, hardware, AI, cloud services

### Database Tables

- `finance_companies`: Financial sector companies
- `healthcare_companies`: Healthcare sector companies
- `tech_companies`: Technology sector companies

Each table contains:
- `id`: Primary key
- `company_name`: Company name
- `industry`: Industry category
- `location`: Company location
- `performance_score`: Performance rating (0-100)
- `created_at`, `updated_at`: Timestamps

## 🔧 Configuration Options

### Environment Variables

```env
# Required
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key

# Optional
LOG_LEVEL=INFO
```

### Router Parameters

```python
router = IndustryRouter(
    supabase_url="custom_url",  # Override env var
    supabase_key="custom_key"   # Override env var
)
```

### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `company_name` | str | Company name to search |
| `industry` | str | Industry category |
| `query` | str | Search query text |
| `location` | str | Location filter |
| `min_performance` | int | Minimum performance score |
| `max_performance` | int | Maximum performance score |
| `sort_by` | str | Sort field (default: performance_score) |
| `sort_order` | str | Sort direction (asc/desc) |
| `limit` | int | Maximum results (default: 50, max: 100) |

## 📊 Response Format

```python
{
    "industry": "technology",
    "database_table": "tech_companies",
    "results": [
        {
            "id": 1,
            "company_name": "Apple Inc.",
            "industry": "Technology",
            "location": "Cupertino, CA", 
            "performance_score": 98,
            "created_at": "2025-01-09T...",
            "updated_at": "2025-01-09T..."
        }
    ],
    "processing_time": "0.245s",
    "query_metadata": {
        "total_results": 1,
        "query_params": {...},
        "timestamp": "2025-01-09T..."
    }
}
```

## 🧪 Testing

### Run Examples
```bash
python examples/industry_router_examples.py
```

### Run Test Suite
```bash
python -m pytest tests/test_industry_router.py -v
```

### Manual Testing
```python
# Test industry detection
router = IndustryRouter()
industry = router.detect_industry({"company_name": "Microsoft"})
print(industry)  # Should output: technology

# Test connection
status = router.test_connection()
print(status)
```

## 📈 Performance Monitoring

### Get Statistics
```python
stats = router.get_statistics()
print(f"Success Rate: {stats['success_rate']:.1f}%")
print(f"Average Response Time: {stats['average_response_time_seconds']}s")
```

### Performance Tips

1. **Use specific filters**: More specific queries are faster
2. **Limit results**: Use `limit` parameter to control result size
3. **Cache router instance**: Reuse router instances when possible
4. **Monitor statistics**: Track performance over time

## 🛠️ Troubleshooting

### Common Issues

1. **Connection Failed**
   - Check SUPABASE_URL and SUPABASE_ANON_KEY
   - Verify project is active in Supabase dashboard
   - Test internet connection

2. **No Industry Detected**
   - Check input data has detectable keywords
   - Try explicit `industry` field
   - Review supported industries list

3. **Empty Results**
   - Verify database has sample data
   - Check filter parameters aren't too restrictive
   - Test with broader queries

4. **Import Errors**
   - Install dependencies: `pip install -r requirements_supabase.txt`
   - Check Python path configuration
   - Verify file structure

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

router = IndustryRouter()
# Detailed logging will show detection process
```

## 🔐 Security Considerations

### Row Level Security (RLS)

The database setup includes RLS policies. For production:

1. **Custom Policies**: Create specific policies for your use case
2. **Service Role**: Use service role key for admin operations
3. **API Keys**: Rotate keys regularly
4. **Network Security**: Use VPC/firewall rules as needed

### Data Privacy

- Input data is not stored by default
- Query statistics are stored in memory only
- Consider logging policies for sensitive data

## 🚀 Production Deployment

### Environment Setup
```bash
# Production environment
export SUPABASE_URL="https://prod-project.supabase.co"
export SUPABASE_ANON_KEY="prod-anon-key"
export LOG_LEVEL="WARNING"
```

### Performance Tuning

1. **Connection Pooling**: Use connection pooling for high traffic
2. **Caching**: Implement Redis/Memcached for frequent queries
3. **Load Balancing**: Distribute requests across multiple instances
4. **Database Optimization**: Add indexes for common query patterns

### Monitoring

1. **Metrics**: Track query volume, response times, error rates
2. **Alerts**: Set up alerts for high error rates or slow responses
3. **Logging**: Implement structured logging with correlation IDs
4. **Health Checks**: Regular connection and functionality tests

## 📚 API Reference

### IndustryRouter Class

#### Methods

- `route_query(input_data: Dict) -> Dict`: Main routing method
- `detect_industry(input_data: Dict) -> Optional[str]`: Industry detection
- `get_database_table(industry: str) -> str`: Get table name for industry
- `fetch_data_from_table(table: str, query_params: Dict) -> List[Dict]`: Fetch data
- `get_statistics() -> Dict`: Get performance statistics
- `test_connection() -> Dict`: Test Supabase connection

#### Properties

- `supported_industries`: List of supported industries
- `industry_mappings`: Industry to table mappings

### Utility Functions

- `create_industry_router(url?, key?) -> IndustryRouter`: Factory function
- `quick_query(input_data, url?, key?) -> Dict`: Quick query utility

## 🤝 Contributing

### Adding New Industries

1. Update `industry_mappings` in `IndustryRouter.__init__()`
2. Create corresponding Supabase table
3. Add test cases
4. Update documentation

### Extending Functionality

1. Follow existing code patterns
2. Add comprehensive tests
3. Update documentation
4. Submit pull request

## 📝 License & Support

This code is provided as-is for integration with the Sales_forge project.

For support:
1. Check this documentation
2. Review test cases and examples
3. Check Supabase documentation
4. Create GitHub issue if needed

---

**Next Steps**: Try the examples, run tests, and integrate into your application!