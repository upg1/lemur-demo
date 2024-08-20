import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from io import BytesIO

# Sample data
pcps = pd.DataFrame({
    'Name': ['Dr. Smith', 'Dr. Johnson', 'Dr. Lee'],
    'Specialty': ['Oncology', 'Gastroenterology', 'Hepatology'],
    'Rating': [4.5, 4.0, 4.8]
})

pharmacies = pd.DataFrame({
    'Pharmacy': ['Pharmacy A', 'Pharmacy B', 'Pharmacy C'],
    'Price': [120, 100, 110]
})

resources = pd.DataFrame({
    'Title': [
        'Understanding Bile Duct Cancer', 
        'Treatment Options for Bile Duct Cancer',
        'Support Groups for Bile Duct Cancer',
        'Rehabilitation Services',
        'Clinical Trials for Bile Duct Cancer'
    ],
    'Type': ['Article', 'Guide', 'Forum', 'Service', 'Trial'],
    'Link': [
        'https://example.com/understanding-bile-duct-cancer',
        'https://example.com/treatment-options',
        'https://example.com/support-groups',
        'https://example.com/rehabilitation-services',
        'https://example.com/clinical-trials'
    ]
})

# Title and Introduction
st.title("Healthcare Front Door for Bile Duct Cancer Patients")
st.write("""
Welcome to your digital healthcare front door. Use this application to manage your care journey with bile duct cancer, find resources, and get personalized recommendations.
""")

# Main Navigation
st.sidebar.title("Navigation")
navigation = st.sidebar.radio("Go to", ["Home", "Symptom Reporting", "Resource Library", "PCP & Specialist Finder", "Affordable Pharmacies", "Care Pathway"])

if navigation == "Home":
    st.write("""
    This app helps you navigate your care journey with bile duct cancer. Use the navigation menu to access various features and resources.
    """)

elif navigation == "Symptom Reporting":
    st.header("Symptom Reporting and Consultation")
    symptoms = st.text_area("Enter your symptoms:")
    
    if st.button("Find PCP and Specialists"):
        st.write("Matching PCPs and specialists based on your symptoms...")
        st.dataframe(pcps)

    st.subheader("Upload Consultation Documents")
    uploaded_file = st.file_uploader("Upload relevant documents after consultation", type=["pdf", "docx", "txt"])
    if uploaded_file is not None:
        st.write("Document uploaded successfully.")

elif navigation == "Resource Library":
    st.header("Resource Library")
    st.write("Search and explore resources related to bile duct cancer.")
    
    resource_types = resources['Type'].unique()
    selected_type = st.selectbox("Select a resource type:", resource_types)

    filtered_resources = resources[resources['Type'] == selected_type]

    num_columns = 3
    cols = st.columns(num_columns)
    
    for i, (index, row) in enumerate(filtered_resources.iterrows()):
        col = cols[i % num_columns]
        with col:
            st.subheader(row['Title'])
            st.write(f"**Type:** {row['Type']}")
            st.write(f"[Read more]({row['Link']})")

elif navigation == "PCP & Specialist Finder":
    st.header("Find PCPs and Specialists")
    st.write("Find and compare primary care physicians and specialists based on your needs.")
    st.dataframe(pcps)

elif navigation == "Affordable Pharmacies":
    st.header("Find Affordable Pharmacy Prices")
    st.write("Locate pharmacies with competitive pricing for your medications.")
    sorted_pharmacies = pharmacies.sort_values(by='Price')
    st.dataframe(sorted_pharmacies)

elif navigation == "Care Pathway":
    st.header("Visualize Your Care Pathway")
    st.write("See possible progressions of your condition and different care options.")
    
    def draw_flowchart():
        G = nx.DiGraph()
        nodes = ['Initial PCP', 'Oncologist', 'Gastroenterologist', 'Hepatologist', 'Palliative Care']
        edges = [
            ('Initial PCP', 'Oncologist'), ('Initial PCP', 'Gastroenterologist'),
            ('Oncologist', 'Hepatologist'), ('Gastroenterologist', 'Hepatologist'),
            ('Hepatologist', 'Palliative Care'),
            ('Oncologist', 'Palliative Care')
        ]
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)
        pos = nx.spring_layout(G, seed=42)
        plt.figure(figsize=(12, 8))
        nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue', 
                font_size=10, font_weight='bold', edge_color='gray', 
                arrows=True, arrowsize=20, node_shape='s')
        labels = {edge: f"{edge[0]} → {edge[1]}" for edge in G.edges()}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color='red')
        buf = BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        return buf

    if st.checkbox("Show Care Pathway Flowchart"):
        buf = draw_flowchart()
        st.image(buf, caption="Care Pathway Flowchart")

