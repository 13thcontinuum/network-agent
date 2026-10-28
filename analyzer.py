import os

from ollama import chat


DEFAULT_MODEL = "llama3.2"


def analyze_network_output(network_data, previous_incidents=""):
    model = os.getenv("OLLAMA_MODEL", DEFAULT_MODEL)
    response = chat(
        model=model,
        messages=[
            {
                "role": "system",
                "content": f"""
You are a senior Cisco network engineer.

Analyze network troubleshooting output. Use previous incidents only when
they are relevant to the current network output.

Previous Incidents:

{previous_incidents}

Provide:
1. Summary
2. Issues Found
3. Root Cause
4. Recommended Fixes
"""
            },
            {
                "role": "user",
                "content": network_data
            }
        ]
    )
    return response["message"]["content"]
