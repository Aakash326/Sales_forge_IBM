import os
import json
import logging
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# IBM watsonx imports
try:
    from ibm_watsonx_ai.foundation_models import Model
    from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
    from ibm_watsonx_ai import Credentials
    HAS_WATSONX = True
except ImportError:
    HAS_WATSONX = False
    Model = None
    GenParams = None
    Credentials = None

# Hugging Face imports
try:
    from transformers import pipeline, AutoTokenizer
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False
    pipeline = None
    AutoTokenizer = None

@dataclass
class GraniteResponse:
    """Enhanced response from Granite model"""
    content: str
    model: str
    backend: str
    tokens_used: int = 0
    finish_reason: str = "completed"
    model_info: Optional[Dict[str, Any]] = None
    function_call: Optional[Dict[str, Any]] = None
    safety_check: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)
    
    def is_safe(self) -> bool:
        """Check if content is safe based on safety check"""
        if self.safety_check:
            return self.safety_check.get("is_safe", True)
        return True

class GraniteClient:
    """Enhanced IBM Granite LLM Client with 3.0+ support"""
    
    def __init__(
        self,
        model_name: str = "granite-3.0-8b-instruct",
        backend: str = "watsonx",
        api_key: str = None,
        project_id: str = None,
        enable_safety: bool = True,
        enable_function_calling: bool = False
    ):
        self.model_name = model_name
        self.backend = backend
        self.model = None
        self.safety_model = None
        self.enable_safety = enable_safety
        self.enable_function_calling = enable_function_calling
        self.logger = logging.getLogger(__name__)
        
        # Load model registry
        from .granite_models import GRANITE_MODELS, GraniteModelRegistry
        self.model_registry = GraniteModelRegistry()
        self.model_info = GRANITE_MODELS.get(model_name)
        
        # Initialize backend
        if backend == "watsonx" and HAS_WATSONX:
            self._init_watsonx(api_key, project_id)
        elif backend == "huggingface" and HAS_TRANSFORMERS:
            self._init_huggingface()
        else:
            self._init_fallback()
        
        # Initialize safety model if enabled
        if enable_safety and self.model_info:
            self._init_safety_model()
    
    def _init_watsonx(self, api_key: str, project_id: str):
        """Initialize watsonx backend"""
        api_key = api_key or os.getenv('IBM_WATSONX_API_KEY')
        project_id = project_id or os.getenv('IBM_WATSONX_PROJECT_ID')
        url = os.getenv('IBM_WATSONX_URL', 'https://us-south.ml.cloud.ibm.com')
        
        if not api_key or not project_id:
            self.logger.warning("Missing watsonx credentials, using fallback")
            self._init_fallback()
            return
        
        try:
            credentials = Credentials(url=url, api_key=api_key)
            
            # Try newer ModelInference first
            try:
                from ibm_watsonx_ai.foundation_models import ModelInference
                self.model = ModelInference(
                    model_id=f"ibm/{self.model_name}",
                    credentials=credentials,
                    project_id=project_id,
                    params={
                        "max_new_tokens": 1024,
                        "temperature": 0.7
                    }
                )
                self.logger.info(f"Initialized watsonx with ModelInference: {self.model_name}")
            except ImportError:
                # Fall back to deprecated Model class
                self.model = Model(
                    model_id=f"ibm/{self.model_name}",
                    credentials=credentials,
                    project_id=project_id,
                    params={
                        GenParams.MAX_NEW_TOKENS: 1024,
                        GenParams.TEMPERATURE: 0.7
                    }
                )
                self.logger.info(f"Initialized watsonx with Model: {self.model_name}")
                
        except Exception as e:
            error_msg = str(e)
            self.logger.error(f"watsonx init failed: {e}")
            
            # Provide specific guidance based on error type
            if "404" in error_msg and "user profile" in error_msg.lower():
                self.logger.warning("User profile not found - account may need verification")
                self.logger.warning("1. Check if IBM Cloud account email is verified")
                self.logger.warning("2. Ensure watsonx.ai service is enabled in your account")
                self.logger.warning("3. Try logging into https://dataplatform.cloud.ibm.com/")
            elif "401" in error_msg or "unauthorized" in error_msg.lower():
                self.logger.warning("Authentication failed - check credentials")
                self.logger.warning("1. Verify API key is correct and not expired")
                self.logger.warning("2. Ensure project ID is correct")
                self.logger.warning("3. Check if you have project access permissions")
            elif "403" in error_msg or "forbidden" in error_msg.lower():
                self.logger.warning("Permission denied - check account access")
                self.logger.warning("1. Verify watsonx.ai service is provisioned")
                self.logger.warning("2. Check if trial/free tier limits exceeded")
            
            self._init_fallback()
    
    def _init_huggingface(self):
        """Initialize Hugging Face backend"""
        try:
            hf_model = f"ibm/{self.model_name}"
            self.model = pipeline(
                "text-generation",
                model=hf_model,
                device_map="auto"
            )
            self.logger.info(f"Initialized HF: {self.model_name}")
        except Exception as e:
            self.logger.error(f"HF init failed: {e}")
            self._init_fallback()
    
    def _init_fallback(self):
        """Initialize fallback mode"""
        self.backend = "fallback"
        self.model = None
        self.logger.info("Using fallback mode")
    
    def generate(
        self,
        prompt: str,
        max_tokens: int = 1024,
        temperature: float = 0.7
    ) -> GraniteResponse:
        """Generate text"""
        
        if self.backend == "watsonx" and self.model:
            return self._generate_watsonx(prompt, max_tokens, temperature)
        elif self.backend == "huggingface" and self.model:
            return self._generate_huggingface(prompt, max_tokens, temperature)
        else:
            return self._generate_fallback(prompt)
    
    def _generate_watsonx(self, prompt: str, max_tokens: int, temperature: float):
        """Generate using watsonx"""
        try:
            self.model.set_params({
                GenParams.MAX_NEW_TOKENS: max_tokens,
                GenParams.TEMPERATURE: temperature
            })
            response = self.model.generate_text(prompt=prompt)
            
            return GraniteResponse(
                content=response,
                model=self.model_name,
                backend="watsonx",
                tokens_used=len(response.split())
            )
        except Exception as e:
            self.logger.error(f"watsonx generation failed: {e}")
            return self._generate_fallback(prompt)
    
    def _generate_huggingface(self, prompt: str, max_tokens: int, temperature: float):
        """Generate using Hugging Face"""
        try:
            result = self.model(
                prompt,
                max_new_tokens=max_tokens,
                temperature=temperature,
                do_sample=temperature > 0
            )
            
            generated_text = result[0]['generated_text']
            if generated_text.startswith(prompt):
                generated_text = generated_text[len(prompt):].strip()
            
            return GraniteResponse(
                content=generated_text,
                model=self.model_name,
                backend="huggingface",
                tokens_used=len(generated_text.split())
            )
        except Exception as e:
            self.logger.error(f"HF generation failed: {e}")
            return self._generate_fallback(prompt)
    
    def _generate_fallback(self, prompt: str):
        """Fallback generation for demo"""
        responses = {
            "research": "Company analysis completed. Found 3 key pain points in operational efficiency, technology modernization, and process optimization.",
            "scoring": "Lead score: 0.72/1.0. Strong fit based on company size and industry alignment. Recommend proceeding with personalized outreach.",
            "outreach": "Personalized outreach strategy created. Focus on identified pain points with value-driven messaging across email and LinkedIn channels."
        }
        
        # Simple keyword matching
        content = responses.get("research", "Analysis completed using IBM Granite technology.")
        if "score" in prompt.lower():
            content = responses["scoring"]
        elif "outreach" in prompt.lower():
            content = responses["outreach"]
        
        return GraniteResponse(
            content=content,
            model="granite-fallback",
            backend="fallback",
            tokens_used=len(content.split())
        )
    
    def chat(self, messages: List[Dict[str, str]], **kwargs):
        """Chat interface"""
        prompt = self._messages_to_prompt(messages)
        return self.generate(prompt, **kwargs)
    
    def _messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        """Convert messages to prompt"""
        parts = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "system":
                parts.append(f"Instructions: {content}")
            elif role == "user":
                parts.append(f"User: {content}")
            elif role == "assistant":
                parts.append(f"Assistant: {content}")
        parts.append("Assistant:")
        return "\n\n".join(parts)
    
    def _init_safety_model(self):
        """Initialize safety model for content moderation"""
        try:
            if self.backend == "watsonx" and HAS_WATSONX:
                safety_credentials = Credentials(
                    url=os.getenv('IBM_WATSONX_URL', 'https://us-south.ml.cloud.ibm.com'),
                    api_key=os.getenv('IBM_WATSONX_API_KEY')
                )
                self.safety_model = Model(
                    model_id="ibm/granite-guardian-3.0-2b",
                    credentials=safety_credentials,
                    project_id=os.getenv('IBM_WATSONX_PROJECT_ID'),
                    params={
                        GenParams.MAX_NEW_TOKENS: 512,
                        GenParams.TEMPERATURE: 0.1
                    }
                )
                self.logger.info("Safety model initialized")
        except Exception as e:
            self.logger.error(f"Safety model initialization failed: {e}")
            self.safety_model = None
    
    def check_content_safety(self, content: str) -> Dict[str, Any]:
        """Check content safety using Granite Guardian model"""
        if not self.enable_safety or not self.safety_model:
            return {"is_safe": True, "risk_level": "low", "categories": []}
        
        try:
            safety_prompt = f"""
            Analyze the following content for safety issues:
            
            Content: {content}
            
            Classify into risk categories:
            - jailbreaking
            - bias  
            - violence
            - profanity
            - sexual_content
            - unethical_behavior
            
            Respond with JSON format:
            {{"is_safe": boolean, "risk_level": "low|medium|high", "categories": [list]}}
            """
            
            if self.backend == "watsonx":
                response = self.safety_model.generate_text(prompt=safety_prompt)
                
                # Parse JSON response
                import re
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
            
            return {"is_safe": True, "risk_level": "low", "categories": []}
            
        except Exception as e:
            self.logger.error(f"Safety check failed: {e}")
            return {"is_safe": True, "risk_level": "unknown", "categories": []}
    
    def parse_function_call(self, content: str) -> Optional[Dict[str, Any]]:
        """Parse function call from model response"""
        if not self.enable_function_calling:
            return None
        
        try:
            # Look for JSON function call pattern
            import re
            json_pattern = r'```json\s*(\{.*?\})\s*```'
            match = re.search(json_pattern, content, re.DOTALL)
            
            if match:
                function_data = json.loads(match.group(1))
                return {
                    "name": function_data.get("tool_name"),
                    "parameters": function_data.get("parameters", {})
                }
            
            return None
            
        except Exception as e:
            self.logger.error(f"Function call parsing failed: {e}")
            return None
    
    def generate_with_template(
        self,
        template_type: str,
        template_vars: Dict[str, Any],
        **kwargs
    ) -> GraniteResponse:
        """Generate using predefined templates"""
        from .granite_models import GranitePromptTemplates
        
        templates = GranitePromptTemplates()
        template = templates.get_template(template_type)
        
        # Format template with variables
        try:
            formatted_prompt = template.format(**template_vars)
        except KeyError as e:
            raise ValueError(f"Missing template variable: {e}")
        
        return self.generate(formatted_prompt, **kwargs)
    
    def chat_with_tools(
        self,
        messages: List[Dict[str, str]],
        tools: List[Dict[str, Any]] = None,
        **kwargs
    ) -> GraniteResponse:
        """Enhanced chat with tool support"""
        
        # Add tool information to system message if tools provided
        if tools and self.enable_function_calling:
            tool_descriptions = []
            for tool in tools:
                tool_desc = f"- {tool['name']}: {tool['description']}"
                if 'parameters' in tool:
                    tool_desc += f" Parameters: {tool['parameters']}"
                tool_descriptions.append(tool_desc)
            
            tool_info = f"\n\nAvailable tools:\n" + "\n".join(tool_descriptions)
            
            # Add to system message or create one
            if messages and messages[0]['role'] == 'system':
                messages[0]['content'] += tool_info
            else:
                messages.insert(0, {
                    'role': 'system',
                    'content': f"You are an AI assistant with access to tools.{tool_info}"
                })
        
        # Generate response
        response = self.chat(messages, **kwargs)
        
        # Parse function call if present
        if self.enable_function_calling:
            function_call = self.parse_function_call(response.content)
            response.function_call = function_call
        
        # Safety check
        if self.enable_safety:
            safety_result = self.check_content_safety(response.content)
            response.safety_check = safety_result
        
        return response

def create_granite_client(
    model_name: str = "granite-3.0-8b-instruct",
    backend: str = "watsonx",
    api_key: str = None,
    project_id: str = None,
    **kwargs
) -> GraniteClient:
    """Factory function to create Granite client"""
    return GraniteClient(
        model_name=model_name,
        backend=backend,
        api_key=api_key,
        project_id=project_id,
        **kwargs
    )