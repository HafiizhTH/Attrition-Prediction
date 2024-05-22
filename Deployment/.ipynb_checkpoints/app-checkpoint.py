import streamlit as st
import pandas as pd
import pickle
import requests
from sklearn.preprocessing import StandardScaler, OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

# Set halaman streamlit
st.set_page_config(
    page_title="Attrition Prediction",
    page_icon=":bar_chart:",
    layout="centered"
)

# Title and description
st.title("Prediksi Karyawan")
st.write("Ini adalah aplikasi model **Attrition Prediction** yang bertujuan untuk membantu Departemen Human Resource dalam pengambilan keputusan.")

# Tabs untuk halaman prediksi dan informasi karyawan
tab1, tab2 = st.tabs(["Prediksi", "Info"])

# Initialize session state to hold the uploaded data
if 'uploaded_data' not in st.session_state:
    st.session_state.uploaded_data = None

# Example file data
dataset_url = "https://raw.githubusercontent.com/HafiizhTH/Human_Resources/main/Data/Data_Clean.csv"
df_sample = pd.read_csv(dataset_url)
df_sample = df_sample.sample(1)

# Convert DataFrame ke file CSV
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
    
    # Upload file
    uploaded_file = st.file_uploader("Upload file Anda", type=['csv', 'xlsx'], help="Batas 200MB per file • CSV, XLSX")
    
    if uploaded_file is not None:
        # Read dataset
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
                
            # Meremove kolom attrition dari dataset
            if 'Attrition' in df.columns:
                df = df.drop(columns=['Attrition'])
            
            # Memastikan dataset tidak kosong
            if df.empty or df.shape[0] < 1:
                st.error("Dataset kosong. Pastikan dataset memiliki minimal 1 baris.")
            else:
                st.session_state.uploaded_data = df
                st.success("File berhasil diupload.")
            
            st.dataframe(df)
        except Exception as e:
            st.error(f"Error reading the file: {e}")
    
    # Predict button
    if st.button("Predict"):
        if st.session_state.uploaded_data is not None:
            st.info("Proses prediksi dimulai.")
            df = st.session_state.uploaded_data
            
            try:
                # Load model dari GitHub
                filename = 'https://raw.githubusercontent.com/HafiizhTH/Human_Resources/main/Data/result_model.pkl'

                # Mendapatkan respons dari URL
                response = requests.get(filename)

                # Memeriksa apakah respons sukses (kode status 200)
                if response.status_code == 200:
                    # Mengunduh model.pkl dari respons konten
                    model = pickle.loads(response.content)
                    print("Model berhasil dimuat.")
                else:
                    print("Gagal memuat model. Status code:", response.status_code)

                # Tentukan fitur yang digunakan dalam model
                model_features = ['Age', 'Department', 'Education', 'EducationField', 'EnvironmentSatisfaction', 'Gender', 
                                  'JobInvolvement', 'JobLevel', 'JobRole', 'MaritalStatus', 'MonthlyIncome', 'PerformanceRating', 
                                  'RelationshipSatisfaction', 'TotalWorkingYears', 'WorkLifeBalance', 'YearsAtCompany']

                # Periksa apakah semua fitur model ada dalam dataset yang diunggah
                missing_features = set(model_features) - set(df.columns)

                if missing_features:
                    st.warning("Beberapa fitur yang dibutuhkan oleh model tidak ditemukan dalam dataset:")
                    st.write(missing_features)
                    st.stop()
                
                # Pisahkan fitur dari dataset pengguna yang sesuai dengan fitur model
                df = df[model_features]

                # fitur numerik dan kategorik
                num_features = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
                cat_features = df.select_dtypes(include=['object', 'category']).columns.tolist()

                # Preprocessing pipelines
                num_pipeline = Pipeline(steps=[
                    ('imputer', SimpleImputer(strategy='median')),
                    ('scaler', StandardScaler())
                ])

                cat_pipeline = Pipeline(steps=[
                    ('imputer', SimpleImputer(strategy='most_frequent')),
                    ('ordinal_encoder', OrdinalEncoder())
                ])

                preprocessor = ColumnTransformer(
                    transformers=[
                        ('num', num_pipeline, num_features),
                        ('cat', cat_pipeline, cat_features)
                    ],
                    remainder='passthrough'
                )
                
                # Apply preprocessing
                df_processed = preprocessor.fit_transform(df)

                # predict
                predictions = model.predict(df_processed)
                
                # Membuat fitur Attrition_Prediction untuk menyimpan hasil prediksi
                df['Attrition_Prediction'] = predictions
                
                # Filter out the employees predicted to have attrition
                attrition_employees = df[df['Attrition_Prediction'] == 1]
                
                if not attrition_employees.empty:
                    st.subheader("Karyawan yang diprediksi akan mengalami attrition:")
                    st.dataframe(attrition_employees)
                else:
                    st.info("Tidak terdapat karyawan yang mengalami attrition.")
                    
            except requests.exceptions.RequestException as e:
                st.error(f"Error downloading the model: {e}")
            except pickle.UnpicklingError as e:
                st.error(f"Error unpickling the model: {e}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
                
        else:
            st.warning("Silakan upload file terlebih dahulu.")

with tab2:
    st.header("Informasi Karyawan")
    
    if st.session_state.uploaded_data is not None:
        df = st.session_state.uploaded_data
        
        st.subheader("Tampilan dari dataset")
        
        max_rows = len(df)
        
        # Input for number of rows to display with adjusted default value
        num_rows = st.number_input("Jumlah baris yang ditampilkan", min_value=1, max_value=max_rows, value=min(5, max_rows))
        
        # Display the specified number of rows from the dataset
        st.dataframe(df.head(num_rows))
        
        st.subheader("Informasi Kolom")
        st.write(df.describe(include='all').transpose())
    else:
        st.info("Upload dataset pada tab Prediksi untuk melihat kontennya di sini.")
