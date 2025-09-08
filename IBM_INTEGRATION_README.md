# IBM Granite LLMs & watsonx ADK Integration

A comprehensive integration of IBM's Granite Large Language Models and watsonx Orchestrate Agent Development Kit (ADK) for advanced B2B sales automation and AI-driven workflows.

## 🚀 Overview

This integration provides:

- **IBM Granite 3.0+ LLMs**: State-of-the-art language models optimized for enterprise tasks
- **watsonx ADK**: Agent development platform for building specialized AI agents
- **Sales Pipeline Automation**: End-to-end B2B sales workflows with AI agents
- **Safety & Compliance**: Built-in content moderation using Granite Guardian models
- **Cost Optimization**: Smart model selection based on task complexity

## 📋 Features

### Granite LLM Integration
- ✅ Granite 3.0 Dense Models (8B, 2B Instruct)
- ✅ Mixture of Experts (MoE) Models (3B-A800M, 1B-A400M)
- ✅ Code Models (8B, 20B Instruct)
- ✅ Guardian Safety Models (8B, 2B)
- ✅ Function Calling & Tool Use
- ✅ Template-based Generation
- ✅ Multi-backend Support (watsonx, Hugging Face, Fallback)

### watsonx ADK Integration
- ✅ Specialized Sales Agents (Research, Scoring, Outreach)
- ✅ Agent Orchestration & Workflows
- ✅ Local Development Environment
- ✅ Agent Validation & Deployment
- ✅ Export/Import Configurations
- ✅ Multi-agent Collaboration

### Sales Automation
- ✅ Company Research & Intelligence
- ✅ Lead Scoring & Qualification
- ✅ Personalized Outreach Generation
- ✅ Sales Process Simulation
- ✅ Pipeline Orchestration

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Sales App     │────│  ADK Manager     │────│  watsonx ADK    │
│                 │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                │
                       ┌──────────────────┐
                       │  Granite Client  │
                       │                  │
                       └──────────────────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
        ┌───────────┐   ┌──────────────┐   ┌──────────┐
        │  watsonx  │   │ Hugging Face │   │ Fallback │
        │           │   │              │   │          │
        └───────────┘   └──────────────┘   └──────────┘
```

## 📦 Installation

### 1. Quick Installation

```bash
python install_ibm_integration.py
```

This script will:
- Install required dependencies
- Test the integration
- Create sample configuration files
- Verify everything works in fallback mode

**Manual Installation:**
```bash
pip install -r requirements.txt
```

Key packages included:
```
ibm-watsonx-ai>=1.2.0
transformers>=4.36.0
torch>=2.0.0
accelerate>=0.25.0
```

> **Note**: The `ibm-watsonx-orchestrate-adk` package is currently in development by IBM. This integration provides simulation mode until it's available on PyPI.

### 2. Environment Configuration

Create a `.env` file:

```bash
# IBM watsonx Configuration
IBM_WATSONX_API_KEY=your_api_key_here
IBM_WATSONX_PROJECT_ID=your_project_id_here
IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com

# watsonx Orchestrate ADK
WATSONX_ORCHESTRATE_WORKSPACE_ID=your_workspace_id_here
WATSONX_ORCHESTRATE_API_KEY=your_orchestrate_api_key_here

# Optional: Hugging Face
HF_TOKEN=your_hf_token_here
```

### 3. Verify Installation

**Quick Test:**
```bash
python examples/granite_quickstart.py
```

**Full Test:**
```bash
python examples/ibm_integration_demo.py
```

> The integration works in three modes:
> - **Fallback Mode**: Works without any API keys (simulation)
> - **Hybrid Mode**: IBM watsonx API + local ADK simulation
> - **Production Mode**: Full IBM watsonx + watsonx Orchestrate (when ADK package is available)

## 🎯 Quick Start

### Basic Granite LLM Usage

```python
from ibm_integrations.granite_client import create_granite_client

# Create client
client = create_granite_client(
    model_name="granite-3.0-8b-instruct",
    backend="watsonx",
    enable_safety=True
)

