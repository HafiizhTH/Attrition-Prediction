import streamlit as st
import pandas as pd
import pickle
import requests
from io import BytesIO
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

# Set the page configuration
st.set_page_config(
    page_title="Attrition Prediction",
    page_icon=":bar_chart:",
    layout="centered"
)

# Title and description
st.title("Prediksi Karyawan")
st.write("Ini adalah aplikasi model **Attrition Prediction** yang bertujuan untuk membantu Departemen Human Resource dalam pengambilan keputusan.")

# Tabs for Prediction and Info
tab1, tab2 = st.tabs(["Prediksi", "Info"])

# Initialize session state to hold the uploaded data
if 'uploaded_data' not in st.session_state:
    st.session_state.uploaded_data = None

# Example file data
dataset_url = "https://raw.githubusercontent.com/HafiizhTH/Human_Resources/main/Data/Data_Clean.csv"
df_sample = pd.read_csv(dataset_url)
df_sample = df_sample.sample(50)

# Convert DataFrame to CSV
csv = df_sample.to_csv(index=False)

with tab1:
    st.header("Mulai Prediksi!")
    st.write("Upload file karyawan attrition dalam format .csv atau .xlsx")

    # Download example file
    st.download_button(
        label="Download Example File",
        data=csv,
        file_name="example_employee_dataset.csv",
        mime='text/csv'
    )
    
    # File upload
    uploaded_file = st.file_uploader("Upload file Anda", type=['csv', 'xlsx'], help="Batas 200MB per file • CSV, XLSX")
    
    if uploaded_file is not None:
        # Read the file into a DataFrame
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            # Store the uploaded data in session state
            st.session_state.uploaded_data = df
            st.success("File berhasil diupload.")
            
            # Display the dataframe
            st.dataframe(df)
        except Exception as e:
            st.error(f"Error reading the file: {e}")
    
    # Predict button
    if st.button("Predict"):
        if st.session_state.uploaded_data is not None:
            st.info("Proses prediksi dimulai.")
            df = st.session_state.uploaded_data

            # Check and separate 'Attrition' column if it exists
            if 'Attrition' in df.columns:
                df = df.drop(columns=['Attrition'])
            
            # Load the model from GitHub
            model_url = "https://raw.githubusercontent.com/HafiizhTH/Human_Resources/main/Data/result_model.pkl"
            response = requests.get(model_url)
            response.raise_for_status()  # Ensure the request was successful
            model = pickle.load(BytesIO(response.content))

            # Separate features into numerical and categorical
            num_features = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
            cat_features = df.select_dtypes(include=['object', 'category']).columns.tolist()

            # Preprocessing pipelines for numerical and categorical features
            num_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler', StandardScaler())
            ])
            
            cat_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('onehot', OneHotEncoder(handle_unknown='ignore'))
            ])
            
            preprocessor = ColumnTransformer(
                transformers=[
                    ('num', num_pipeline, num_features),
                    ('cat', cat_pipeline, cat_features)
                ]
            )
            
            # Apply preprocessing to the data
            df_processed = preprocessor.fit_transform(df)

            # Predicting with the model
            predictions = model.predict(df_processed)
            
            # Add predictions to the dataframe
            df['Attrition_Prediction'] = predictions
            
            # Filter out the employees predicted to have attrition
            attrition_employees = df[df['Attrition_Prediction'] == 1]
            
            if not attrition_employees.empty:
                st.subheader("Karyawan yang diprediksi akan mengalami attrition:")
                st.dataframe(attrition_employees)
            else:
                st.info("Tidak terdapat karyawan yang mengalami attrition.")
        else:
            st.warning("Silakan upload file terlebih dahulu.")

with tab2:
    st.header("Informasi Karyawan")
    
    if st.session_state.uploaded_data is not None:
        df = st.session_state.uploaded_data
        
        st.subheader("Tampilan dari dataset")
        
        # Input for number of rows to display
        num_rows = st.number_input("Jumlah baris yang ditampilkan", min_value=1, max_value=len(df), value=5)
        
        # Display the specified number of rows from the dataset
        st.dataframe(df.head(num_rows))
        
        st.subheader("Informasi Kolom")
        st.write(df.describe(include='all').transpose())
    else:
        st.info("Upload dataset pada tab Prediksi untuk melihat kontennya di sini.")
