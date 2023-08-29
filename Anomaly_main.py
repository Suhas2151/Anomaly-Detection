import streamlit as st
import re
import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder

# Load the trained Random Forest model
loaded_random_forest_model = pickle.load(open('random_forest_model.pkl', 'rb'))

# Function to preprocess the log data
def preprocess_log(log_text):
    # Define regular expressions to extract relevant information
    ip_pattern = r'(^\S+\.[\S+\.]+\S+)\s'
    timestamp_pattern = r'\[(\d{2}/\w+/\d{4}:\d{2}:\d{2}:\d{2} \+\d{4})\]'
    request_pattern = r'\"(\S+)\s(\S+)\s*(\S*)\"'
    status_pattern = r'(\d{3})'
    size_pattern = r'\s(\d+) "'
    user_agent_pattern = r'"([^"]+)"'
    protocol_pattern = r'HTTP/([\d.]+)'
    
    # Extract relevant features using regular expressions
    ip = re.search(ip_pattern, log_text).group(1)
    request_line = re.search(request_pattern, log_text).group(1)
    protocol = re.search(protocol_pattern, log_text).group(1)
    status_code = re.search(status_pattern, log_text).group(1)
    size = re.search(size_pattern, log_text).group(1)
    # ... extract other features ...
    
    # Convert IP address to numeric value
    def convert_ip_to_numeric(ip):
    # Split the IP address into its components (octets)
             octets = ip.split('.')
    
    # Convert each octet to an integer and calculate the numeric value
    numeric_value = 0
    for i, octet in enumerate(octets):
        numeric_value += int(octet) * (256 ** (3 - i))
    
    return numeric_value

    
    # Extract date, hour, minute, seconds from the timestamp
    # ... perform necessary extraction ...
    
    # Return the processed features as a dictionary
    processed_features = {
        'Ip_address': ip_numeric,
        'HTTP request line': request_line,
        'protocol': protocol,
        'HTTP status code': status_code,
        'Size of the response in bytes': size,
        # ... add other features ...
    }
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
            
            # Convert the processed features into a DataFrame
            features_df = pd.DataFrame([processed_features])
            
            # Apply scaling if needed
            scaler = StandardScaler()
            processed_features_scaled = scaler.transform(features_df)
            
            # Make prediction using the loaded model
            predicted_label = loaded_random_forest_model.predict(processed_features_scaled)[0]
            
            if predicted_label == 0:
                st.write("Prediction: Normal")
            else:
                st.write("Prediction: Anomaly")

