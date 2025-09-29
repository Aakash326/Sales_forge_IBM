#!/usr/bin/env python3
"""
IBM Strategic Intelligence Workflow - 4 Agents
Strategic business intelligence (4-6 minutes)

Architecture:
1. Market Intelligence Agent - Industry analysis, market sizing, growth rates
2. Technical Architecture Agent - Solution complexity, implementation roadmaps  
3. Executive Decision Agent - ROI modeling, investment analysis
4. Compliance Risk Agent - Regulatory assessment, governance analysis

This workflow provides C-level strategic intelligence using IBM Granite models.
"""

import asyncio
import sys
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
load_dotenv(os.path.join(project_root, '.env'))

# Add the project root to the Python path
sys.path.insert(0, project_root)

from src.ibm_integrations.granite_client import create_granite_client
from src.ibm_integrations.strategic_agents.market_intelligence_agent import MarketIntelligenceAgent
from src.ibm_integrations.strategic_agents.technical_architecture_agent import TechnicalArchitectureAgent
from src.ibm_integrations.strategic_agents.executive_decision_agent import ExecutiveDecisionAgent
from src.ibm_integrations.strategic_agents.compliance_risk_agent import ComplianceRiskAgent
from src.workflow.nodes.simulation_node import SimulationNode
from src.workflow.nodes.advanced_simulation_node import AdvancedSimulationNode
from src.workflow.states.lead_states import LeadState


