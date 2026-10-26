from ollama import chat

# Read router output
with open("router_output.txt", "r") as file:
    network_data = file.read()

response = chat(
    model="llama3.2",
    messages=[
        {
            "role": "system",
            "content": """
You are a senior Cisco network engineer.

Analyse network troubleshooting output.

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

print("\n=== AI NETWORK ANALYSIS ===\n")
print(response["message"]["content"])