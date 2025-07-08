from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import re

# Load API key from .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_test_cases_and_scripts(metadata):
    """
    Generates test cases and automation scripts using OpenAI's GPT model.
    Input: metadata dict with keys: 'request', 'response', 'justification'
    Output: list of test case dicts, Python test script (as string)
    """
    # Format request and response for readability
    formatted_request = json.dumps(metadata['request'], indent=2)
    formatted_response = json.dumps(metadata['response'], indent=2)

    # Prompt with strict output structure
    prompt = f"""
                You are a senior test automation engineer.

                Below are the details of an API:

                **Business Justification**:
                {metadata['justification']}

                **Sample Request JSON**:
                {formatted_request}

                **Sample Response JSON**:
                {formatted_response}

                ---

                ✅ Generate comprehensive test cases covering:
                - Positive flows (expected inputs)
                - Negative flows (invalid, missing, or boundary values)
                - Edge cases (large inputs, nulls, special chars)

                ✅ For each test case, include:
                - Test Case Name
                - Description
                - API Endpoint
                - HTTP Method (infer based on context)
                - Request Body
                - Expected Response

                ✅ After the test cases, generate a sample Python automation script using `requests` or `httpx`.

                Respond in this format:

                ---TEST CASES---
                ```json
                [
                {{
                    "Test Case Name": "Valid Input Example",
                    "Description": "Tests a valid payload",
                    "API Endpoint": "/example",
                    "HTTP Method": "POST",
                    "Request Body": {{ "field1": "value1" }},
                    "Expected Response": {{ "status": "success" }}
                }}
                ]
                ---AUTOMATION SCRIPT---
                <python script here>
            """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
    except Exception as e:
        return f"❌ LLM Error: {e}", "# LLM call failed."

    raw_output = response.choices[0].message.content.strip()

    # Parse the structured output
    test_cases, automation_script = None, "# ⚠️ Automation script not found."
    if "---AUTOMATION SCRIPT---" in raw_output:
        try:
            test_block, automation_script = raw_output.split("---AUTOMATION SCRIPT---", 1)
            test_block = test_block.replace("---TEST CASES---", "").strip()
            json_block = re.search(r"\[.*\]", test_block, re.DOTALL).group()
            test_cases = json.loads(json_block)
        except Exception:
            test_cases = test_block.strip()  # fallback to plain string
    else:
        test_cases = raw_output  # fallback if script not found

    return test_cases, automation_script.strip()