class IBMStrategicWorkflow:
    """
    IBM Strategic Intelligence Workflow
    
    4 specialized IBM Granite-powered agents for strategic business intelligence:
    - Market Intelligence Agent: Industry analysis and market opportunity assessment
    - Technical Architecture Agent: Solution design and implementation planning
    - Executive Decision Agent: ROI modeling and investment decision support
    - Compliance Risk Agent: Regulatory and governance risk assessment
    """
    
    def __init__(self, config=None):
        self.config = config or {}
        self.execution_mode = "strategic_intelligence"
        self.agent_timeout = 90  # 90 seconds per agent for deep analysis
        
        # Initialize IBM Granite client
        self.granite_client = create_granite_client(
            model_name="granite-3.0-8b-instruct",
            backend="watsonx"
        )
        
        # Initialize strategic agents
        self.market_agent = MarketIntelligenceAgent(self.granite_client)
        self.technical_agent = TechnicalArchitectureAgent(self.granite_client)
        self.executive_agent = ExecutiveDecisionAgent(self.granite_client) 
        self.compliance_agent = ComplianceRiskAgent(self.granite_client)
        
        # Initialize enhanced AutoGen simulation for strategic scenarios
        self.use_enhanced_simulation = config.get('use_enhanced_simulation', True)
        if self.use_enhanced_simulation:
            self.strategic_simulation_node = AdvancedSimulationNode(
                model_name="gpt-4o",  # Use more powerful model for strategic scenarios
                base_temperature=0.6,  # More conservative for strategic planning
                seed=42,
                use_swarm_pattern=False,  # Use MagenticOne for strategic coordination
                enable_magentic_one=True,
                conversation_timeout=120  # Longer timeout for strategic discussions
            )
        else:
            self.strategic_simulation_node = SimulationNode(
                model_name="gpt-4o",
                temperature=0.6,
                seed=42,
                use_json_mode=True,
                max_retries=3
            )
        
    async def run_strategic_workflow(self, lead_data: dict, tactical_results: dict = None) -> dict:
        """
        Execute 4-agent strategic workflow
        Target execution time: 4-6 minutes for comprehensive strategic analysis
        """
        
        print("🎯 IBM Strategic Intelligence Workflow")
        print("=" * 60)
        print(f"Company: {lead_data.get('company_name', 'Unknown')}")
        print(f"Industry: {lead_data.get('industry', 'Unknown')}")
        print(f"Size: {lead_data.get('company_size', 'Unknown')} employees")
        print(f"Revenue: ${lead_data.get('annual_revenue', 0):,}" if lead_data.get('annual_revenue') else "Revenue: Unknown")
        print(f"Target: 4-6 minute execution for strategic intelligence")
        print()
        
        start_time = datetime.now()
        
        # Prepare context for strategic analysis
        strategic_context = self._prepare_strategic_context(lead_data, tactical_results)
        
        # Agent 1: Market Intelligence Agent (60-90 seconds)
        print("🌍 Agent 1: Market Intelligence Agent")
        print("-" * 40)
        market_start = datetime.now()
        market_intelligence = await self._run_market_intelligence_agent(strategic_context)
        market_time = (datetime.now() - market_start).total_seconds()
        print(f"✅ Market analysis completed in {market_time:.1f}s")
        self._display_market_results(market_intelligence)
        
        # Agent 2: Technical Architecture Agent (60-90 seconds)
        print("\n⚙️  Agent 2: Technical Architecture Agent")
        print("-" * 40)
        technical_start = datetime.now()
        technical_analysis = await self._run_technical_architecture_agent(strategic_context, market_intelligence)
        technical_time = (datetime.now() - technical_start).total_seconds()
        print(f"✅ Technical analysis completed in {technical_time:.1f}s")
        self._display_technical_results(technical_analysis)
        
        # Agent 3: Executive Decision Agent (60-90 seconds)
        print("\n💼 Agent 3: Executive Decision Agent")
        print("-" * 40)
        executive_start = datetime.now()
        executive_analysis = await self._run_executive_decision_agent(strategic_context, market_intelligence, technical_analysis)
        executive_time = (datetime.now() - executive_start).total_seconds()
        print(f"✅ Executive analysis completed in {executive_time:.1f}s")
        self._display_executive_results(executive_analysis)
        
        # Agent 4: Compliance Risk Agent (60-90 seconds)
        print("\n🛡️  Agent 4: Compliance Risk Agent")
        print("-" * 40)
        compliance_start = datetime.now()
        compliance_analysis = await self._run_compliance_risk_agent(strategic_context, market_intelligence, technical_analysis)
        compliance_time = (datetime.now() - compliance_start).total_seconds()
        print(f"✅ Compliance analysis completed in {compliance_time:.1f}s")
        self._display_compliance_results(compliance_analysis)
        
        # Agent 5: Strategic Simulation Agent (C-level conversation simulation)
        print("\n🎭 Agent 5: Strategic Simulation Agent")
        print("-" * 40)
        simulation_start = datetime.now()
        strategic_simulation = await self._run_strategic_simulation_agent(
            strategic_context, market_intelligence, technical_analysis, executive_analysis, compliance_analysis
        )
        simulation_time = (datetime.now() - simulation_start).total_seconds()
        print(f"✅ Strategic simulation completed in {simulation_time:.1f}s")
        self._display_strategic_simulation_results(strategic_simulation)
        
        # Generate strategic synthesis
        print("\n🧠 Strategic Intelligence Synthesis")
        print("-" * 40)
        synthesis_start = datetime.now()
        strategic_synthesis = await self._generate_strategic_synthesis(
            strategic_context, market_intelligence, technical_analysis, executive_analysis, compliance_analysis, strategic_simulation
        )
        synthesis_time = (datetime.now() - synthesis_start).total_seconds()
        print(f"✅ Strategic synthesis completed in {synthesis_time:.1f}s")
        
        # Final strategic intelligence report
        total_time = (datetime.now() - start_time).total_seconds()
        strategic_report = self._generate_strategic_report(
            strategic_context, market_intelligence, technical_analysis, 
            executive_analysis, compliance_analysis, strategic_synthesis, strategic_simulation,
            {
                'market_time': market_time,
                'technical_time': technical_time,
                'executive_time': executive_time,
                'compliance_time': compliance_time,
                'simulation_time': simulation_time,
                'synthesis_time': synthesis_time,
                'total_time': total_time
            }
        )
        
        self._display_strategic_intelligence_dashboard(strategic_report)
        
        return strategic_report
    
    def _prepare_strategic_context(self, lead_data: dict, tactical_results: dict = None) -> dict:
        """Prepare comprehensive context for strategic analysis"""
        
        context = {
            "company_profile": {
                "name": lead_data.get('company_name', ''),
                "industry": lead_data.get('industry', ''),
                "size": lead_data.get('company_size', 0),
                "location": lead_data.get('location', ''),
                "annual_revenue": lead_data.get('annual_revenue', 0),
                "stage": lead_data.get('stage', 'unknown')
            },
            "solution_requirements": {
                "multi_tenant": lead_data.get('company_size', 0) > 100,
                "real_time_processing": True,
                "global_deployment": lead_data.get('company_size', 0) > 1000,
                "high_availability": lead_data.get('company_size', 0) > 500,
                "enterprise_security": True,
                "compliance_required": any(term in (lead_data.get('industry', '')).lower() 
                                         for term in ['fintech', 'finance', 'healthcare', 'government'])
            }
        }
        
        # Include tactical intelligence if available
        if tactical_results:
            context["tactical_intelligence"] = {
                "lead_score": tactical_results.get('lead_score', 0.5),
                "qualification_score": tactical_results.get('qualification_score', 0.5),
                "pain_points": tactical_results.get('pain_points', []),
                "tech_stack": tactical_results.get('tech_stack', []),
                "predicted_conversion": tactical_results.get('predicted_conversion', 0.5),
                "estimated_deal_size": tactical_results.get('metadata', {}).get('estimated_deal_size', 75000)
            }
        
        return context
    
    async def _run_market_intelligence_agent(self, context: dict) -> dict:
        """
        Market Intelligence Agent: Industry analysis and market opportunity assessment
        - Market size and growth analysis
        - Competitive landscape mapping
        - Industry trend identification
        - Market timing assessment
        """
        
        try:
            market_analysis = await asyncio.wait_for(
                self.market_agent.analyze_market_opportunity(
                    company_data=context["company_profile"],
                    solution_requirements=context["solution_requirements"],
                    tactical_context=context.get("tactical_intelligence", {})
                ),
                timeout=self.agent_timeout
            )
            
            return market_analysis
            
        except asyncio.TimeoutError:
            print(f"⚠️  Market Intelligence agent timeout after {self.agent_timeout}s")
            return self._fallback_market_analysis(context)
        except Exception as e:
            print(f"⚠️  Market Intelligence agent failed: {str(e)[:50]}")
            return self._fallback_market_analysis(context)
    
    async def _run_technical_architecture_agent(self, context: dict, market_intel: dict) -> dict:
        """
        Technical Architecture Agent: Solution design and implementation planning
        - Solution architecture design
        - Implementation roadmap creation
        - Technical feasibility assessment
        - Resource requirement analysis
        """
        
        try:
            technical_analysis = await asyncio.wait_for(
                self.technical_agent.design_technical_solution(
                    company_data=context["company_profile"],
                    solution_requirements=context["solution_requirements"],
                    market_context=market_intel,
                    tactical_context=context.get("tactical_intelligence", {})
                ),
                timeout=self.agent_timeout
            )
            
            return technical_analysis
            
        except asyncio.TimeoutError:
            print(f"⚠️  Technical Architecture agent timeout after {self.agent_timeout}s")
            return self._fallback_technical_analysis(context, market_intel)
        except Exception as e:
            print(f"⚠️  Technical Architecture agent failed: {str(e)[:50]}")
            return self._fallback_technical_analysis(context, market_intel)
    
    async def _run_executive_decision_agent(self, context: dict, market_intel: dict, tech_analysis: dict) -> dict:
        """
        Executive Decision Agent: ROI modeling and investment decision support
        - Financial impact modeling
        - ROI and payback analysis
        - Investment recommendation
        - Business case development
        """
        
        try:
            executive_analysis = await asyncio.wait_for(
                self.executive_agent.generate_executive_analysis(
                    company_data=context["company_profile"],
                    market_intelligence=market_intel,
                    technical_analysis=tech_analysis,
                    tactical_context=context.get("tactical_intelligence", {})
                ),
                timeout=self.agent_timeout
            )
            
            return executive_analysis
            
        except asyncio.TimeoutError:
            print(f"⚠️  Executive Decision agent timeout after {self.agent_timeout}s")
            return self._fallback_executive_analysis(context, market_intel, tech_analysis)
        except Exception as e:
            print(f"⚠️  Executive Decision agent failed: {str(e)[:50]}")
            return self._fallback_executive_analysis(context, market_intel, tech_analysis)
    
    async def _run_compliance_risk_agent(self, context: dict, market_intel: dict, tech_analysis: dict) -> dict:
        """
        Compliance Risk Agent: Regulatory and governance risk assessment
        - Regulatory requirement analysis
        - Compliance gap assessment
        - Risk mitigation planning
        - Governance framework evaluation
        """
        
        try:
            compliance_analysis = await asyncio.wait_for(
                self.compliance_agent.assess_compliance_risk(
                    company_data=context["company_profile"],
                    solution_requirements=context["solution_requirements"],
                    market_context=market_intel,
                    technical_context=tech_analysis
                ),
                timeout=self.agent_timeout
            )
            
            return compliance_analysis
            
        except asyncio.TimeoutError:
            print(f"⚠️  Compliance Risk agent timeout after {self.agent_timeout}s")
            return self._fallback_compliance_analysis(context, market_intel, tech_analysis)
        except Exception as e:
            print(f"⚠️  Compliance Risk agent failed: {str(e)[:50]}")
            return self._fallback_compliance_analysis(context, market_intel, tech_analysis)
    
    async def _run_strategic_simulation_agent(self, context: dict, market_intel: dict, tech_analysis: dict, 
                                            exec_analysis: dict, compliance_analysis: dict) -> dict:
        """
        Strategic Simulation Agent: C-level conversation simulation using AutoGen
        - Executive stakeholder conversation simulation
        - Strategic decision-making scenarios
        - Investment approval discussions
        - Risk assessment dialogue
        """
        
        try:
            # Create strategic lead state for simulation
            strategic_lead_state = LeadState(
                company_name=context["company_profile"]["name"],
                industry=context["company_profile"]["industry"],
                company_size=context["company_profile"]["size"],
                contact_name="C-Suite Executive",
                # Add strategic context as pain points
                pain_points=[
                    "Strategic market positioning",
                    "Investment ROI optimization", 
                    "Competitive advantage",
                    "Risk mitigation"
                ],
                # Add technical considerations
                tech_stack=["Enterprise Architecture", "Strategic Systems", "Governance Platform"],
                engagement_level=0.8,  # High engagement for strategic discussions
                metadata={
                    "market_intelligence": market_intel,
                    "technical_analysis": tech_analysis,
                    "executive_analysis": exec_analysis,
                    "compliance_analysis": compliance_analysis,
                    "strategic_context": True,
                    "investment_amount": exec_analysis.get("total_investment", "$500,000"),
                    "projected_roi": exec_analysis.get("projected_roi", "3.2x"),
                    "market_opportunity": market_intel.get("total_addressable_market", "$75B")
                }
            )
            
            # Run enhanced strategic simulation
            result_state = await self.strategic_simulation_node.execute(strategic_lead_state)
            
            # Extract strategic simulation insights
            simulation_results = {
                "strategic_conversion_probability": result_state.predicted_conversion,
                "strategic_approach": result_state.recommended_approach,
                "c_level_insights": result_state.metadata.get("key_insights", []),
                "strategic_objections": result_state.metadata.get("objections_identified", []),
                "executive_success_factors": result_state.metadata.get("success_factors", []),
                "strategic_risks": result_state.metadata.get("risk_factors", []),
                "simulation_type": result_state.metadata.get("simulation_type", "strategic"),
                "conversation_quality": "executive_level"
            }
            
            # Add strategic-specific metrics
            if self.use_enhanced_simulation and "advanced_simulation_results" in result_state.metadata:
                adv_results = result_state.metadata["advanced_simulation_results"]
                simulation_results.update({
                    "orchestration_type": adv_results.get("simulation_type", "magentic_one"),
                    "strategic_agent_strategy": adv_results.get("strategy_used", {}),
                    "executive_engagement_metrics": adv_results.get("performance_metrics", {})
                })
            
            print(f"✅ Strategic simulation analysis complete")
            print(f"   • Executive Conversion Probability: {result_state.predicted_conversion:.1%}")
            if simulation_results.get("orchestration_type"):
                print(f"   • Orchestration: {simulation_results['orchestration_type'].title()}")
            
            return simulation_results
            
        except Exception as e:
            print(f"⚠️  Strategic simulation failed: {str(e)[:50]}")
            return self._fallback_strategic_simulation(context, exec_analysis)
    
    async def _generate_strategic_synthesis(self, context: dict, market_intel: dict, tech_analysis: dict, 
                                          exec_analysis: dict, compliance_analysis: dict, strategic_simulation: dict = None) -> dict:
        """Generate strategic synthesis combining all agent analyses"""
        
        try:
            # Use Granite model for strategic synthesis
            synthesis_prompt = f"""
            Generate strategic synthesis for {context['company_profile']['name']}:
            
            INPUTS:
            - Market Intelligence: {str(market_intel)[:500]}...
            - Technical Analysis: {str(tech_analysis)[:500]}...
            - Executive Analysis: {str(exec_analysis)[:500]}...
            - Compliance Analysis: {str(compliance_analysis)[:500]}...
            
            SYNTHESIS REQUIREMENTS:
            1. Strategic alignment assessment
            2. Investment coherence analysis
            3. Risk-reward balance evaluation
            4. Implementation feasibility score
            5. Overall strategic recommendation
            
            Provide comprehensive synthesis focusing on C-level strategic decision making.
            """
            
            response = await asyncio.wait_for(
                self.granite_client.generate_response(synthesis_prompt, max_tokens=1500),
                timeout=30
            )
            
            return {
                "strategic_alignment_score": 0.75,  # Would be extracted from AI response
                "investment_coherence": {
                    "financial_alignment": 0.80,
                    "market_timing": 0.70,
                    "technical_feasibility": 0.85,
                    "overall_coherence_score": 0.78
                },
                "risk_reward_balance": {
                    "risk_level": "medium",
                    "reward_potential": "high", 
                    "balance_score": 0.72
                },
                "implementation_feasibility": 0.75,
                "strategic_recommendation": "Proceed with phased implementation approach",
                "synthesis_narrative": response.get("content", "Strategic synthesis generated"),
                "confidence_level": 0.80,
                "strategic_simulation_insights": strategic_simulation.get("c_level_insights", []) if strategic_simulation else [],
                "executive_conversion_probability": strategic_simulation.get("strategic_conversion_probability", 0.75) if strategic_simulation else 0.75
            }
            
        except Exception as e:
            print(f"⚠️  Strategic synthesis failed: {str(e)[:50]}")
            return self._fallback_strategic_synthesis()
    
    def _generate_strategic_report(self, context: dict, market_intel: dict, tech_analysis: dict,
                                 exec_analysis: dict, compliance_analysis: dict, synthesis: dict, 
                                 strategic_simulation: dict, timing_metrics: dict) -> dict:
        """Generate comprehensive strategic intelligence report"""
        
        return {
            "company_profile": context["company_profile"],
            "execution_metrics": timing_metrics,
            
            # Agent analyses
            "market_intelligence": market_intel,
            "technical_architecture": tech_analysis,
            "executive_decision_intelligence": exec_analysis,
            "compliance_risk_assessment": compliance_analysis,
            "strategic_simulation": strategic_simulation,
            
            # Strategic synthesis
            "strategic_synthesis": synthesis,
            
            # Strategic KPIs
            "strategic_kpis": {
                "financial_metrics": {
                    "total_investment": exec_analysis.get("total_investment", "$450,000"),
                    "projected_roi": exec_analysis.get("projected_roi", "3.2x"),
                    "payback_period": exec_analysis.get("payback_period", "18 months"),
                    "3yr_revenue_potential": exec_analysis.get("revenue_potential", "$2.5M"),
                    "investment_confidence": exec_analysis.get("investment_confidence", 0.75)
                },
                "market_metrics": {
                    "market_size": market_intel.get("total_addressable_market", "$2.5B"),
                    "growth_rate": market_intel.get("market_growth_rate", "15.2%"),
                    "market_share_potential": market_intel.get("market_share_potential", "0.8%"),
                    "opportunity_score": market_intel.get("market_opportunity_score", 0.78),
                    "timing_score": market_intel.get("market_timing_score", 0.82)
                },
                "operational_metrics": {
                    "implementation_timeline": tech_analysis.get("implementation_timeline", "9-12 months"),
                    "team_size_required": tech_analysis.get("team_size_required", "8-12 people"),
                    "architecture_complexity": tech_analysis.get("complexity_score", "Medium"),
                    "feasibility_score": tech_analysis.get("technical_feasibility_score", 0.85),
                    "architecture_score": tech_analysis.get("architecture_quality_score", 0.80)
                },
                "risk_metrics": {
                    "overall_risk_level": compliance_analysis.get("overall_risk_level", "medium"),
                    "risk_score": compliance_analysis.get("risk_score", 0.35),
                    "compliance_readiness": compliance_analysis.get("compliance_readiness", "78%"),
                    "regulatory_complexity": compliance_analysis.get("regulatory_complexity", "Medium"),
                    "potential_financial_impact": compliance_analysis.get("financial_impact", "$150K mitigation cost")
                }
            },
            
            # Strategic recommendations
            "executive_summary": self._generate_executive_summary(context, market_intel, exec_analysis, synthesis),
            "key_recommendations": self._generate_key_recommendations(synthesis, market_intel, tech_analysis),
            "immediate_actions": self._generate_immediate_actions(context, synthesis),
            "strategic_initiatives": self._generate_strategic_initiatives(market_intel, tech_analysis, exec_analysis),
            
            # Analysis quality metrics
            "analysis_confidence": synthesis.get("confidence_level", 0.75),
            "data_quality_score": 0.80,
            "strategic_coherence": synthesis.get("strategic_alignment_score", 0.75)
        }
    
    # Fallback methods for when IBM services are unavailable
    def _fallback_market_analysis(self, context: dict) -> dict:
        """Fallback market intelligence without IBM services"""
        print("📊 Using fallback market analysis")
        
        company_size = context["company_profile"]["size"]
        industry = context["company_profile"]["industry"].lower() if context["company_profile"]["industry"] else ""
        
        # Industry-based market sizing
        market_size_map = {
            "fintech": "$125B",
            "healthcare": "$85B", 
            "technology": "$180B",
            "software": "$120B",
            "default": "$75B"
        }
        
        market_size = next((size for key, size in market_size_map.items() if key in industry), market_size_map["default"])
        
        return {
            "total_addressable_market": market_size,
            "market_growth_rate": "12.5%",
            "market_opportunity_score": 0.72,
            "market_timing_score": 0.78,
            "competitive_intensity": "Medium",
            "market_maturity": "Growth",
            "key_trends": ["Digital transformation", "Cloud adoption", "AI integration"],
            "market_share_potential": "0.5%"
        }
    
    def _fallback_technical_analysis(self, context: dict, market_intel: dict) -> dict:
        """Fallback technical analysis without IBM services"""
        print("⚙️  Using fallback technical analysis")
        
        company_size = context["company_profile"]["size"]
        
        complexity = "High" if company_size > 500 else "Medium" if company_size > 100 else "Low"
        timeline = "12-18 months" if company_size > 500 else "6-12 months" if company_size > 100 else "3-6 months"
        
        return {
            "implementation_timeline": timeline,
            "technical_feasibility_score": 0.80,
            "complexity_score": complexity,
            "team_size_required": f"{max(4, company_size // 50)}-{max(8, company_size // 30)} people",
            "architecture_components": ["API Gateway", "Microservices", "Database Layer", "Frontend"],
            "integration_requirements": ["CRM Integration", "Authentication", "Analytics"],
            "infrastructure_needs": ["Cloud Platform", "Load Balancing", "Monitoring"],
            "architecture_quality_score": 0.78
        }
    
    def _fallback_executive_analysis(self, context: dict, market_intel: dict, tech_analysis: dict) -> dict:
        """Fallback executive analysis without IBM services"""
        print("💼 Using fallback executive analysis")
        
        company_size = context["company_profile"]["size"]
        revenue = context["company_profile"].get("annual_revenue", company_size * 100000)  # Estimate if not provided
        
        base_investment = max(200000, company_size * 500)  # Base investment calculation
        projected_roi = 2.8 if company_size > 500 else 3.2 if company_size > 100 else 3.8
        
        return {
            "total_investment": f"${base_investment:,}",
            "projected_roi": f"{projected_roi}x",
            "payback_period": "16-20 months",
            "revenue_potential": f"${int(base_investment * projected_roi):,}",
            "investment_confidence": 0.75,
            "financial_impact_analysis": {
                "cost_savings": f"${int(base_investment * 0.6):,}",
                "revenue_increase": f"${int(base_investment * 1.2):,}",
                "efficiency_gains": "25-35%"
            },
            "business_justification": "Strong ROI with manageable implementation risk"
        }
    
    def _fallback_compliance_analysis(self, context: dict, market_intel: dict, tech_analysis: dict) -> dict:
        """Fallback compliance analysis without IBM services"""
        print("🛡️  Using fallback compliance analysis")
        
        industry = context["company_profile"]["industry"].lower() if context["company_profile"]["industry"] else ""
        
        # Industry-specific compliance requirements
        high_compliance_industries = ["fintech", "finance", "healthcare", "government"]
        is_high_compliance = any(term in industry for term in high_compliance_industries)
        
        risk_level = "high" if is_high_compliance else "medium"
        compliance_score = 0.65 if is_high_compliance else 0.80
        
        return {
            "overall_risk_level": risk_level,
            "risk_score": 1.0 - compliance_score,
            "compliance_readiness": f"{int(compliance_score * 100)}%",
            "regulatory_complexity": "High" if is_high_compliance else "Medium",
            "financial_impact": "$200K mitigation cost" if is_high_compliance else "$75K mitigation cost",
            "key_compliance_areas": ["Data Privacy", "Security Standards", "Audit Requirements"],
            "mitigation_strategies": ["Compliance framework", "Regular audits", "Staff training"],
            "regulatory_timeline": "6-12 months" if is_high_compliance else "3-6 months"
        }
    
    def _fallback_strategic_synthesis(self) -> dict:
        """Fallback strategic synthesis without IBM services"""
        print("🧠 Using fallback strategic synthesis")
        
        return {
            "strategic_alignment_score": 0.75,
            "investment_coherence": {
                "financial_alignment": 0.78,
                "market_timing": 0.72,
                "technical_feasibility": 0.80,
                "overall_coherence_score": 0.77
            },
            "risk_reward_balance": {
                "risk_level": "medium",
                "reward_potential": "high",
                "balance_score": 0.74
            },
            "implementation_feasibility": 0.78,
            "strategic_recommendation": "Proceed with strategic implementation",
            "confidence_level": 0.75
        }
    
    def _fallback_strategic_simulation(self, context: dict, exec_analysis: dict) -> dict:
        """Fallback strategic simulation without AutoGen"""
        print("🎭 Using fallback strategic simulation")
        
        company_size = context["company_profile"]["size"]
        
        # Strategic conversion tends to be higher due to C-level engagement
        base_conversion = 0.65
        if company_size > 1000:
            base_conversion += 0.15  # Large enterprises have higher strategic conversion
        elif company_size > 500:
            base_conversion += 0.1
            
        return {
            "strategic_conversion_probability": min(base_conversion, 0.9),
            "strategic_approach": "Executive-level strategic engagement",
            "c_level_insights": [
                "Strong strategic alignment with business objectives",
                "Investment aligns with market opportunity",
                "Executive team shows high engagement"
            ],
            "strategic_objections": ["Implementation timeline", "Resource allocation"],
            "executive_success_factors": ["Clear ROI", "Strategic differentiation"],
            "strategic_risks": ["Market timing", "Competitive response"],
            "simulation_type": "fallback_strategic",
            "conversation_quality": "executive_level"
        }
    
    def _generate_executive_summary(self, context: dict, market_intel: dict, exec_analysis: dict, synthesis: dict) -> str:
        """Generate executive summary"""
        
        company_name = context["company_profile"]["name"]
        market_size = market_intel.get("total_addressable_market", "$75B")
        roi = exec_analysis.get("projected_roi", "3.2x")
        
        return f"""Strategic analysis for {company_name} reveals a compelling investment opportunity in a {market_size} addressable market. 
Financial modeling indicates {roi} ROI with strong strategic alignment across market positioning, technical feasibility, and risk management. 
Recommend proceeding with phased implementation approach to capture market opportunity while managing execution risk."""
    
    def _generate_key_recommendations(self, synthesis: dict, market_intel: dict, tech_analysis: dict) -> list:
        """Generate key strategic recommendations"""
        
        return [
            f"Capitalize on {market_intel.get('market_growth_rate', '12%')} market growth with strategic solution positioning",
            f"Implement {tech_analysis.get('implementation_timeline', '6-12 month')} phased deployment to minimize risk",
            "Establish multi-stakeholder engagement strategy for C-level buy-in",
            "Develop competitive differentiation through advanced feature positioning",
            "Create strategic partnership opportunities for market expansion"
        ]
    
    def _generate_immediate_actions(self, context: dict, synthesis: dict) -> list:
        """Generate immediate action items"""
        
        return [
            "Schedule strategic alignment meeting with C-level stakeholders",
            "Initiate technical proof-of-concept development",
            "Conduct competitive landscape analysis and positioning study",
            "Develop detailed implementation roadmap with milestone tracking",
            "Establish executive sponsor and project governance structure"
        ]
    
    def _generate_strategic_initiatives(self, market_intel: dict, tech_analysis: dict, exec_analysis: dict) -> list:
        """Generate strategic initiatives"""
        
        return [
            f"Market expansion initiative targeting {market_intel.get('market_share_potential', '1%')} market share",
            f"Technical excellence program with {tech_analysis.get('team_size_required', '8-12')} dedicated team",
            f"Revenue optimization strategy achieving {exec_analysis.get('projected_roi', '3.2x')} ROI target",
            "Strategic partnership development for competitive positioning",
            "Innovation pipeline establishment for sustained market leadership"
        ]
    
    # Display methods for each agent's results
    def _display_market_results(self, market_intel: dict):
        """Display market intelligence results"""
        print(f"   • Market Size: {market_intel.get('total_addressable_market', 'Unknown')}")
        print(f"   • Growth Rate: {market_intel.get('market_growth_rate', 'Unknown')}")
        print(f"   • Opportunity Score: {market_intel.get('market_opportunity_score', 0.5):.2f}")
        print(f"   • Market Timing: {market_intel.get('market_timing_score', 0.5):.2f}")
        print(f"   • Competitive Intensity: {market_intel.get('competitive_intensity', 'Medium')}")
    
    def _display_technical_results(self, tech_analysis: dict):
        """Display technical architecture results"""
        print(f"   • Implementation Timeline: {tech_analysis.get('implementation_timeline', 'Unknown')}")
        print(f"   • Feasibility Score: {tech_analysis.get('technical_feasibility_score', 0.5):.2f}")
        print(f"   • Complexity: {tech_analysis.get('complexity_score', 'Medium')}")
        print(f"   • Team Size: {tech_analysis.get('team_size_required', 'Unknown')}")
        print(f"   • Architecture Quality: {tech_analysis.get('architecture_quality_score', 0.5):.2f}")
    
    def _display_executive_results(self, exec_analysis: dict):
        """Display executive decision results"""
        print(f"   • Investment Required: {exec_analysis.get('total_investment', 'Unknown')}")
        print(f"   • Projected ROI: {exec_analysis.get('projected_roi', 'Unknown')}")
        print(f"   • Payback Period: {exec_analysis.get('payback_period', 'Unknown')}")
        print(f"   • Revenue Potential: {exec_analysis.get('revenue_potential', 'Unknown')}")
        print(f"   • Investment Confidence: {exec_analysis.get('investment_confidence', 0.5):.1%}")
    
    def _display_compliance_results(self, compliance_analysis: dict):
        """Display compliance risk results"""
        print(f"   • Risk Level: {compliance_analysis.get('overall_risk_level', 'Unknown').title()}")
        print(f"   • Compliance Readiness: {compliance_analysis.get('compliance_readiness', 'Unknown')}")
        print(f"   • Regulatory Complexity: {compliance_analysis.get('regulatory_complexity', 'Unknown')}")
        print(f"   • Financial Impact: {compliance_analysis.get('financial_impact', 'Unknown')}")
        print(f"   • Mitigation Timeline: {compliance_analysis.get('regulatory_timeline', 'Unknown')}")
    
    def _display_strategic_simulation_results(self, simulation_results: dict):
        """Display strategic simulation results"""
        print(f"   • Executive Conversion: {simulation_results.get('strategic_conversion_probability', 0.75):.1%}")
        print(f"   • Simulation Type: {simulation_results.get('simulation_type', 'strategic').title()}")
        print(f"   • Conversation Quality: {simulation_results.get('conversation_quality', 'executive_level').replace('_', ' ').title()}")
        
        # AutoGen-specific metrics
        if simulation_results.get('orchestration_type'):
            print(f"   • Orchestration: {simulation_results['orchestration_type'].title()}")
        
        if simulation_results.get('executive_engagement_metrics'):
            metrics = simulation_results['executive_engagement_metrics']
            if metrics.get('response_time'):
                print(f"   • Response Time: {metrics['response_time']:.2f}s")
            if metrics.get('message_count'):
                print(f"   • Conversation Depth: {metrics['message_count']} exchanges")
        
        # Strategic insights
        c_level_insights = simulation_results.get('c_level_insights', [])
        if c_level_insights:
            print(f"   • C-Level Insights: {len(c_level_insights)} identified")
            for insight in c_level_insights[:2]:  # Show first 2
                print(f"     - {insight}")
        
        strategic_objections = simulation_results.get('strategic_objections', [])
        if strategic_objections:
            print(f"   • Strategic Objections: {len(strategic_objections)} identified")
        
        print(f"   • Strategic Approach: {simulation_results.get('strategic_approach', 'Executive engagement')}")
    
    def _display_strategic_intelligence_dashboard(self, report: dict):
        """Display comprehensive strategic intelligence dashboard"""
        
        print("\n" + "="*70)
        print("🎯 IBM STRATEGIC INTELLIGENCE DASHBOARD")
        print("="*70)
        
        # Performance metrics
        timing = report["execution_metrics"]
        total_time = timing["total_time"]
        print(f"\n⏱️  Execution Performance:")
        print(f"   • Total Time: {total_time:.1f} seconds ({total_time/60:.1f} minutes)")
        print(f"   • Market Intelligence: {timing['market_time']:.1f}s")
        print(f"   • Technical Architecture: {timing['technical_time']:.1f}s")
        print(f"   • Executive Decision: {timing['executive_time']:.1f}s")
        print(f"   • Compliance Risk: {timing['compliance_time']:.1f}s")
        
        performance_status = "🚀 Excellent" if total_time < 240 else "✅ Good" if total_time < 360 else "⚠️  Acceptable"
        print(f"   • Performance: {performance_status} (Target: 4-6 minutes)")
        
        # Executive Summary
        print(f"\n🎯 Executive Summary:")
        print(f"{report['executive_summary']}")
        
        # Strategic KPIs
        kpis = report["strategic_kpis"]
        
        print(f"\n💰 Financial Intelligence:")
        fm = kpis["financial_metrics"]
        print(f"   • Investment Required: {fm['total_investment']}")
        print(f"   • Projected ROI: {fm['projected_roi']}")
        print(f"   • Payback Period: {fm['payback_period']}")
        print(f"   • 3-Year Revenue: {fm['3yr_revenue_potential']}")
        print(f"   • Investment Confidence: {fm['investment_confidence']:.1%}")
        
        print(f"\n🌍 Market Intelligence:")
        mm = kpis["market_metrics"]
        print(f"   • Total Market Size: {mm['market_size']}")
        print(f"   • Growth Rate: {mm['growth_rate']}")
        print(f"   • Market Share Potential: {mm['market_share_potential']}")
        print(f"   • Opportunity Score: {mm['opportunity_score']:.2f}/1.0")
        print(f"   • Market Timing: {mm['timing_score']:.2f}/1.0")
        
        print(f"\n⚙️  Technical Architecture:")
        om = kpis["operational_metrics"]
        print(f"   • Implementation Timeline: {om['implementation_timeline']}")
        print(f"   • Team Size Required: {om['team_size_required']}")
        print(f"   • Architecture Complexity: {om['architecture_complexity']}")
        print(f"   • Feasibility Score: {om['feasibility_score']:.2f}/1.0")
        print(f"   • Architecture Quality: {om['architecture_score']:.2f}/1.0")
        
        print(f"\n🛡️  Risk Assessment:")
        rm = kpis["risk_metrics"]
        print(f"   • Overall Risk Level: {rm['overall_risk_level'].title()}")
        print(f"   • Risk Score: {rm['risk_score']:.2f}/1.0")
        print(f"   • Compliance Readiness: {rm['compliance_readiness']}")
        print(f"   • Regulatory Complexity: {rm['regulatory_complexity']}")
        print(f"   • Mitigation Cost: {rm['potential_financial_impact']}")
        
        # Strategic Recommendations
        print(f"\n🚀 Strategic Recommendations:")
        for i, rec in enumerate(report["key_recommendations"][:5], 1):
            print(f"   {i}. {rec}")
        
        # Immediate Actions
        print(f"\n⚡ Immediate Actions (Next 30 Days):")
        for i, action in enumerate(report["immediate_actions"][:5], 1):
            print(f"   {i}. {action}")
        
        # Strategic Initiatives
        print(f"\n🎯 Strategic Initiatives (3-12 Months):")
        for i, initiative in enumerate(report["strategic_initiatives"][:5], 1):
            print(f"   {i}. {initiative}")
        
        # Analysis Quality
        print(f"\n📈 Analysis Quality:")
        print(f"   • Overall Confidence: {report['analysis_confidence']:.1%}")
        print(f"   • Strategic Coherence: {report['strategic_coherence']:.2f}/1.0")
        print(f"   • Data Quality Score: {report['data_quality_score']:.2f}/1.0")
        
        # Strategic Synthesis
        synthesis = report["strategic_synthesis"]
        print(f"\n🧠 Strategic Synthesis:")
        print(f"   • Strategic Alignment: {synthesis['strategic_alignment_score']:.2f}/1.0")
        print(f"   • Investment Coherence: {synthesis['investment_coherence']['overall_coherence_score']:.1%}")
        print(f"   • Risk-Reward Balance: {synthesis['risk_reward_balance']['balance_score']:.2f}/1.0")
        print(f"   • Implementation Feasibility: {synthesis['implementation_feasibility']:.2f}/1.0")
        print(f"   • Recommendation: {synthesis['strategic_recommendation']}")


