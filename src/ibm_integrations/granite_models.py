from enum import Enum
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

class GraniteModelFamily(Enum):
    """IBM Granite model families (updated for Granite 3.0+)"""
    CHAT = "chat"
    INSTRUCT = "instruct" 
    CODE = "code"
    GUARDIAN = "guardian"  # Safety models
    MOE = "mixture_of_experts"  # MoE models

class GraniteModelSize(Enum):
    """Granite model sizes (updated for Granite 3.0+)"""
    TINY = "1b"
    SMALL = "2b"
    MEDIUM = "3b"
    LARGE = "8b"
    EXTRA_LARGE = "13b"
    ULTRA = "20b"
    MEGA = "34b"

@dataclass
class GraniteModelInfo:
    """Information about a Granite model (updated for Granite 3.0+)"""
    name: str
    family: GraniteModelFamily
    size: GraniteModelSize
    context_length: int
    use_cases: List[str]
    backend_supported: List[str]
    languages_supported: List[str]
    supports_function_calling: bool = False
    supports_rag: bool = False
    cost_tier: str = "medium"  # low, medium, high
    max_tokens: int = 4096

# Updated Model Registry for Granite 3.0+
GRANITE_MODELS = {
    # Granite 3.0 Dense Models
    "granite-3.0-8b-instruct": GraniteModelInfo(
        name="granite-3.0-8b-instruct",
        family=GraniteModelFamily.INSTRUCT,
        size=GraniteModelSize.LARGE,
        context_length=8192,
        use_cases=["rag", "classification", "summarization", "entity_extraction", "tool_use", "research"],
        backend_supported=["watsonx", "huggingface", "ollama"],
        languages_supported=["en", "es", "fr", "de", "it", "pt", "ja", "ko", "zh", "ar", "hi", "ru"],
        supports_function_calling=True,
        supports_rag=True,
        cost_tier="medium",
        max_tokens=4096
    ),
    
    "granite-3.0-2b-instruct": GraniteModelInfo(
        name="granite-3.0-2b-instruct", 
        family=GraniteModelFamily.INSTRUCT,
        size=GraniteModelSize.SMALL,
        context_length=8192,
        use_cases=["quick_analysis", "simple_classification", "fast_scoring", "rag"],
        backend_supported=["watsonx", "huggingface", "ollama"],
        languages_supported=["en", "es", "fr", "de", "it", "pt", "ja", "ko", "zh", "ar", "hi", "ru"],
        supports_function_calling=True,
        supports_rag=True,
        cost_tier="low",
        max_tokens=2048
    ),
    
    # Granite 3.0 MoE Models
    "granite-3.0-3b-a800m": GraniteModelInfo(
        name="granite-3.0-3b-a800m",
        family=GraniteModelFamily.MOE,
        size=GraniteModelSize.MEDIUM,
        context_length=8192,
        use_cases=["efficient_processing", "multi_task", "optimization"],
        backend_supported=["watsonx", "huggingface"],
        languages_supported=["en", "es", "fr", "de", "it", "pt"],
        supports_function_calling=True,
        supports_rag=True,
        cost_tier="low",
        max_tokens=3072
    ),
    
    "granite-3.0-1b-a400m": GraniteModelInfo(
        name="granite-3.0-1b-a400m",
        family=GraniteModelFamily.MOE,
        size=GraniteModelSize.TINY,
        context_length=8192,
        use_cases=["ultra_fast", "edge_deployment", "real_time"],
        backend_supported=["watsonx", "huggingface"],
        languages_supported=["en", "es", "fr", "de"],
        supports_function_calling=True,
        supports_rag=False,
        cost_tier="low",
        max_tokens=1536
    ),
    
    # Code Models
    "granite-code-8b-instruct": GraniteModelInfo(
        name="granite-code-8b-instruct",
        family=GraniteModelFamily.CODE,
        size=GraniteModelSize.LARGE,
        context_length=8192,
        use_cases=["code_generation", "code_explanation", "code_fixing", "technical_analysis"],
        backend_supported=["watsonx", "huggingface"],
        languages_supported=["python", "javascript", "java", "go", "rust", "cpp", "c", "ruby", "php", "swift"],
        supports_function_calling=True,
        supports_rag=False,
        cost_tier="medium",
        max_tokens=4096
    ),
    
    "granite-code-20b-instruct": GraniteModelInfo(
        name="granite-code-20b-instruct", 
        family=GraniteModelFamily.CODE,
        size=GraniteModelSize.ULTRA,
        context_length=8192,
        use_cases=["complex_code_analysis", "advanced_programming", "system_design"],
        backend_supported=["watsonx"],
        languages_supported=["python", "javascript", "java", "go", "rust", "cpp", "c", "ruby", "php", "swift"],
        supports_function_calling=True,
        supports_rag=False,
        cost_tier="high",
        max_tokens=4096
    ),
    
    # Guardian Safety Models
    "granite-guardian-3.0-8b": GraniteModelInfo(
        name="granite-guardian-3.0-8b",
        family=GraniteModelFamily.GUARDIAN,
        size=GraniteModelSize.LARGE,
        context_length=8192,
        use_cases=["safety_classification", "risk_detection", "content_moderation"],
        backend_supported=["watsonx", "huggingface"],
        languages_supported=["en"],
        supports_function_calling=False,
        supports_rag=False,
        cost_tier="low",
        max_tokens=2048
    ),
    
    "granite-guardian-3.0-2b": GraniteModelInfo(
        name="granite-guardian-3.0-2b",
        family=GraniteModelFamily.GUARDIAN,
        size=GraniteModelSize.SMALL,
        context_length=8192,
        use_cases=["fast_safety_check", "content_filtering", "risk_assessment"],
        backend_supported=["watsonx", "huggingface"],
        languages_supported=["en"],
        supports_function_calling=False,
        supports_rag=False,
        cost_tier="low",
        max_tokens=1024
    ),
    
    # Legacy Models (for backward compatibility)
    "granite-13b-chat": GraniteModelInfo(
        name="granite-13b-chat-v2",
        family=GraniteModelFamily.CHAT,
        size=GraniteModelSize.EXTRA_LARGE,
        context_length=8192,
        use_cases=["conversation", "general_analysis", "outreach_generation"],
        backend_supported=["watsonx", "huggingface"],
        languages_supported=["en"],
        supports_function_calling=False,
        supports_rag=False,
        cost_tier="medium",
        max_tokens=4096
    ),
    
    "granite-13b-instruct": GraniteModelInfo(
        name="granite-13b-instruct-v2",
        family=GraniteModelFamily.INSTRUCT,
        size=GraniteModelSize.EXTRA_LARGE,
        context_length=8192,
        use_cases=["research", "structured_tasks", "data_analysis"],
        backend_supported=["watsonx", "huggingface"],
        languages_supported=["en"],
        supports_function_calling=False,
        supports_rag=True,
        cost_tier="medium",
        max_tokens=4096
    )
}

