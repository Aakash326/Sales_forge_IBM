#!/usr/bin/env python3
"""
IndustryRouter Test Suite

Comprehensive test suite for the IndustryRouter class including unit tests,
integration tests, and mock tests for scenarios where Supabase is unavailable.

Usage:
    python -m pytest tests/test_industry_router.py -v
    
    Or run directly:
    python tests/test_industry_router.py

Prerequisites:
    pip install pytest pytest-mock pytest-asyncio
"""

import sys
import os
import pytest
import time
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, List, Any

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

try:
    from src.agents.industry_router import IndustryRouter, create_industry_router, quick_query
except ImportError:
    pytest.skip("IndustryRouter not available", allow_module_level=True)


class TestIndustryRouter:
    """Test suite for IndustryRouter class"""
    
    @pytest.fixture
    def mock_supabase_client(self):
        """Create a mock Supabase client"""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.data = [
            {
                'id': 1,
                'company_name': 'Test Company',
                'industry': 'Technology',
                'location': 'San Francisco, CA',
                'performance_score': 95
            }
        ]
        
        # Setup mock chain: client.table().select().execute()
        mock_query = Mock()
        mock_query.execute.return_value = mock_response
        mock_query.ilike.return_value = mock_query
        mock_query.gte.return_value = mock_query
        mock_query.lte.return_value = mock_query
        mock_query.order.return_value = mock_query
        mock_query.limit.return_value = mock_query
        
        mock_table = Mock()
        mock_table.select.return_value = mock_query
        
        mock_client.table.return_value = mock_table
        
        return mock_client
    
    @pytest.fixture
    def router_with_mock(self, mock_supabase_client):
        """Create IndustryRouter with mock Supabase client"""
        with patch('src.agents.industry_router.create_client', return_value=mock_supabase_client):
            with patch.dict(os.environ, {
                'SUPABASE_URL': 'https://test.supabase.co',
                'SUPABASE_ANON_KEY': 'test-key'
            }):
                router = IndustryRouter()
                return router
    
    def test_initialization_with_env_vars(self):
        """Test IndustryRouter initialization with environment variables"""
        with patch.dict(os.environ, {
            'SUPABASE_URL': 'https://test.supabase.co',
            'SUPABASE_ANON_KEY': 'test-key'
        }):
            with patch('src.agents.industry_router.create_client') as mock_create:
                mock_create.return_value = Mock()
                router = IndustryRouter()
                
                assert router.supabase_url == 'https://test.supabase.co'
                assert router.supabase_key == 'test-key'
                assert len(router.supported_industries) == 3
                assert 'finance' in router.supported_industries
                assert 'healthcare' in router.supported_industries
                assert 'technology' in router.supported_industries
    
    def test_initialization_with_parameters(self):
        """Test IndustryRouter initialization with direct parameters"""
        with patch('src.agents.industry_router.create_client') as mock_create:
            mock_create.return_value = Mock()
            router = IndustryRouter(
                supabase_url='https://param.supabase.co',
                supabase_key='param-key'
            )
            
            assert router.supabase_url == 'https://param.supabase.co'
            assert router.supabase_key == 'param-key'
    
    def test_initialization_without_credentials(self):
        """Test IndustryRouter initialization fails without credentials"""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="Supabase credentials not found"):
                IndustryRouter()
    
    def test_detect_industry_explicit(self, router_with_mock):
        """Test industry detection with explicit industry field"""
        test_cases = [
            ({'industry': 'finance'}, 'finance'),
            ({'industry': 'healthcare'}, 'healthcare'),
            ({'industry': 'technology'}, 'technology'),
            ({'industry': 'fintech'}, 'finance'),
            ({'industry': 'biotech'}, 'healthcare'),
            ({'industry': 'tech'}, 'technology'),
        ]
        
        for input_data, expected in test_cases:
            result = router_with_mock.detect_industry(input_data)
            assert result == expected, f"Failed for input {input_data}"
    
    def test_detect_industry_company_name(self, router_with_mock):
        """Test industry detection based on company names"""
        test_cases = [
            ({'company_name': 'Goldman Sachs'}, 'finance'),
            ({'company_name': 'JPMorgan Chase'}, 'finance'),
            ({'company_name': 'Johnson & Johnson'}, 'healthcare'),
            ({'company_name': 'Pfizer Inc.'}, 'healthcare'),
            ({'company_name': 'Apple Inc.'}, 'technology'),
            ({'company_name': 'Microsoft Corporation'}, 'technology'),
        ]
        
        for input_data, expected in test_cases:
            result = router_with_mock.detect_industry(input_data)
            assert result == expected, f"Failed for input {input_data}"
    
    def test_detect_industry_query(self, router_with_mock):
        """Test industry detection based on query text"""
        test_cases = [
            ({'query': 'banking and financial services'}, 'finance'),
            ({'query': 'pharmaceutical research companies'}, 'healthcare'),
            ({'query': 'software development firms'}, 'technology'),
            ({'query': 'AI and machine learning platforms'}, 'technology'),
        ]
        
        for input_data, expected in test_cases:
            result = router_with_mock.detect_industry(input_data)
            assert result == expected, f"Failed for input {input_data}"
    
    def test_detect_industry_no_match(self, router_with_mock):
        """Test industry detection returns None for no matches"""
        test_cases = [
            {'company_name': 'Random Corp'},
            {'query': 'general business consulting'},
            {'industry': 'agriculture'},
            {}
        ]
        
        for input_data in test_cases:
            result = router_with_mock.detect_industry(input_data)
            assert result is None, f"Should return None for input {input_data}"
    
    def test_get_database_table(self, router_with_mock):
        """Test database table mapping"""
        test_cases = [
            ('finance', 'finance_companies'),
            ('healthcare', 'healthcare_companies'),
            ('technology', 'tech_companies'),
        ]
        
        for industry, expected_table in test_cases:
            result = router_with_mock.get_database_table(industry)
            assert result == expected_table
    
    def test_get_database_table_invalid_industry(self, router_with_mock):
        """Test database table mapping with invalid industry"""
        with pytest.raises(ValueError, match="Unsupported industry"):
            router_with_mock.get_database_table('invalid_industry')
    
    def test_build_query_params(self, router_with_mock):
        """Test query parameter building"""
        input_data = {
            'location': 'New York',
            'company_name': 'Test Corp',
            'min_performance': 80,
            'max_performance': 95,
            'sort_by': 'company_name',
            'sort_order': 'asc',
            'limit': 10
        }
        
        result = router_with_mock._build_query_params(input_data)
        
        assert result['location'] == 'New York'
        assert result['company_name'] == 'Test Corp'
        assert result['min_performance'] == 80
        assert result['max_performance'] == 95
        assert result['sort_by'] == 'company_name'
        assert result['sort_order'] == 'asc'
        assert result['limit'] == 10
    
    def test_fetch_data_from_table(self, router_with_mock):
        """Test data fetching from Supabase table"""
        query_params = {
            'location': 'CA',
            'min_performance': 90,
            'limit': 5
        }
        
        result = router_with_mock.fetch_data_from_table('tech_companies', query_params)
        
        assert isinstance(result, list)
        assert len(result) > 0
        assert result[0]['company_name'] == 'Test Company'
    
    def test_fetch_data_from_table_error(self, router_with_mock):
        """Test data fetching handles errors properly"""
        # Mock an error in the query execution
        router_with_mock.supabase_client.table.side_effect = Exception("Database error")
        
        with pytest.raises(Exception, match="Database query failed"):
            router_with_mock.fetch_data_from_table('tech_companies', {})
    
    def test_route_query_success(self, router_with_mock):
        """Test successful query routing"""
        input_data = {
            'company_name': 'Apple Inc.',
            'industry': 'technology',
            'location': 'CA'
        }
        
        result = router_with_mock.route_query(input_data)
        
        assert result['industry'] == 'technology'
        assert result['database_table'] == 'tech_companies'
        assert isinstance(result['results'], list)
        assert 'processing_time' in result
        assert 'query_metadata' in result
        assert 'error' not in result
    
    def test_route_query_no_industry_detected(self, router_with_mock):
        """Test query routing when no industry is detected"""
        input_data = {
            'company_name': 'Random Corp',
            'query': 'generic business'
        }
        
        result = router_with_mock.route_query(input_data)
        
        assert result['industry'] == 'unknown'
        assert result['database_table'] is None
        assert result['results'] == []
        assert 'error' in result
        assert result['error'] == 'Unable to detect industry'
    
    def test_route_query_invalid_input(self, router_with_mock):
        """Test query routing with invalid input"""
        invalid_inputs = [
            "not_a_dict",
            123,
            None,
            []
        ]
        
        for invalid_input in invalid_inputs:
            result = router_with_mock.route_query(invalid_input)
            assert result['industry'] == 'error'
            assert 'error' in result
    
    def test_statistics_tracking(self, router_with_mock):
        """Test query statistics tracking"""
        # Initial stats
        initial_stats = router_with_mock.get_statistics()
        assert initial_stats['total_queries'] == 0
        assert initial_stats['successful_queries'] == 0
        assert initial_stats['failed_queries'] == 0
        
        # Run some queries
        successful_input = {'industry': 'technology'}
        failed_input = 'invalid'
        
        router_with_mock.route_query(successful_input)
        router_with_mock.route_query(failed_input)
        
        final_stats = router_with_mock.get_statistics()
        assert final_stats['total_queries'] == 2
        assert final_stats['successful_queries'] == 1
        assert final_stats['failed_queries'] == 1
        assert final_stats['success_rate'] == 50.0
    
    def test_connection_test(self, router_with_mock):
        """Test connection testing functionality"""
        result = router_with_mock.test_connection()
        
        assert 'connected' in result
        assert 'timestamp' in result
        assert 'tables_status' in result
    
    def test_fuzzy_matching(self, router_with_mock):
        """Test fuzzy string matching"""
        test_cases = [
            ('apple', 'apple inc', True),
            ('microsoft', 'microsoft corporation', True),
            ('bank', 'banking services', True),
            ('xyz', 'completely different', False),
        ]
        
        for keyword, text, expected in test_cases:
            result = router_with_mock._fuzzy_match(keyword, text)
            assert result == expected
    
    def test_pattern_detection(self, router_with_mock):
        """Test regex pattern detection"""
        test_cases = [
            ('banking and financial services', 'finance'),
            ('pharmaceutical research', 'healthcare'),
            ('software development', 'technology'),
            ('random business text', None),
        ]
        
        for text, expected in test_cases:
            result = router_with_mock._detect_by_patterns(text)
            assert result == expected


