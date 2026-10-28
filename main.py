from datetime import datetime

from analyzer import analyze_network_output
from database import get_relevant_incidents, init_db, save_incident

init_db()

with open("router_output.txt", "r", encoding="utf-8") as file:
    network_data = file.read()

previous_incidents = get_relevant_incidents(network_data)
analysis = analyze_network_output(network_data, previous_incidents)
save_incident(str(datetime.now()), network_data, analysis)

print("\n=== AI NETWORK ANALYSIS ===\n")
print(analysis)