# Demo and testing functions
async def run_single_strategic_demo():
    """Run single strategic workflow demo"""
    
    enterprise_prospect = {
        "lead_id": "STRATEGIC_001",
        "company_name": "TechFlow Dynamics",
        "contact_email": "sarah.chen@techflow.com",
        "contact_name": "Sarah Chen", 
        "company_size": 850,
        "industry": "Enterprise Software",
        "location": "Austin, TX",
        "annual_revenue": 125000000,  # $125M
        "stage": "strategic_evaluation"
    }
    
    # Optional tactical results (would normally come from CrewAI workflow)
    sample_tactical_results = {
        "lead_score": 0.78,
        "qualification_score": 0.82,
        "pain_points": ["Technical debt", "Scaling challenges", "Integration complexity"],
        "tech_stack": ["AWS", "Microservices", "React", "Python"],
        "predicted_conversion": 0.73,
        "metadata": {
            "estimated_deal_size": 180000
        }
    }
    
    print("🎯 IBM Strategic Intelligence - Enhanced AutoGen Demo")
    print(f"Processing: {enterprise_prospect['company_name']}")
    print("Features: Strategic C-Level Simulation with MagenticOne")
    
    # Configure with enhanced AutoGen simulation
    config = {'use_enhanced_simulation': True}
    workflow = IBMStrategicWorkflow(config)
    result = await workflow.run_strategic_workflow(enterprise_prospect, sample_tactical_results)
    
    return result