class GraniteModelRouter:
    """Route tasks to optimal Granite 3.0+ models"""
    
    def __init__(self):
        self.task_model_mapping = {
            # Primary task mappings for Granite 3.0+
            "research": "granite-3.0-8b-instruct",
            "scoring": "granite-3.0-2b-instruct", 
            "outreach": "granite-3.0-8b-instruct",
            "simulation": "granite-3.0-8b-instruct",
            "quick_analysis": "granite-3.0-2b-instruct",
            "technical_analysis": "granite-code-8b-instruct",
            "code_generation": "granite-code-8b-instruct",
            "safety_check": "granite-guardian-3.0-2b",
            "content_moderation": "granite-guardian-3.0-8b",
            "rag": "granite-3.0-8b-instruct",
            "classification": "granite-3.0-2b-instruct",
            "summarization": "granite-3.0-8b-instruct",
            "entity_extraction": "granite-3.0-2b-instruct",
            "tool_use": "granite-3.0-8b-instruct",
            "ultra_fast": "granite-3.0-1b-a400m",
            "efficient_processing": "granite-3.0-3b-a800m"
        }
    
    def get_best_model(self, task_type: str, complexity: str = "medium") -> str:
        """Get best model for task type and complexity"""
        
        base_model = self.task_model_mapping.get(task_type, "granite-13b-chat")
        
        # Adjust based on complexity
        if complexity == "low" and "13b" in base_model:
            return base_model.replace("13b", "8b")
        elif complexity == "high" and "13b" in base_model:
            return base_model.replace("13b", "20b")
        
        return base_model
    
    def get_model_info(self, model_name: str) -> Optional[GraniteModelInfo]:
        """Get information about a model"""
        return GRANITE_MODELS.get(model_name)
    
    def list_models_by_family(self, family: GraniteModelFamily) -> list:
        """List models by family"""
        return [
            name for name, info in GRANITE_MODELS.items()
            if info.family == family
        ]
    
    def list_models_by_use_case(self, use_case: str) -> list:
        """List models that support a use case"""
        return [
            name for name, info in GRANITE_MODELS.items()
            if use_case in info.use_cases
        ]