class TestUtilityFunctions:
    """Test utility functions"""
    
    def test_create_industry_router(self):
        """Test factory function"""
        with patch('src.agents.industry_router.IndustryRouter') as mock_router:
            create_industry_router('test_url', 'test_key')
            mock_router.assert_called_once_with('test_url', 'test_key')
    
    def test_quick_query(self):
        """Test quick query utility function"""
        test_data = {'industry': 'technology'}
        
        with patch('src.agents.industry_router.IndustryRouter') as mock_router_class:
            mock_router = Mock()
            mock_router.route_query.return_value = {'industry': 'technology', 'results': []}
            mock_router_class.return_value = mock_router
            
            result = quick_query(test_data, 'test_url', 'test_key')
            
            mock_router_class.assert_called_once_with('test_url', 'test_key')
            mock_router.route_query.assert_called_once_with(test_data)
            assert result['industry'] == 'technology'


class TestIntegrationScenarios:
    """Integration test scenarios"""
    
    @pytest.fixture
    def integration_router(self):
        """Create router for integration tests (requires real Supabase)"""
        # Skip if no real credentials available
        if not (os.getenv('SUPABASE_URL') and os.getenv('SUPABASE_ANON_KEY')):
            pytest.skip("No Supabase credentials available for integration tests")
        
        try:
            return IndustryRouter()
        except Exception:
            pytest.skip("Cannot connect to Supabase for integration tests")
    
    def test_end_to_end_query(self, integration_router):
        """Test end-to-end query with real database"""
        input_data = {
            'industry': 'technology',
            'min_performance': 90,
            'limit': 3
        }
        
        result = integration_router.route_query(input_data)
        
        assert result['industry'] == 'technology'
        assert result['database_table'] == 'tech_companies'
        assert isinstance(result['results'], list)
        assert 'processing_time' in result
        
        # Verify processing time is reasonable
        processing_time = float(result['processing_time'].rstrip('s'))
        assert processing_time < 5.0  # Should complete within 5 seconds
    
    def test_real_connection_test(self, integration_router):
        """Test connection with real Supabase instance"""
        result = integration_router.test_connection()
        
        assert result['connected'] is True
        assert len(result['tables_status']) == 3
        
        for table, status in result['tables_status'].items():
            assert table in ['finance_companies', 'healthcare_companies', 'tech_companies']
            assert 'accessible' in status


