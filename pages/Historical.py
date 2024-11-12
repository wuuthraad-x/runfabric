import streamlit as st
import pandas as pd
import xgboost as xgb
import zipfile
import os
import category_encoders as ce
from sklearn.preprocessing import LabelEncoder

# Required columns for the model
required_columns = [
    "UDI", "Type", "Air temperature °C", "Process temperature °C",
    "Rotational speed rpm", "Torque Nm", "Tool wear min",
    "Target", "Temperature difference °C"
]

zip_path = "steam_app/xg_model.zip"  # Path to your zip file
extracted_model_path = "/steam_app/pages"  # Folder to extract the model to

# Unzip the file if not already extracted
if not os.path.exists(extracted_model_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extracted_model_path)

# Load the model file (replace with the actual model filename inside the unzipped folder)
model_file = os.path.join(extracted_model_path, "model.xgb")  # Update this with actual filename
model = xgb.Booster()
model.load_model(model_file)

# Step 2: Streamlit UI for Input or Upload
st.title("XGBoost Model Predictions with Preprocessing and Validation")
choice = st.radio("Choose Input Method:", ["Enter Data", "Upload CSV"])

# Step 3: Collect and Prepare Input Data
if choice == "Enter Data":
    # Define input fields for manual entry (customize according to your model’s features)
    udi = st.number_input("UDI", step=1)
    feature_type = st.selectbox("Type", ["Type1", "Type2"])  # Adjust based on actual values
    air_temp = st.number_input("Air temperature [K]")
    process_temp = st.number_input("Process temperature [K]")
    rotational_speed = st.number_input("Rotational speed [rpm]")
    torque = st.number_input("Torque [Nm]")
    tool_wear = st.number_input("Tool wear [min]")
    target = st.number_input("Target", step=1)
    
    # Assemble input into a DataFrame
    data = pd.DataFrame({
        "UDI": [udi],
        "Type": [feature_type],
        "Air temperature [K]": [air_temp],
        "Process temperature [K]": [process_temp],
        "Rotational speed [rpm]": [rotational_speed],
        "Torque [Nm]": [torque],
        "Tool wear [min]": [tool_wear],
        "Target": [target]
    })

elif choice == "Upload CSV":
    uploaded_file = st.file_uploader("Upload your input CSV", type="csv")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)

# Step 4: Apply Preprocessing Steps
if st.button("Predict"):
    if data is not None:
        # Convert temperatures from Kelvin to Celsius
        if "Air temperature [K]" in data.columns and "Process temperature [K]" in data.columns:
            data["Air temperature [K]"] = data["Air temperature [K]"] - 272.15
            data["Process temperature [K]"] = data["Process temperature [K]"] - 272.15
            
            # Rename columns to indicate Celsius
            data.rename(columns={
                "Air temperature [K]": "Air temperature °C",
                "Process temperature [K]": "Process temperature °C"
            }, inplace=True)
            
            # Create a new column for temperature difference
            data["Temperature difference °C"] = data["Process temperature °C"] - data["Air temperature °C"]

            # Apply categorical encoding
            encoder = ce.OrdinalEncoder(cols=['Type'])
            data = encoder.fit_transform(data)
            
            # Label encoding for 'Failure Type'
            if 'Failure Type' in data.columns:
                scaler = LabelEncoder()
                data['Failure Type'] = scaler.fit_transform(data['Failure Type'])

            # Check for and add missing columns with zeros
            for col in required_columns:
                if col not in data.columns:
                    data[col] = 0

            # Clean column names to remove special characters
            data.columns = data.columns.str.replace(r"[\[\]<>]", "", regex=True)

            # Ensure data contains only required columns, in the correct order
            data = data[required_columns]
            
            # Convert to DMatrix for prediction
            dmatrix_data = xgb.DMatrix(data.values, feature_names=required_columns)
            predictions = model.predict(dmatrix_data)
                
            # Display predictions
            st.write("Predictions:", predictions)
        else:
            st.write("Air temperature and Process temperature columns are required in Kelvin (K).")
    else:
        st.write("Please provide input data.")
