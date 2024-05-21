# Mengimpor library yang diperlukan
import streamlit as st
import pandas as pd
import joblib

# Set the page configuration
st.set_page_config(
    page_title="Attrition Prediction",
    page_icon=":bar_chart:",
    layout="centered"
)

# Title and description
st.title("Prediksi Karyawan")
st.write("Ini sebuah aplikasi model **Attrition Prediction** yang bertujuan agar dapat membantu Departemen Human Resource dalam pengambilan keputusan.")

# Tabs for Prediction and Info
tab1, tab2 = st.tabs(["Prediksi", "Info"])

# Initialize session state to hold the uploaded data
if 'uploaded_data' not in st.session_state:
    st.session_state.uploaded_data = None

# Load model
df_model = "https://raw.githubusercontent.com/HafiizhTH/Human_Resources/main/Data/result_model.pkl"
model = joblib.load(df_model)

# Example file data
dataset = "https://raw.githubusercontent.com/HafiizhTH/Human_Resources/main/Data/Data_Clean.csv"
df_sample = pd.read_csv(dataset)
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
            # Placeholder for prediction logic
            st.info("Proses prediksi dimulai.")
            # Here you can add the code to perform predictions
            # For example: predictions = model.predict(df)
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