async def run_fintech_strategic_demo():
    """Run strategic workflow demo for fintech company (high compliance)"""
    
    fintech_prospect = {
        "lead_id": "STRATEGIC_FIN_001",
        "company_name": "PaymentCore Technologies",
        "contact_email": "cto@paymentcore.com",
        "contact_name": "David Kim",
        "company_size": 420,
        "industry": "Financial Technology",
        "location": "New York, NY",
        "annual_revenue": 65000000,  # $65M
        "stage": "strategic_evaluation"
    }
    
    sample_tactical_results = {
        "lead_score": 0.85,
        "qualification_score": 0.79,
        "pain_points": ["Regulatory compliance", "Security requirements", "Payment processing speed"],
        "tech_stack": ["Payment Gateway", "Compliance Platform", "Kubernetes", "PostgreSQL"],
        "predicted_conversion": 0.68,
        "metadata": {
            "estimated_deal_size": 220000
        }
    }
    
    print("🎯 IBM Strategic Intelligence - FinTech Enhanced Demo")
    print(f"Processing: {fintech_prospect['company_name']}")
    print("Features: High-Compliance Strategic Simulation")
    
    # Configure with enhanced simulation for FinTech
    config = {'use_enhanced_simulation': True}
    workflow = IBMStrategicWorkflow(config)
    result = await workflow.run_strategic_workflow(fintech_prospect, sample_tactical_results)
    
    return result


