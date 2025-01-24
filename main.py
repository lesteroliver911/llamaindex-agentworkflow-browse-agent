from llama_index.llms.openai import OpenAI
from tavily import AsyncTavilyClient
from llama_index.core.workflow import Context
from llama_index.core.agent.workflow import FunctionAgent, ReActAgent
from llama_index.core.agent.workflow import AgentWorkflow
from llama_index.core.agent.workflow import (
    AgentInput,
    AgentOutput,
    ToolCall,
    ToolCallResult,
    AgentStream,
)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException
import helium
from PIL import Image
from io import BytesIO
from time import sleep
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client with API key from environment variable
llm = OpenAI(model="gpt-4", api_key=os.getenv("OPENAI_API_KEY"))

# Initialize Chrome driver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--force-device-scale-factor=1")
chrome_options.add_argument("--window-size=1000,1300")
chrome_options.add_argument("--disable-pdf-viewer")
driver = helium.start_chrome(headless=False, options=chrome_options)

# Web interaction tools
async def navigate_to(url: str) -> str:
    """Navigate to a specific URL."""
    helium.go_to(url)
    return f"Navigated to {url}"

async def click_element(text: str, element_type: str = "button") -> str:
    """Click an element with specific text."""
    try:
        if element_type == "link":
            helium.click(helium.Link(text))
        else:
            helium.click(text)
        return f"Clicked {element_type} with text: {text}"
    except Exception as e:
        return f"Error clicking element: {str(e)}"

async def search_text(text: str, nth_result: int = 1) -> str:
    """Search for text on the current page."""
    elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{text}')]")
    if nth_result > len(elements):
        return f"Match n°{nth_result} not found (only {len(elements)} matches found)"
    elem = elements[nth_result - 1]
    driver.execute_script("arguments[0].scrollIntoView(true);", elem)
    return f"Found {len(elements)} matches for '{text}'. Focused on element {nth_result}"

async def take_screenshot(ctx: Context) -> str:
    """Take a screenshot of the current page."""
    sleep(1.0)
    png_bytes = driver.get_screenshot_as_png()
    image = Image.open(BytesIO(png_bytes))
    current_state = await ctx.get("state")
    current_state["screenshots"].append(image)
    await ctx.set("state", current_state)
    return f"Screenshot taken: {image.size} pixels"

# Define specialized agents
browser_agent = FunctionAgent(
    name="BrowserAgent",
    description="Agent capable of web browsing and interaction",
    system_prompt=(
        "You are a web browsing agent that can navigate websites, click elements, "
        "and search for text on pages. You can also take screenshots of the current page."
    ),
    llm=llm,
    tools=[navigate_to, click_element, search_text, take_screenshot],
    can_handoff_to=["AnalysisAgent"],
)

analysis_agent = FunctionAgent(
    name="AnalysisAgent",
    description="Agent for analyzing web content and screenshots",
    system_prompt=(
        "You analyze web content and screenshots to extract relevant information "
        "and provide insights based on the browsing results."
    ),
    llm=llm,
    tools=[search_text, take_screenshot],
    can_handoff_to=["BrowserAgent"],
)

# Create workflow
agent_workflow = AgentWorkflow(
    agents=[browser_agent, analysis_agent],
    root_agent=browser_agent.name,
    initial_state={
        "screenshots": [],
        "current_url": "",
        "extracted_info": "",
    },
)

# Main execution function
async def main():
    # Get user input
    user_input = input("Enter your browsing instruction: ")
    
    handler = agent_workflow.run(
        user_msg=user_input
    )

    current_agent = None
    async for event in handler.stream_events():
        if hasattr(event, "current_agent_name") and event.current_agent_name != current_agent:
            current_agent = event.current_agent_name
            print(f"\n{'='*50}")
            print(f"🤖 Agent: {current_agent}")
            print(f"{'='*50}\n")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
