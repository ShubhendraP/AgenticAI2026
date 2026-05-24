import gradio as gr
import random 
import time 
from datetime import datetime


LOG_FILE = "simple_agent_debug.log"

def log_to_file(message: str, error: bool = False):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    prefix = "ERROR" if error else "INFO"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} | {prefix} | {message}\n")
        f.flush()

log_to_file("Starting Simple Agent Debug Demo")

def simple_agent(query: str) -> str:
    log_to_file(f"Received query: {query}")
    start = time.time()

    try:
        if "calc" in query.lower():
            tool_name = "BrokenCalculator" if random.random() < 0.4 else "Calculator"
            log_to_file(f"Trying to use tool: {tool_name}")

            if tool_name == "Calculator":
                digits = [int(s) for s in query.replace("*", " ").split() if s.isdigit()]
                result = digits[0] * digits[1]
                log_to_file(f"Calculator result: {result}")
                answer = f"The result of the calculation is: {result}"
            else:
                raise ValueError(f"Tool {tool_name} not found")
            
        else:
            answer = f"I do not know how to handle '{query}'"
            log_to_file(f"No valid tool found for this query")

    except Exception as e:
        log_to_file(f"Error occurred: {str(e)}", error=True)
        answer = f"Agent failed due to: {str(e)}"

    finally:
        elapsed = time.time() - start
        log_to_file(f"Query completed in {elapsed:.2f} seconds")

    return answer

demo = gr.Interface(
    fn=simple_agent,
    inputs=gr.Textbox(lines=2, placeholder="Try: calc 67 8 or calc 78*7"),
    outputs="text",
    title="Debugging a Broken Agent (Simple Example)",
    description="Agent occasionally fails..."
)

if __name__ == "__main__":
    demo.launch()

                


              