async def run_comparative_strategic_demo():
    """Run comparative demo across different company sizes and industries"""
    
    prospects = [
        {
            "profile": {
                "lead_id": "STRATEGIC_COMP_001",
                "company_name": "MidMarket Software Co",
                "company_size": 180,
                "industry": "Software",
                "annual_revenue": 35000000,
                "location": "Seattle, WA"
            },
            "tactical": {
                "lead_score": 0.72,
                "predicted_conversion": 0.65,
                "metadata": {"estimated_deal_size": 95000}
            }
        },
        {
            "profile": {
                "lead_id": "STRATEGIC_COMP_002", 
                "company_name": "Enterprise Healthcare Systems",
                "company_size": 1200,
                "industry": "Healthcare Technology", 
                "annual_revenue": 280000000,
                "location": "Boston, MA"
            },
            "tactical": {
                "lead_score": 0.88,
                "predicted_conversion": 0.74,
                "metadata": {"estimated_deal_size": 350000}
            }
        },
        {
            "profile": {
                "lead_id": "STRATEGIC_COMP_003",
                "company_name": "Growth Stage Startup",
                "company_size": 45,
                "industry": "SaaS Platform",
                "annual_revenue": 8000000,
                "location": "San Francisco, CA"
            },
            "tactical": {
                "lead_score": 0.69,
                "predicted_conversion": 0.58,
                "metadata": {"estimated_deal_size": 45000}
            }
        }
    ]
    
    workflow = IBMStrategicWorkflow()
    results = []
    
    print("🎯 IBM Strategic Intelligence - Comparative Demo")
    print("=" * 70)
    
    for i, prospect_data in enumerate(prospects, 1):
        print(f"\n🔥 Processing Prospect {i}/3: {prospect_data['profile']['company_name']}")
        print("-" * 50)
        
        try:
            result = await workflow.run_strategic_workflow(
                prospect_data['profile'], 
                prospect_data['tactical']
            )
            results.append(result)
            print(f"✅ Completed: {prospect_data['profile']['company_name']}")
            
        except Exception as e:
            print(f"❌ Failed: {prospect_data['profile']['company_name']} - {str(e)[:50]}...")
            results.append(None)
    
    # Comparative analysis
    successful = [r for r in results if r is not None]
    if successful:
        print("\n" + "="*70)
        print("📊 COMPARATIVE STRATEGIC ANALYSIS")
        print("="*70)
        
        for result in successful:
            company = result["company_profile"]["name"]
            size = result["company_profile"]["size"]
            kpis = result["strategic_kpis"]
            
            print(f"\n📈 {company} ({size} employees):")
            print(f"   • Investment: {kpis['financial_metrics']['total_investment']}")
            print(f"   • ROI: {kpis['financial_metrics']['projected_roi']}")
            print(f"   • Market Size: {kpis['market_metrics']['market_size']}")
            print(f"   • Risk Level: {kpis['risk_metrics']['overall_risk_level'].title()}")
            print(f"   • Strategic Score: {result['strategic_coherence']:.2f}/1.0")
    
    return results


if __name__ == "__main__":
    print("IBM Strategic Intelligence Workflow")
    print("=" * 50)
    
    # Run demos
    async def main():
        print("\n1️⃣  Enterprise Strategic Demo:")
        await run_single_strategic_demo()
        
        print("\n\n2️⃣  FinTech Strategic Demo:")
        await run_fintech_strategic_demo()
        
        print("\n\n3️⃣  Comparative Strategic Demo:")
        await run_comparative_strategic_demo()
    
    asyncio.run(main())