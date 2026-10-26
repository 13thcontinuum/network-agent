with open("router_output.txt", "r") as file:
    network_data = file.read()

print("\n=== Network Troubleshooting Agent ===\n")

print("Data Loaded:\n")
print(network_data)

print("\nAGENT ANALYSIS\n")

if "Gateway of last resort is not set" in network_data:
    print("Issue Found:")
    print("- Missing default route")

else:
    print("No obvious issue detected")