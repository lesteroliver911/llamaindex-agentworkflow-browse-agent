# AI-Powered Web Automation Agents 🤖

Automate web interactions using LLMs and llamaindex agentworkflow. 

## Why This Exists

Traditional web automation is brittle and high-maintenance. This system uses GPT-4 and LlamaIndex to create resilient, natural-language-driven automation that:

- Reduces engineering time spent on web scraping/testing
- Adapts to UI changes without code updates
- Enables non-technical team members to create automation workflows

## Core Features

- **Natural Language Control**: Write instructions in plain English
- **Intelligent Navigation**: Automatically finds and interacts with UI elements
- **Content Analysis**: Extracts and analyzes web content using GPT-4o
- **State Management**: Maintains context across multi-step workflows

## Quick Start

```bash
# Clone the repo
git clone https://github.com/yourusername/web-automation-agents

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Add your API keys to .env

# Run with example workflow
python main.py
```

### Content Research
```python
instruction = """
Go to competitor.com/pricing,
compare all plan features,
screenshot the comparison table,
analyze pricing strategy
"""

workflow.run(instruction)
```

### Web Testing
```python
instruction = """
Navigate to app.com/signup,
try creating account with invalid email,
verify error message,
screenshot results
"""

workflow.run(instruction)
```

## Requirements

- Python 3.8+
- OpenAI API key (GPT-4 access required)
- Chrome/Chromium browser
- 8GB+ RAM recommended

## Integration Examples

### Custom Agent Tools
```python
@tool
async def custom_action(ctx: Context) -> str:
    # Your custom automation logic
    return "Action completed"

browser_agent.add_tool(custom_action)
```

### Workflow Customization
```python
workflow = AgentWorkflow(
    agents=[browser_agent, analysis_agent],
    root_agent="BrowserAgent",
    initial_state={
        "custom_data": {},
        "screenshots": []
    }
)
```

## Production Considerations

- Rate Limiting: Implement appropriate delays for web requests
- Error Handling: Add retry logic for network issues
- State Management: Consider persistent storage for workflow state
- Monitoring: Add logging for production debugging

## Roadmap

- [ ] Parallel agent execution
- [ ] Custom LLM support
- [ ] Browser profile management
- [ ] API endpoint wrapper


## License

MIT

Built with ❤️ using [LlamaIndex](https://github.com/jerryjliu/llama_index)
