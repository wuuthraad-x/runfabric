import streamlit as st
import pandas as pd

# Set a title
st.title("Upload CSV File")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# If a file is uploaded, read it and store it in session state
if uploaded_file is not None:
    # Read the CSV into a DataFrame
    df = pd.read_csv(uploaded_file)
    
    # Store the DataFrame in session state
    st.session_state['df'] = df
    
    # Display the DataFrame
    st.write("CSV uploaded successfully!")
    st.write(df)
else:
    st.write("Please upload a CSV file.")
