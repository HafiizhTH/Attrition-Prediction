# Mengimpor library yang diperlukan
import streamlit as st
import pandas as pd
import pickle

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

# Example file data
example_data = {
    'EmployeeID': [1, 2, 3, 4, 5],
    'Age': [34, 28, 45, 32, 25],
    'Gender': ['Male', 'Female', 'Male', 'Female', 'Male'],
    'Department': ['Sales', 'HR', 'Finance', 'IT', 'Marketing'],
    'MonthlyIncome': [5000, 6000, 7000, 8000, 9000]
}
example_df = pd.DataFrame(example_data)
example_csv = example_df.to_csv(index=False).encode('utf-8')

with tab1:
    st.header("Mulai Prediksi!")
    st.write("Upload file karyawan attrition dalam format .csv atau .xlsx")

    # Download example file
    st.download_button(
        label="Download Example File",
        data=example_csv,
        file_name="example_employee_data.csv",
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
        num_rows = st.number_input("Jumlah baris untuk ditampilkan", min_value=1, max_value=len(df), value=5)
        
        # Display the specified number of rows from the dataset
        st.dataframe(df.head(num_rows))
        
        st.subheader("Informasi Kolom")
        st.write(df.describe(include='all').transpose())
    else:
        st.info("Upload dataset pada tab Prediksi untuk melihat kontennya di sini.")