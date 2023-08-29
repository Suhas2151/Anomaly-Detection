import streamlit as st
import pandas as pd
import re
import  pickle
from sklearn.preprocessing import StandardScaler, LabelEncoder
import ipaddress
# Load the trained Random Forest model
loaded_random_forest_model = pickle.load(open('random_forest_model.pkl', 'rb'))

# Function to preprocess the log data
def preprocess_log(log_text,protocol, user_agent):
    ip_pattern = r'(^\S+\.[\S+\.]+\S+)\s'
    timestamp_pattern = r'\[(\d{2}/\w+/\d{4}:\d{2}:\d{2}:\d{2} \+\d{4})\]'
    request_pattern = r'\"(\S+)\s(\S+)\s*(\S*)\"'
    status_pattern = r'(\d{3})'
    size_pattern = r'\s(\d+) "'
    user_agent_pattern = r'"([^"]+)"'
    protocol_pattern = r'HTTP/([\d.]+)'
    browser_pattern = r'"([^"]+)"$'
    
    ip_str = re.search(ip_pattern, log_text).group(1)
    timestamp = re.search(timestamp_pattern, log_text).group(1)
    request_line = re.search(request_pattern, log_text).group(1)
    status_code = re.search(status_pattern, log_text).group(1)
    size = re.search(size_pattern, log_text).group(1)
    # ... extract other features ...
    
    # Apply label encoding to categorical features
    protocol_encoder = LabelEncoder()
    protocol_encoded = protocol_encoder.transform([protocol])[0]
    user_agent_encoder = LabelEncoder()
    user_agent_encoded = user_agent_encoder.transform([user_agent])[0]
    # ... apply encoding for other features ...
    
    # Convert IP address to numeric value
   
    def convert_ip_to_numeric(ip_str):
        ip = ipaddress.ip_address(ip_str)
    return int(ip)
    
    # Return the processed features as a list
    processed_features = [ip_numeric, timestamp, request_line, protocol_encoded, user_agent_encoded, ...]
    return processed_features

# Streamlit UI
st.title("Log Anomaly Detection App")
st.sidebar.title("Navigation")

# Sidebar navigation
tabs = ["Home", "Anomaly Detection"]
selected_tab = st.sidebar.radio("Go to", tabs)

# Home tab
if selected_tab == "Home":
    st.write("Welcome to the Log Anomaly Detection App!")

# Anomaly Detection tab
elif selected_tab == "Anomaly Detection":
    st.write("Detect anomalies in your log data:")
    
    # User input for log text
    user_input = st.text_area("Enter log text:", "")
    
    if st.button("Detect Anomaly"):
        if user_input:
            # Preprocess the user input
            processed_features = preprocess_log(user_input)
            
            # Apply scaling if needed
            scaler = StandardScaler()
            processed_features_scaled = scaler.transform([processed_features])
            
            # Make prediction using the loaded model
            predicted_label = loaded_random_forest_model.predict(processed_features_scaled)[0]
            
            if predicted_label == 0:
                st.write("Prediction: Normal")
            else:
                st.write("Prediction: Anomaly")