# Generate content
response = client.generate(
    "Analyze the benefits of using AI in B2B sales",
    max_tokens=1024
)

print(f"Response: {response.content}")
print(f"Safe: {response.is_safe()}")
```

### Template-based Generation

```python
# Use optimized templates
response = client.generate_with_template(
    template_type="research",
    template_vars={
        "company_name": "IBM",
        "context": "Looking to understand their AI strategy"
    }
)
```

### watsonx ADK Agents

```python
from ibm_integrations.watsonx_adk_client import create_watsonx_adk_client

# Create ADK client
adk_client = create_watsonx_adk_client(local_mode=True)

# Create specialized agents
research_agent = adk_client.create_sales_research_agent()
scoring_agent = adk_client.create_lead_scoring_agent()
outreach_agent = adk_client.create_outreach_agent()

# Execute workflow
result = await adk_client.execute_workflow(
    "comprehensive_sales_pipeline",
    {
        "company_name": "TechCorp",
        "contact_name": "John Smith",
        "industry": "SaaS"
    }
)
```

## 🔧 Configuration

### Model Selection

The system automatically selects optimal models based on task type:

- **Research**: `granite-3.0-8b-instruct` (comprehensive analysis)
- **Scoring**: `granite-3.0-2b-instruct` (fast classification)
- **Outreach**: `granite-3.0-8b-instruct` (quality content)
- **Code**: `granite-code-8b-instruct` (technical tasks)
- **Safety**: `granite-guardian-3.0-2b` (content moderation)

### Cost Optimization

Choose models by cost tier:

```python
from ibm_integrations.granite_models import GraniteModelRouter

router = GraniteModelRouter()

# Get cost-optimized model
model = router.get_best_model(
    task_type="research",
    complexity="medium"  # "low", "medium", "high"
)
```

## 📊 Examples

### 1. Basic Examples
```bash
python examples/granite_quickstart.py
```

### 2. Comprehensive Demo
```bash
python examples/ibm_integration_demo.py
```

### 3. ADK Agents Demo
```bash
python examples/adk_agents_demo.py
```

### 4. Configuration Guide
```bash
python examples/configuration_guide.py
```

## 🏢 Enterprise Features

### Safety & Compliance

- **Content Moderation**: Granite Guardian models filter harmful content
- **Risk Assessment**: Automatic classification of safety risks
- **Compliance Checks**: Built-in validation for enterprise requirements

### Agent Management

- **Validation**: Comprehensive agent configuration validation
- **Deployment**: One-click deployment to watsonx Orchestrate
- **Monitoring**: Agent performance tracking and metrics
- **Version Control**: Export/import agent configurations

### Scalability

- **Multi-backend Support**: Fallback from watsonx to Hugging Face to local
- **Cost Controls**: Smart model selection based on task complexity
- **Performance Optimization**: Efficient prompt templates and caching

## 🔍 Available Models

### Granite 3.0 Models

| Model | Size | Context | Use Cases | Cost Tier |
|-------|------|---------|-----------|-----------|
| granite-3.0-8b-instruct | 8B | 8K | Research, Analysis, RAG | Medium |
| granite-3.0-2b-instruct | 2B | 8K | Classification, Scoring | Low |
| granite-3.0-3b-a800m | 3B MoE | 8K | Multi-task, Optimization | Low |
| granite-3.0-1b-a400m | 1B MoE | 8K | Real-time, Edge | Low |

### Code Models

| Model | Size | Context | Use Cases | Cost Tier |
|-------|------|---------|-----------|-----------|
| granite-code-8b-instruct | 8B | 8K | Code generation, Technical | Medium |
| granite-code-20b-instruct | 20B | 8K | Complex programming | High |

### Safety Models

| Model | Size | Context | Use Cases | Cost Tier |
|-------|------|---------|-----------|-----------|
| granite-guardian-3.0-8b | 8B | 8K | Content moderation | Low |
| granite-guardian-3.0-2b | 2B | 8K | Fast safety checks | Low |

## 🛠️ API Reference

### GraniteClient

```python
from ibm_integrations.granite_client import GraniteClient

