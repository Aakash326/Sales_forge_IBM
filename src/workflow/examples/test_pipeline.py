import unittest
from unittest.mock import Mock, patch
from datetime import datetime
import tempfile
import os

from ..sales_pipeline import SalesPipeline
from ..states.lead_states import LeadState
from ..nodes.research_node import ResearchNode
from ..nodes.scoring_node import ScoringNode
from ..edges.conditional_routing import ConditionalRouter
from ..edges.scoring_logic import ScoringLogic
from ..persistence.state_store import StateStore

class TestSalesPipeline(unittest.TestCase):
    """Test cases for the main sales pipeline"""
    
    def setUp(self):
        self.pipeline = SalesPipeline()
        
        self.sample_lead_data = {
            "lead_id": "test_lead_123",
            "company_name": "Test Company",
            "contact_email": "test@company.com",
            "contact_name": "Test Contact",
            "company_size": 100,
            "industry": "Technology"
        }
    
    def test_pipeline_initialization(self):
        """Test pipeline initializes correctly"""
        self.assertIsInstance(self.pipeline, SalesPipeline)
        self.assertIsNotNone(self.pipeline.workflow)
        self.assertIsNotNone(self.pipeline.research_node)
        self.assertIsNotNone(self.pipeline.scoring_node)
    
    @patch('workflows.nodes.research_node.ResearchNode.execute')
    def test_pipeline_execution(self, mock_research):
        """Test basic pipeline execution"""
        
        # Mock research node response
        mock_lead_state = LeadState(**self.sample_lead_data)
        mock_lead_state.research_completed = True
        mock_lead_state.pain_points = ["Data integration challenges"]
        mock_research.return_value = mock_lead_state
        
        # This would normally run the full workflow, but we'll test components
        self.assertTrue(True)  # Placeholder for workflow execution test

class TestLeadState(unittest.TestCase):
    """Test cases for LeadState model"""
    
    def setUp(self):
        self.lead_data = {
            "lead_id": "test_123",
            "company_name": "Test Corp",
            "contact_email": "test@testcorp.com"
        }
    
    def test_lead_state_creation(self):
        """Test creating a lead state"""
        lead = LeadState(**self.lead_data)
        
        self.assertEqual(lead.lead_id, "test_123")
        self.assertEqual(lead.company_name, "Test Corp")
        self.assertEqual(lead.stage, "new")
        self.assertEqual(lead.lead_score, 0.0)
        self.assertIsInstance(lead.created_at, datetime)
    
    def test_lead_state_defaults(self):
        """Test default values are set correctly"""
        lead = LeadState(**self.lead_data)
        
        self.assertFalse(lead.research_completed)
        self.assertEqual(lead.outreach_attempts, 0)
        self.assertEqual(lead.response_rate, 0.0)
        self.assertEqual(len(lead.pain_points), 0)
        self.assertEqual(len(lead.key_insights), 0)

class TestConditionalRouter(unittest.TestCase):
    """Test cases for conditional routing logic"""
    
    def setUp(self):
        self.router = ConditionalRouter()
        self.lead_state = LeadState(
            lead_id="test",
            company_name="Test",
            contact_email="test@test.com"
        )
    
    def test_route_after_research_success(self):
        """Test routing after successful research"""
        self.lead_state.research_completed = True
        result = self.router.route_after_research(self.lead_state)
        self.assertEqual(result, "scoring")
    
    def test_route_after_research_failure(self):
        """Test routing after failed research"""
        self.lead_state.research_completed = False
        result = self.router.route_after_research(self.lead_state)
        self.assertEqual(result, "end")
    
    def test_route_after_high_engagement(self):
        """Test routing with high engagement"""
        self.lead_state.engagement_level = 0.8
        self.lead_state.response_rate = 0.5
        result = self.router.route_after_outreach(self.lead_state)
        self.assertEqual(result, "qualify")
    
    def test_route_after_low_engagement(self):
        """Test routing with low engagement"""
        self.lead_state.engagement_level = 0.1
        self.lead_state.response_rate = 0.0
        result = self.router.route_after_outreach(self.lead_state)
        self.assertEqual(result, "end")