class GraniteModelRegistry:
    """Registry for managing Granite models"""
    
    def __init__(self):
        self.router = GraniteModelRouter()
        self.models = GRANITE_MODELS
    
    def get_recommended_model(self, task: str, backend: str = "watsonx") -> str:
        """Get recommended model for task and backend"""
        
        # Get base recommendation
        model_name = self.router.get_best_model(task)
        model_info = self.router.get_model_info(model_name)
        
        # Check backend compatibility
        if model_info and backend in model_info.backend_supported:
            return model_name
        
        # Find alternative
        for name, info in self.models.items():
            if backend in info.backend_supported and task in info.use_cases:
                return name
        
        # Fallback
        return "granite-13b-chat"
    
    def validate_model_config(self, model_name: str, backend: str) -> bool:
        """Validate model configuration"""
        model_info = self.router.get_model_info(model_name)
        
        if not model_info:
            return False
        
        return backend in model_info.backend_supported
    
    def get_model_stats(self) -> Dict[str, Any]:
        """Get model registry statistics"""
        families = {}
        sizes = {}
        backends = set()
        
        for info in self.models.values():
            families[info.family.value] = families.get(info.family.value, 0) + 1
            sizes[info.size.value] = sizes.get(info.size.value, 0) + 1
            backends.update(info.backend_supported)
        
        return {
            "total_models": len(self.models),
            "families": families,
            "sizes": sizes,
            "backends": list(backends)
        }

class GranitePromptTemplates:
    """Optimized prompt templates for Granite 3.0+ models"""
    
    RESEARCH_TEMPLATE = """<|im_start|>system
You are a B2B company research specialist using IBM Granite AI. Analyze companies thoroughly and provide actionable business insights.

Instructions:
- Focus on factual, verifiable information
- Identify 3-4 specific pain points
- Include technology stack insights
- Provide competitive landscape context
<|im_end|>

<|im_start|>user
Research company: {company_name}
Context: {context}

Provide comprehensive analysis covering:
1. Company overview and key business metrics
2. Industry position and competitive challenges  
3. Technology infrastructure and pain points
4. Growth opportunities and market trends
<|im_end|>

<|im_start|>assistant"""

    SCORING_TEMPLATE = """<|im_start|>system
You are a lead scoring analyst using IBM Granite AI. Evaluate B2B leads systematically using quantitative metrics.

Scoring Criteria:
- Company fit (size, industry, revenue): 0-30 points
- Engagement level (website, content): 0-25 points  
- Pain point alignment: 0-25 points
- Decision maker access: 0-20 points

Provide score as decimal (0.0-1.0)
<|im_end|>

<|im_start|>user
Score this lead:
{lead_data}

Provide detailed scoring breakdown and final score.
<|im_end|>

<|im_start|>assistant"""

    OUTREACH_TEMPLATE = """<|im_start|>system
You are a B2B outreach specialist using IBM Granite AI. Create personalized, value-driven outreach strategies.

Guidelines:
- Reference specific company challenges
- Lead with value proposition
- Include 2-3 touchpoint strategy
- Professional but conversational tone
<|im_end|>

<|im_start|>user
Create outreach campaign for:
Contact: {contact_name}
Company: {company_name}
Context: {company_context}

Generate:
1. Email subject lines (3 options)
2. Email body (personalized)
3. LinkedIn connection message
4. Follow-up sequence outline
<|im_end|>

<|im_start|>assistant"""

    TOOL_USE_TEMPLATE = """<|im_start|>system
You are an AI assistant that can use tools to complete tasks. When you need to use a tool, format your response as:

```json
{{
  "tool_name": "tool_name",
  "parameters": {{
    "param1": "value1"
  }}
}}
```

Available tools: {available_tools}
<|im_end|>

<|im_start|>user
{user_request}
<|im_end|>

<|im_start|>assistant"""

    @classmethod
    def get_template(cls, template_type: str) -> str:
        """Get template by type"""
        templates = {
            "research": cls.RESEARCH_TEMPLATE,
            "scoring": cls.SCORING_TEMPLATE, 
            "outreach": cls.OUTREACH_TEMPLATE,
            "tool_use": cls.TOOL_USE_TEMPLATE
        }
        return templates.get(template_type, cls.RESEARCH_TEMPLATE)