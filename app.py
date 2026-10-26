import streamlit as st
from ollama import chat

from datetime import datetime
import os

from database import (
    init_db,
    save_incident,
    get_all_incidents,
    count_incidents,
    get_recent_incidents,
)

MEMORY_FILE = "memory/incidents.txt"


def save_memory(network_input, analysis):

    with open(MEMORY_FILE, "a", encoding="utf-8") as file:

        file.write("\n")
        file.write("=" * 60)
        file.write("\n")

        file.write(
            f"Date: {datetime.now()}\n"
        )

        file.write("\nINPUT:\n")
        file.write(network_input)

        file.write("\n\nANALYSIS:\n")
        file.write(analysis)

        file.write("\n")


def load_memory():

    try:

        with open(
            MEMORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return file.read()

    except FileNotFoundError:

        return "No previous incidents."

init_db()

st.title("Network AI Agent")

st.subheader("Incident Dashboard")

total_incidents = count_incidents()

st.metric(
    "Total Incidents Analyzed",
    total_incidents
)

recent_incidents = get_recent_incidents()

st.subheader("Recent Incidents")

for incident in recent_incidents:

    st.write(
        f"Incident {incident[0]} - {incident[1]}"
    )

uploaded_file = st.file_uploader(
    "Upload Network Output",
    type=["txt"]
)

if uploaded_file is not None:

    network_data = uploaded_file.read().decode("utf-8")

    st.subheader("Input")

    st.text(network_data)

    if st.button("Analyze"):

        with st.spinner("Analyzing network data..."):

            memory = load_memory()
            response = chat(
                model="llama3.2",
                messages=[
                    {
                        "role": "system",
                        "content": f"""
You are a senior Cisco network engineer.

You have access to previous
network troubleshooting cases.

Previous Memory:

{memory}

When appropriate,
use previous incidents to assist
your analysis.

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

        st.subheader("AI Analysis")

        analysis = response["message"]["content"]

        save_memory(
            network_data,
            analysis
            )

        save_incident(
            str(datetime.now()),
            network_data,
            analysis
        )
        
        st.write(analysis)

if st.button("View Memory"):

    st.text(load_memory())

if st.button("View Database"):

    incidents = get_all_incidents()

    st.subheader("Incident Database")

    for incident in incidents:

        st.write(f"ID: {incident[0]}")

        st.write(f"Date: {incident[1]}")

        st.write("Network Input:")

        st.write(incident[2])

        st.write("Analysis:")

        st.write(incident[3])

        st.divider()