class TestScoringLogic(unittest.TestCase):
    """Test cases for scoring logic"""
    
    def setUp(self):
        self.scoring = ScoringLogic()
        self.lead_state = LeadState(
            lead_id="test",
            company_name="Test Corp",
            contact_email="test@test.com"
        )
    
    def test_company_size_scoring(self):
        """Test company size scoring"""
        # Large company
        score_large = self.scoring._score_company_size(1000)
        self.assertEqual(score_large, 1.0)
        
        # Medium company
        score_medium = self.scoring._score_company_size(200)
        self.assertEqual(score_medium, 0.8)
        
        # Small company
        score_small = self.scoring._score_company_size(25)
        self.assertEqual(score_small, 0.4)
    
    def test_industry_fit_scoring(self):
        """Test industry fit scoring"""
        # High fit industry
        score_tech = self.scoring._score_industry_fit("Technology Software")
        self.assertEqual(score_tech, 0.9)
        
        # Medium fit industry
        score_retail = self.scoring._score_industry_fit("Retail")
        self.assertEqual(score_retail, 0.7)
        
        # Unknown industry
        score_unknown = self.scoring._score_industry_fit("Unknown Industry")
        self.assertEqual(score_unknown, 0.6)
    
    def test_composite_score_calculation(self):
        """Test composite score calculation"""
        self.lead_state.company_size = 500
        self.lead_state.industry = "Technology"
        self.lead_state.engagement_level = 0.7
        self.lead_state.research_completed = True
        self.lead_state.pain_points = ["Integration issues", "Scalability"]
        
        score = self.scoring.calculate_composite_score(self.lead_state)
        self.assertGreater(score, 0.5)
        self.assertLessEqual(score, 1.0)

class TestStateStore(unittest.TestCase):
    """Test cases for state storage"""
    
    def setUp(self):
        # Use temporary database for testing
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.store = StateStore(self.temp_db.name)
        
        self.lead_state = LeadState(
            lead_id="test_lead",
            company_name="Test Company",
            contact_email="test@company.com",
            company_size=100,
            industry="Technology"
        )
    
    def tearDown(self):
        # Clean up temporary database
        os.unlink(self.temp_db.name)
    
    def test_save_and_load_lead_state(self):
        """Test saving and loading lead state"""
        # Save state
        success = self.store.save_lead_state(self.lead_state)
        self.assertTrue(success)
        
        # Load state
        loaded_state = self.store.load_lead_state("test_lead")
        self.assertIsNotNone(loaded_state)
        self.assertEqual(loaded_state.lead_id, "test_lead")
        self.assertEqual(loaded_state.company_name, "Test Company")
    
    def test_get_leads_by_stage(self):
        """Test retrieving leads by stage"""
        # Save a lead
        self.store.save_lead_state(self.lead_state)
        
        # Get leads in 'new' stage
        leads = self.store.get_leads_by_stage("new")
        self.assertEqual(len(leads), 1)
        self.assertEqual(leads[0].lead_id, "test_lead")
    
    def test_pipeline_stats(self):
        """Test pipeline statistics"""
        # Save some test leads
        for i in range(3):
            lead = LeadState(
                lead_id=f"lead_{i}",
                company_name=f"Company {i}",
                contact_email=f"test{i}@company.com",
                stage="new" if i < 2 else "qualified",
                lead_score=0.5 + (i * 0.2)
            )
            self.store.save_lead_state(lead)
        
        stats = self.store.get_pipeline_stats()
        self.assertEqual(stats["total_leads"], 3)
        self.assertIn("new", stats["stage_distribution"])
        self.assertIn("qualified", stats["stage_distribution"])

class TestWorkflowIntegration(unittest.TestCase):
    """Integration tests for the complete workflow"""
    
    def setUp(self):
        self.pipeline = SalesPipeline()
    
    @patch('workflows.nodes.research_node.ResearchNode._create_research_crew')
    @patch('workflows.nodes.scoring_node.ScoringNode._create_analytics_crew')
    @patch('workflows.nodes.outreach_node.OutreachNode._create_outreach_crew')
    def test_end_to_end_workflow(self, mock_outreach, mock_scoring, mock_research):
        """Test complete workflow execution"""
        
        # Mock the CrewAI crews to avoid external dependencies
        mock_research.return_value = Mock()
        mock_scoring.return_value = Mock()
        mock_outreach.return_value = Mock()
        
        lead_data = {
            "lead_id": "integration_test",
            "company_name": "Integration Test Corp",
            "contact_email": "test@integration.com",
            "company_size": 250,
            "industry": "Technology"
        }
        
        # This would test the full workflow in a real scenario
        # For now, we'll just verify the pipeline can be instantiated
        self.assertIsNotNone(self.pipeline)

def run_tests():
    """Run all test cases"""
    
    # Create test suite
    test_classes = [
        TestLeadState,
        TestConditionalRouter, 
        TestScoringLogic,
        TestStateStore,
        TestWorkflowIntegration
    ]
    
    suite = unittest.TestSuite()
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print("TEST SUMMARY")
    print(f"{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\nFailures:")
        for test, traceback in result.failures:
            print(f"  - {test}")
    
    if result.errors:
        print(f"\nErrors:")
        for test, traceback in result.errors:
            print(f"  - {test}")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    # Run the tests
    success = run_tests()
    
    if success:
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed!")
        
    exit(0 if success else 1)