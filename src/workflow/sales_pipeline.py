from typing import Dict, Any, List
import sys
import os

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from src.workflow.states.lead_states import LeadState
from src.workflow.nodes.research_node import ResearchNode
from src.workflow.nodes.outreach_node import OutreachNode
from src.workflow.nodes.scoring_node import ScoringNode
from src.workflow.nodes.simulation_node import SimulationNode
from src.workflow.edges.conditional_routing import ConditionalRouter
from src.workflow.edges.scoring_logic import ScoringLogic
from src.workflow.persistence.state_store import StateStore
from src.workflow.persistence.checkpoints import CheckpointManager

# Handle optional dependencies
try:
    from langgraph.graph import StateGraph, END
    HAS_LANGGRAPH = True
except ImportError:
    HAS_LANGGRAPH = False
    StateGraph = None
    END = None

try:
    from langgraph.checkpoint.sqlite import SqliteSaver
except ImportError:
    try:
        from langgraph.checkpoint import SqliteSaver
    except ImportError:
        SqliteSaver = None

try:
    from langchain_core.runnables import RunnableLambda
    HAS_LANGCHAIN_CORE = True
except ImportError:
    HAS_LANGCHAIN_CORE = False
    RunnableLambda = None

class SalesPipeline:
    """
    Main sales pipeline workflow orchestrator using LangGraph
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.state_store = StateStore()
        self.checkpoint_manager = CheckpointManager()
        
        # Initialize nodes
        self.research_node = ResearchNode()
        self.outreach_node = OutreachNode()
        self.scoring_node = ScoringNode()
        self.simulation_node = SimulationNode()
        
        # Initialize routing logic
        self.router = ConditionalRouter()
        self.scoring_logic = ScoringLogic()
        
        # Build the workflow graph
        if HAS_LANGGRAPH:
            self.workflow = self._build_workflow()
        else:
            self.workflow = None
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow"""
        
        # Create the state graph
        workflow = StateGraph(LeadState)
        
        # Add nodes
        workflow.add_node("research", self.research_node.execute)
        workflow.add_node("scoring", self.scoring_node.execute)
        workflow.add_node("outreach", self.outreach_node.execute)
        workflow.add_node("simulation", self.simulation_node.execute)
        workflow.add_node("qualify", self._qualify_lead)
        workflow.add_node("handoff", self._handoff_to_sales)
        
        # Set entry point
        workflow.set_entry_point("research")
        
        # Add conditional edges
        workflow.add_conditional_edges(
            "research",
            self.router.route_after_research,
            {
                "scoring": "scoring",
                "end": END
            }
        )
        
        workflow.add_conditional_edges(
            "scoring", 
            self.scoring_logic.evaluate_score,
            {
                "outreach": "outreach",
                "simulation": "simulation",
                "end": END
            }
        )
        
        workflow.add_conditional_edges(
            "outreach",
            self.router.route_after_outreach,
            {
                "qualify": "qualify",
                "simulation": "simulation",
                "end": END
            }
        )
        
        workflow.add_conditional_edges(
            "simulation",
            self.router.route_after_simulation,
            {
                "qualify": "qualify",
                "outreach": "outreach",
                "end": END
            }
        )
        
        workflow.add_conditional_edges(
            "qualify",
            self.router.route_after_qualification,
            {
                "handoff": "handoff",
                "outreach": "outreach",
                "end": END
            }
        )
        
        workflow.add_edge("handoff", END)
        
        return workflow
    
    def _qualify_lead(self, state: LeadState) -> LeadState:
        """Qualify the lead based on interactions"""
        # Lead qualification logic
        state.qualification_score = self._calculate_qualification_score(state)
        state.stage = "qualified" if state.qualification_score > 0.7 else "nurturing"
        return state
    
    def _handoff_to_sales(self, state: LeadState) -> LeadState:
        """Hand off qualified lead to sales team"""
        state.stage = "sales_handoff"
        state.assigned_rep = self._assign_sales_rep(state)
        return state
    
    def _calculate_qualification_score(self, state: LeadState) -> float:
        """Calculate lead qualification score"""
        # Implement scoring logic based on engagement, company size, etc.
        score = 0.0
        
        if state.engagement_level > 0.6:
            score += 0.3
        if state.company_size and state.company_size > 100:
            score += 0.2
        if state.pain_points:
            score += 0.3
        if state.response_rate > 0.5:
            score += 0.2
            
        return min(score, 1.0)
    
    def _assign_sales_rep(self, state: LeadState) -> str:
        """Assign appropriate sales rep based on lead characteristics"""
        # Simple assignment logic - can be enhanced
        if state.company_size and state.company_size > 1000:
            return "enterprise_rep"
        elif state.company_size and state.company_size > 100:
            return "mid_market_rep"
        else:
            return "smb_rep"
    
    def run(self, initial_state: Dict[str, Any]) -> Dict[str, Any]:
        """Run the sales pipeline workflow"""
        
        # Convert dict to LeadState
        lead_state = LeadState(**initial_state)
        
        if not HAS_LANGGRAPH or not self.workflow:
            # Fallback execution when LangGraph is not available
            print(f"LangGraph not available, using sequential execution for {lead_state.company_name}")
            return self._run_sequential_pipeline(lead_state)
        
        # Create compiled workflow with checkpoints
        if SqliteSaver:
            checkpointer = SqliteSaver.from_conn_string(":memory:")
            compiled_workflow = self.workflow.compile(checkpointer=checkpointer)
        else:
            compiled_workflow = self.workflow.compile()
        
        # Execute workflow
        config = {"configurable": {"thread_id": lead_state.lead_id}}
        result = compiled_workflow.invoke(lead_state.dict(), config=config)
        
        return result
    
    def _run_sequential_pipeline(self, lead_state: LeadState) -> Dict[str, Any]:
        """Run pipeline sequentially without LangGraph"""
        
        print("Running pipeline in sequential mode...")
        
        # Step 1: Research
        print("1. Executing research...")
        lead_state = self.research_node.execute(lead_state)
        
        # Check if research was successful
        if not lead_state.research_completed:
            print("Research failed, ending pipeline")
            return lead_state.dict()
        
        # Step 2: Scoring
        print("2. Executing scoring...")
        lead_state = self.scoring_node.execute(lead_state)
        
        # Step 3: Outreach (based on score)
        if lead_state.lead_score > 0.4:
            print("3. Executing outreach...")
            lead_state = self.outreach_node.execute(lead_state)
            
            # Step 4: Simulation (if engagement is good)
            if lead_state.engagement_level > 0.5:
                print("4. Executing simulation...")
                lead_state = self.simulation_node.execute(lead_state)
                
                # Step 5: Qualification
                if lead_state.predicted_conversion > 0.6:
                    print("5. Qualifying lead...")
                    lead_state = self._qualify_lead(lead_state)
                    
                    # Step 6: Handoff if qualified
                    if lead_state.qualification_score > 0.7:
                        print("6. Handing off to sales...")
                        lead_state = self._handoff_to_sales(lead_state)
        
        print(f"Pipeline completed for {lead_state.company_name}")
        return lead_state.dict()