class TestPerformance:
    """Performance-related tests"""
    
    def test_query_performance(self, router_with_mock):
        """Test query performance is within acceptable limits"""
        input_data = {'industry': 'technology'}
        
        start_time = time.time()
        result = router_with_mock.route_query(input_data)
        end_time = time.time()
        
        execution_time = end_time - start_time
        assert execution_time < 1.0  # Should complete within 1 second
        
        # Verify reported time is accurate
        reported_time = float(result['processing_time'].rstrip('s'))
        assert abs(reported_time - execution_time) < 0.1  # Within 100ms tolerance
    
    def test_batch_query_performance(self, router_with_mock):
        """Test performance with multiple queries"""
        queries = [
            {'industry': 'finance'},
            {'industry': 'healthcare'},
            {'industry': 'technology'},
        ] * 10  # 30 queries total
        
        start_time = time.time()
        results = [router_with_mock.route_query(query) for query in queries]
        end_time = time.time()
        
        total_time = end_time - start_time
        assert total_time < 5.0  # All 30 queries within 5 seconds
        assert len(results) == 30
        assert all(r['industry'] != 'error' for r in results)


def run_tests():
    """Run tests when script is executed directly"""
    import subprocess
    import sys
    
    # Try to run with pytest
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pytest', __file__, '-v', '--tb=short'
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        return result.returncode == 0
        
    except FileNotFoundError:
        print("pytest not found. Install with: pip install pytest pytest-mock")
        return False


if __name__ == "__main__":
    print("🧪 IndustryRouter Test Suite")
    print("=" * 50)
    
    success = run_tests()
    
    if success:
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed. Check output above.")
        sys.exit(1)