from datetime import datetime

import streamlit as st

from analyzer import analyze_network_output

from database import (
    init_db,
    save_incident,
    get_all_incidents,
    count_incidents,
    get_recent_incidents,
    get_relevant_incidents,
)

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

            memory = get_relevant_incidents(network_data)
            analysis = analyze_network_output(network_data, memory)

        st.subheader("AI Analysis")

        save_incident(
            str(datetime.now()),
            network_data,
            analysis
        )
        
        st.write(analysis)

        report_name = (
            f"NetworkReport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )

        st.download_button(
            label="Download Report",
            data=analysis,
            file_name=report_name,
            mime="text/plain"
        )

if st.button("View Memory"):

    if uploaded_file is None:
        st.info("Upload network output to find relevant incident memory.")
    else:
        st.text(get_relevant_incidents(network_data))

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