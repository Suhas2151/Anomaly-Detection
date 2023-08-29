import streamlit as st
import pandas as pd
import re
import  pickle
from sklearn.preprocessing import StandardScaler, LabelEncoder
import re
import ipaddress
from datetime import datetime
# Load the trained Random Forest model
loaded_random_forest_model = pickle.load(open('random_forest_model.pkl', 'rb'))

# Function to preprocess the log data
def preprocess_log(log_text):
    ip_pattern = r'(^\S+\.[\S+\.]+\S+)\s'
    timestamp_pattern = r'\[(\d{2}/\w+/\d{4}:\d{2}:\d{2}:\d{2} \+\d{4})\]'
    request_pattern = r'\"(\S+)\s(\S+)\s*(\S*)\"'
    status_pattern = r'(\d{3})'
    size_pattern = r'\s(\d+) "'
    # user_agent_pattern = r'"([^"]+)"'
    protocol_pattern = r'HTTP/([\d.]+)'
    # browser_pattern = r'"([^"]+)"$'
    ip = re.search(ip_pattern, log_text).group(1)
    timestamp = re.search(timestamp_pattern, log_text).group(1)
    request_line = re.search(request_pattern, log_text).group(1)
    protocol = re.search(protocol_pattern, log_text).group(1)
    size=re.search(size_pattern, log_text).group(1)
    status=re.search(status_pattern, log_text).group(1)
    if protocol=='1.1':
        protocol=6
    
    if request_line=='GET':
        request_line=4
    elif request_line=='POST':
        request_line=7
    else:
        request_line=1
    def convert_ip_to_numeric(ip):
        octets = ip.split('.')
        numeric_value = 0
        for i, octet in enumerate(octets):
            numeric_value += int(octet) * (256 ** (3 - i))
        return numeric_value


    def extract_date_time_components(timestamp):
        format_string = "%d/%b/%Y:%H:%M:%S %z"
        parsed_date = datetime.strptime(timestamp, format_string)
        
        day=parsed_date.day,
        hour=parsed_date.hour,
        minute=parsed_date.minute,
        second=parsed_date.second
    
        
        return day,hour,minute,second
    
    ip_numeric=convert_ip_to_numeric(ip)
    date, hour, minute, second=extract_date_time_components(timestamp)
    request=1
    processed_features = [ip_numeric,date,hour,minute,second,request_line,protocol,size,status,request]
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
        input_list = processed_features

   # Initialize an empty list to store all values
        all_values_list = []

        # Iterate through the elements and append them to the new list
        for item in input_list:
            if isinstance(item, tuple):
                all_values_list.append(item[0])  # Append the value inside the tuple
            else:
                all_values_list.append(item)  # Append the item as is

        predicted_label = loaded_random_forest_model.predict([all_values_list])[0]
                
        if predicted_label == 0:
            st.write("Prediction: Normal")
        else:
            st.write("Prediction: Anomaly")