client = GraniteClient(
    model_name="granite-3.0-8b-instruct",
    backend="watsonx",
    enable_safety=True,
    enable_function_calling=True
)

# Text generation
response = client.generate(prompt, max_tokens=1024, temperature=0.7)

# Chat interface  
response = client.chat(messages, max_tokens=1024)

# Template generation
response = client.generate_with_template(template_type, template_vars)

# Tool-enabled chat
response = client.chat_with_tools(messages, tools)
```

### watsonx ADK Client

```python
from ibm_integrations.watsonx_adk_client import WatsonxADKClient

adk_client = WatsonxADKClient(
    workspace_id="workspace_id",
    local_mode=True,
    granite_client=granite_client
)

# Create agents
agent = adk_client.create_sales_research_agent()

# Deploy agents
await adk_client.deploy_agent(agent)

# Execute workflows
result = await adk_client.execute_workflow(workflow_name, input_data)
```

### ADK Agent Manager

```python
from ibm_integrations.adk_agent_manager import ADKAgentManager

manager = ADKAgentManager(
    granite_client=granite_client,
    enable_watsonx_adk=True
)

# Execute sales crews
research = await manager.execute_research_crew(company_name, context)
scoring = await manager.execute_scoring_crew(lead_data)
outreach = await manager.execute_outreach_crew(lead_data)
```

## 🚦 Deployment

### Development Environment

```python
# Local development with fallback
client = create_granite_client(backend="fallback")
adk_client = create_watsonx_adk_client(local_mode=True)
```

### Production Environment

```python
# Full watsonx integration
client = create_granite_client(
    backend="watsonx",
    api_key=os.getenv("IBM_WATSONX_API_KEY"),
    project_id=os.getenv("IBM_WATSONX_PROJECT_ID")
)

adk_client = create_watsonx_adk_client(
    workspace_id=os.getenv("WATSONX_ORCHESTRATE_WORKSPACE_ID"),
    local_mode=False
)
```

## 🔧 Troubleshooting

### Common Issues

1. **Authentication Failed**
   - Verify `IBM_WATSONX_API_KEY` and `IBM_WATSONX_PROJECT_ID`
   - Check API key permissions and expiration

2. **Model Not Available**
   - Ensure model is deployed in your watsonx instance
   - Check model name spelling (e.g., `granite-3.0-8b-instruct`)

3. **ADK Connection Issues**
   - Verify `WATSONX_ORCHESTRATE_WORKSPACE_ID` is correct
   - Use `local_mode=True` for development

4. **Performance Issues**
   - Use smaller models for simple tasks (`granite-3.0-2b-instruct`)
   - Optimize prompts and reduce `max_tokens`

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Enable detailed logging
client = create_granite_client(model_name="granite-3.0-8b-instruct")
```

## 📈 Performance & Costs

### Model Performance

- **Granite 3.0 8B**: Best balance of capability and cost
- **Granite 3.0 2B**: 3-5x faster, 70% of 8B performance
- **MoE Models**: Best efficiency for multi-task scenarios

### Cost Optimization Tips

1. Use smaller models for simple tasks
2. Implement response caching
3. Optimize prompt templates
4. Set appropriate `max_tokens` limits
5. Use batch processing when possible

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 📚 Additional Resources

- [IBM watsonx Documentation](https://www.ibm.com/docs/en/watsonx-as-a-service)
- [watsonx Orchestrate ADK](https://github.com/IBM/ibm-watsonx-orchestrate-adk)  
- [Granite Models on Hugging Face](https://huggingface.co/ibm-granite)
- [IBM Granite Research](https://research.ibm.com/blog/granite-code-models-open-source)

## 📞 Support

For issues and questions:

1. Check the troubleshooting guide above
2. Review example configurations
3. Open an issue on GitHub
4. Contact IBM Support for watsonx-related issues

---

**Built with IBM Granite 3.0 LLMs and watsonx ADK** 🪨🤖