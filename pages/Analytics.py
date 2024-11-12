import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Set a title
st.title("CSV Data Analysis with Seaborn")

# Check if the CSV has been uploaded in the session state
if 'df' in st.session_state:
    df = st.session_state['df']
    
    # Filter numeric columns (float and int)
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    
    # Display the DataFrame
    st.write("Here is the CSV data you uploaded:")
    
    # Show some basic summary statistics
    st.write("Summary of the data:")
    st.write(df.describe())
    
    # Check if there are numeric columns
    if len(numeric_columns) == 0:
        st.warning("No numeric columns available for plotting.")
    else:
        # Seaborn visualization options
        st.sidebar.header("Visualization Options")
        plot_type = st.sidebar.selectbox("Select plot type", ['Pairplot', 'Correlation Heatmap', 'Histogram', 'Boxplot', 'Barplot'])
        
        if plot_type == 'Pairplot':
            # Pairplot (for numerical columns)
            st.subheader("Pairplot of the data")
            fig = plt.figure(figsize=(10, 8))
            sns.pairplot(df[numeric_columns])  # Only pass numeric columns
            st.pyplot(fig)

        elif plot_type == 'Correlation Heatmap':
            # Correlation Heatmap
            st.subheader("Correlation Heatmap")
            # Calculate correlation matrix for numeric columns
            corr = df[numeric_columns].corr()  # Only use numeric columns
            # Create a heatmap
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5, ax=ax)
            st.pyplot(fig)

        elif plot_type == 'Histogram':
            # Histogram (for numerical columns)
            st.subheader("Histogram of a selected column")
            column = st.selectbox("Select column for histogram", numeric_columns)
            
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.histplot(df[column], kde=True, ax=ax)
            st.pyplot(fig)

        elif plot_type == 'Boxplot':
            # Boxplot (for numerical columns)
            st.subheader("Boxplot for a selected column")
            column = st.selectbox("Select column for boxplot", numeric_columns)
            
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.boxplot(x=df[column], ax=ax)
            st.pyplot(fig)

        elif plot_type == 'Barplot':
            # Barplot (for categorical vs numerical columns)
            st.subheader("Barplot between categorical and numerical columns")
            categorical_columns = df.select_dtypes(include=['object']).columns
            
            if len(categorical_columns) == 0:
                st.warning("No categorical columns available for barplot.")
            else:
                categorical_column = st.selectbox("Select categorical column", categorical_columns)
                numerical_column = st.selectbox("Select numerical column", numeric_columns)
                
                fig, ax = plt.subplots(figsize=(8, 6))
                sns.barplot(x=df[categorical_column], y=df[numerical_column], ax=ax)
                st.pyplot(fig)

else:
    st.write("No CSV file uploaded yet. Please upload one on the Home page.")
