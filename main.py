from src.data_loader import load_data
from src.household_graph import build_household_graph
from src.fraud_detection import calculate_household_risk
from src.graph_visualization import visualize_graph
from src.ai_detection import detect_anomalies

# Path to dataset
file_path = "data/welfare_fraud_detection_dummy_dataset.xlsx"

# Load datasets
citizens, households, properties, schemes, ration_cards = load_data(file_path)

# Build household network graph
G = build_household_graph(citizens, properties, schemes)

print("\nHousehold Network Graph Built Successfully")
print("Total Nodes:", G.number_of_nodes())
print("Total Edges:", G.number_of_edges())

# Run rule-based fraud detection
risk_results = calculate_household_risk(
    citizens,
    properties,
    schemes,
    ration_cards
)

print("\nRule-Based Fraud Detection Results:")
print(risk_results)

# Run AI anomaly detection
risk_results = detect_anomalies(risk_results)

print("\nAI Anomaly Detection Results:")
print(risk_results)

# Generate network graph visualization
visualize_graph(G)

print("\nGraph visualization generated: household_network.html")
print("Open the HTML file in your browser to view the network.")