import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
from pyvis.network import Network

from src.data_loader import load_data
from src.household_graph import build_household_graph
from src.feature_engineering import build_features
from src.ai_detection import detect_anomalies
from src.pattern_detection import detect_patterns
from src.graph_analysis import analyze_graph
from src.risk_engine import calculate_risk


# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="YOJANTRA - Welfare Fraud Intelligence",
    layout="wide"
)

st.title("YOJANTRA: Household Welfare Fraud Intelligence System")

st.markdown("""
AI-powered platform for detecting welfare fraud using **household network intelligence**.

Features:
- Household economic graph
- Fraud pattern detection
- AI anomaly detection
- Risk scoring engine
- Investigation dataset export
""")


# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

@st.cache_data
def get_data():
    file_path = "data/welfare_fraud_detection_dummy_dataset.xlsx"
    return load_data(file_path)

citizens, households, properties, schemes, ration_cards = get_data()


# ---------------------------------------------------
# BUILD HOUSEHOLD GRAPH
# ---------------------------------------------------

G = build_household_graph(citizens, properties, schemes)


# ---------------------------------------------------
# FEATURE ENGINEERING
# ---------------------------------------------------

features = build_features(citizens, properties, schemes, ration_cards)


# ---------------------------------------------------
# AI ANOMALY DETECTION
# ---------------------------------------------------

features = detect_anomalies(features)


# ---------------------------------------------------
# FRAUD PATTERN DETECTION
# ---------------------------------------------------

patterns = detect_patterns(citizens, properties, schemes, ration_cards)


# ---------------------------------------------------
# GRAPH ANALYSIS
# ---------------------------------------------------

graph_results = analyze_graph(G)


# ---------------------------------------------------
# RISK SCORING ENGINE
# ---------------------------------------------------

risk_results = calculate_risk(features, graph_results, patterns)


# ---------------------------------------------------
# DASHBOARD METRICS
# ---------------------------------------------------

st.subheader("System Overview")

col1, col2, col3 = st.columns(3)

high_risk = risk_results[risk_results["risk_score"] >= 70]

col1.metric("Total Households", len(risk_results))
col2.metric("High Risk Households", len(high_risk))
col3.metric("Total Citizens", len(citizens))


# ---------------------------------------------------
# RISK SCORE CHART
# ---------------------------------------------------

st.subheader("Household Fraud Risk Score")

fig = px.bar(
    risk_results,
    x="household_id",
    y="risk_score",
    color="risk_score",
    color_continuous_scale="Reds"
)

st.plotly_chart(fig, use_container_width=True)


# ---------------------------------------------------
# PROPERTY ANALYSIS
# ---------------------------------------------------

st.subheader("Household Property Distribution")

fig2 = px.bar(
    features,
    x="household_id",
    y="total_property_value",
    color="anomaly"
)

st.plotly_chart(fig2, use_container_width=True)


# ---------------------------------------------------
# SCHEME DISTRIBUTION
# ---------------------------------------------------

st.subheader("Scheme Participation")

scheme_counts = schemes["scheme_name"].value_counts().reset_index()
scheme_counts.columns = ["scheme", "count"]

fig3 = px.pie(
    scheme_counts,
    names="scheme",
    values="count"
)

st.plotly_chart(fig3)


# ---------------------------------------------------
# FRAUD PATTERNS
# ---------------------------------------------------

st.subheader("Detected Fraud Patterns")

st.dataframe(patterns)


# ---------------------------------------------------
# GRAPH INTELLIGENCE ALERTS
# ---------------------------------------------------

st.subheader("Graph Intelligence Alerts")

st.dataframe(graph_results)


# ---------------------------------------------------
# NETWORK GRAPH
# ---------------------------------------------------

st.subheader("Household Economic Network")

net = Network(height="600px", width="100%")

for node, data in G.nodes(data=True):

    node_type = data.get("type")

    if node_type == "citizen":
        color = "blue"
    elif node_type == "property":
        color = "green"
    elif node_type == "scheme":
        color = "red"
    else:
        color = "gray"

    net.add_node(node, label=f"{node} ({node_type})", color=color)

for source, target, data in G.edges(data=True):

    relation = data.get("relation")
    net.add_edge(source, target, title=relation)

net.write_html("graph.html")

with open("graph.html", "r", encoding="utf-8") as f:
    components.html(f.read(), height=600)


# ---------------------------------------------------
# SUSPICIOUS HOUSEHOLDS
# ---------------------------------------------------

st.subheader("Suspicious Households for Investigation")

suspicious_households = risk_results[
    risk_results["risk_score"] >= 50
]

st.dataframe(suspicious_households)


# ---------------------------------------------------
# DOWNLOAD DATASET
# ---------------------------------------------------

st.subheader("Download Investigation Dataset")

investigation_data = suspicious_households.merge(
    citizens,
    on="household_id",
    how="left"
)

csv = investigation_data.to_csv(index=False)

st.download_button(
    label="Download Suspicious Household Dataset",
    data=csv,
    file_name="fraud_investigation_dataset.csv",
    mime="text/csv"
)


# ---------------------------------------------------
# HOUSEHOLD INVESTIGATION PANEL
# ---------------------------------------------------

st.subheader("Household Investigation")

selected = st.selectbox(
    "Select Household",
    citizens["household_id"].unique()
)

members = citizens[citizens["household_id"] == selected]

st.write("Household Members")
st.dataframe(members)

member_ids = members["citizen_id"].tolist()

household_properties = properties[
    properties["owner_id"].isin(member_ids)
]

st.write("Properties Owned")
st.dataframe(household_properties)

household_schemes = schemes[
    schemes["citizen_id"].isin(member_ids)
]

st.write("Schemes Used")
st.dataframe(household_schemes)

risk_info = risk_results[
    risk_results["household_id"] == selected
]

st.write("Risk Analysis")
st.dataframe(risk_info)


# ---------------------------------------------------
# FRAUD RISK MAP
# ---------------------------------------------------

st.subheader("Geographic Distribution of High-Risk Households")

city_coordinates = {
    "Pune": (18.5204, 73.8567),
    "Nashik": (19.9975, 73.7898),
    "Nagpur": (21.1458, 79.0882),
    "Delhi": (28.6139, 77.2090)
}

map_data = risk_results.merge(
    citizens[["household_id", "address"]],
    on="household_id",
    how="left"
)

map_data["lat"] = map_data["address"].map(
    lambda x: city_coordinates.get(x, (20.5937, 78.9629))[0]
)

map_data["lon"] = map_data["address"].map(
    lambda x: city_coordinates.get(x, (20.5937, 78.9629))[1]
)

fig4 = px.scatter_mapbox(
    map_data,
    lat="lat",
    lon="lon",
    color="risk_score",
    size="risk_score",
    hover_name="household_id",
    zoom=4,
    color_continuous_scale="Reds"
)

fig4.update_layout(mapbox_style="open-street-map")

st.plotly_chart(fig4, use_container_width=True)