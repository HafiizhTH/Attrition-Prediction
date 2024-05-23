import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
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
    layout="wide"
)

def generate_palette(series):
    max_val = series.value_counts().idxmax()
    min_val = series.value_counts().idxmin()
    colors = ['#DD5746' if val == min_val else '#FFC470' if val == max_val else '#4793AF' for val in series.unique()]
    return dict(zip(series.unique(), colors))

# Title and description
st.title("Attrition Predictionn")
st.write("adalah sebuah aplikasi model yang bertujuan untuk membantu **Departemen Human Resource** dalam pengambilan keputusan.")

# Sidebar untuk navigasi
st.sidebar.title("Navigasi")
page = st.sidebar.selectbox("Pilih Halaman", ["Prediksi", "Informasi Karyawan", "FAQ"])

# Initialize session state to hold the uploaded data
if 'uploaded_data' not in st.session_state:
    st.session_state.uploaded_data = None

# Example file data
dataset_url = "https://raw.githubusercontent.com/HafiizhTH/Human_Resources/main/Data/Data_Clean.csv"
df_sample = pd.read_csv(dataset_url)
df_sample = df_sample.sample(20)

# Convert DataFrame ke file CSV
csv = df_sample.to_csv(index=False)

# Fitur yang digunakan pada saat model
model_features = ['Age', 'Department', 'Education', 'EducationField', 'EnvironmentSatisfaction', 'Gender', 
                  'JobInvolvement', 'JobLevel', 'JobRole', 'MaritalStatus', 'MonthlyIncome', 'PerformanceRating',
                  'RelationshipSatisfaction', 'TotalWorkingYears', 'WorkLifeBalance', 'YearsAtCompany']

# Halaman Prediksi
if page == "Prediksi":
    st.header("Mulai Prediksi!")
    st.write("Pilih metode prediksi: single data (input manual) atau multiple data (upload dataset)")

    # Membuat tab untuk single prediction dan multi-prediction
    tab1, tab2 = st.tabs(["Single-predict", "Multi-predict"])

    # Bagian Single-predict
    with tab1:
        st.write("Silakan masukkan data karyawan untuk diprediksi:")
        
        # Definisi pilihan untuk setiap kolom
        predefined_options = {
            'Department': ['Research & Development', 'Sales', 'Human Resources'],
            'Education': {'Below College': 1, 'College': 2, 'Bachelor': 3, 'Master': 4, 'Doctor': 5},
            'EducationField': ['Medical', 'Life Sciences', 'Marketing', 'Technical Degree', 'Human Resources', 'Other'],
            'Gender': ['Male', 'Female'],
            'JobRole': ['Healthcare Representative', 'Research Scientist', 'Sales Executive', 'Manager', 
                        'Laboratory Technician', 'Research Director', 'Manufacturing Director', 'Human Resources', 
                        'Sales Representative'],
            'MaritalStatus': ['Single', 'Married', 'Divorced'],
            'JobLevel': [1, 2, 3, 4, 5],
            'JobLevel': [1, 2, 3, 4, 5],
            'PerformanceRating': [1, 2, 3, 4],
            'RelationshipSatisfaction': [1, 2, 3, 4],
            'WorkLifeBalance': [1, 2, 3, 4],
            'EnvironmentSatisfaction': [1, 2, 3, 4]
        }

        # Input fields
        user_input = {}
        col1, col2, col3 = st.columns(3)
        for i, feature in enumerate(model_features):
            column = col1 if i % 3 == 0 else col2 if i % 3 == 1 else col3
            if feature in predefined_options:
                user_input[feature] = column.selectbox(f"{feature}", predefined_options[feature])
            else:
                user_input[feature] = column.number_input(f"{feature}", min_value=0)

        # Predict button for single data
        if st.button("Predict Single Data", key="predict_single"):
            try:
                # Load model dari GitHub
                filename = 'https://raw.githubusercontent.com/HafiizhTH/Human_Resources/main/Data/result_model.pkl'
                response = requests.get(filename)
                if response.status_code == 200:
                    model = pickle.loads(response.content)
                else:
                    st.error("Gagal memuat model. Status code:", response.status_code)
                    st.stop()

                # Buat Datafreame
                user_data = pd.DataFrame([user_input])

                # Preprocessing
                num_features = user_data.select_dtypes(include=['int64', 'float64']).columns.tolist()
                cat_features = user_data.select_dtypes(include=['object', 'category']).columns.tolist()

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

                user_data_processed = preprocessor.fit_transform(user_data)
                prediction = model.predict(user_data_processed)

                if prediction[0] == 1:
                    st.success("Karyawan ini diprediksi mengalami attrition.")
                else:
                    st.success("Karyawan ini diprediksi tidak mengalami attrition.")
            except Exception as e:
                st.error(f"An error occurred: {e}")

    # Bagian Multi-predict
    with tab2:
        st.write("Upload file karyawan attrition dalam format .csv atau .xlsx")

        # Download example file
        st.download_button(
            label="Download Example File",
            data=csv,
            file_name="example_employee_dataset.csv",
            mime='text/csv',
            key="download_example"
        )
        
        # Upload file
        uploaded_file = st.file_uploader("Upload file Anda", type=['csv', 'xlsx'], help="Batas 200MB per file • CSV, XLSX", key="uploader")
        
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                    
                if 'Attrition' in df.columns:
                    df = df.drop(columns=['Attrition'])
                
                if df.empty or df.shape[0] < 1:
                    st.error("Dataset kosong. Pastikan dataset memiliki minimal 1 baris.")
                else:
                    st.session_state.uploaded_data = df
                    st.success("File berhasil diupload.")
                
                st.dataframe(df)
            except Exception as e:
                st.error(f"Error reading the file: {e}")
        
        if st.button("Predict", key="predict_button"):
            if st.session_state.uploaded_data is not None:
                st.info("Proses prediksi dimulai.")
                df = st.session_state.uploaded_data
                
                try:
                    filename = 'https://raw.githubusercontent.com/HafiizhTH/Human_Resources/main/Data/result_model.pkl'
                    response = requests.get(filename)
                    if response.status_code == 200:
                        model = pickle.loads(response.content)
                    else:
                        st.error("Gagal memuat model. Status code:", response.status_code)
                        st.stop()
                    
                    missing_features = set(model_features) - set(df.columns)
                    if missing_features:
                        st.warning("Beberapa fitur yang dibutuhkan oleh model tidak ditemukan dalam dataset:")
                        st.write(missing_features)
                        st.stop()
                    
                    df = df[model_features]

                    num_features = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
                    cat_features = df.select_dtypes(include=['object', 'category']).columns.tolist()

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
                    
                    df_processed = preprocessor.fit_transform(df)
                    predictions = model.predict(df_processed)
                    df['Attrition_Prediction'] = predictions
                    
                    attrition_employees = df[df['Attrition_Prediction'] == 1]
                    no_attrition_employees = df[df['Attrition_Prediction'] == 0]
                    
                    st.subheader("Hasil Prediksi")
                    st.write(f"Jumlah karyawan yang diprediksi mengalami attrition: {len(attrition_employees)}")
                    st.write(f"Jumlah karyawan yang diprediksi tidak mengalami attrition: {len(no_attrition_employees)}")
                    
                    total_employees = len(df)
                    attrition_percentage = (len(attrition_employees) / total_employees) * 100
                    st.write(f"Persentase karyawan yang diprediksi mengalami attrition: {attrition_percentage:.0f}" "%")

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
                
# Halaman Informasi karyawan
elif page == "Informasi Karyawan":
    st.header("Informasi Karyawan")
    
    if st.session_state.uploaded_data is not None:
        df = st.session_state.uploaded_data
        
        tab1, tab2 = st.tabs(["Data Deskriptif", "Data Visualisasi"])
        
        with tab1:
            st.subheader("Tampilan dari dataset")
            
            max_rows = len(df)
            num_rows = st.number_input("Jumlah baris yang ditampilkan", min_value=1, max_value=max_rows, value=min(5, max_rows))
            
            st.dataframe(df.head(num_rows))
            st.subheader("Informasi Kolom")
            st.write(df.describe(include='all').transpose())
        
        with tab2:
            st.subheader("Visualisasi Data")
            
            select_col = st.selectbox("Pilih kolom untuk divisualisasikan", df.columns)
            
            if pd.api.types.is_numeric_dtype(df[select_col]):
                st.write(f"Visualisasi Histogram untuk kolom {select_col}")
                fig, ax = plt.subplots(figsize=(10, 5))
                sns.histplot(df[select_col], ax=ax, color='#4793AF')
                
                st.pyplot(fig)
            else:
                st.write(f"Visualisasi Bar Chart untuk kolom {select_col}")
                fig, ax = plt.subplots(figsize=(10, 5))
                palette = generate_palette(df[select_col])
                sns.countplot(y=df[select_col], palette=palette, ax=ax)
                
                # Menambahkan anotasi jumlah karyawan dengan jarak
                for container in ax.containers:
                    ax.bar_label(container, label_type='edge', padding=5, fontsize=10, color='black', fontweight='bold')
                
                st.pyplot(fig)
                
    else:
        st.info("Upload dataset pada tab Prediksi untuk melihat kontennya di sini.")

# Halaman FAQ
elif page == "FAQ":
    st.header("Frequently Asked Questions (FAQ)")

    with st.expander("Apa itu Attrition Prediction?"):
        st.write("""
        Attrition Prediction adalah sebuah aplikasi model yang bertujuan untuk memprediksi apakah seorang karyawan akan meninggalkan perusahaan atau tidak.
        """)

    with st.expander("Kolom yang digunakan untuk model"):
        st.write("""
        Berikut adalah kolom yang harus ada ketika upload file untuk model prediksi attrition:
        - Age
        - Department
        - Education
        - EducationField
        - EnvironmentSatisfaction
        - Gender
        - JobInvolvement
        - JobLevel
        - JobRole
        - MaritalStatus
        - MonthlyIncome
        - PerformanceRating
        - RelationshipSatisfaction
        - TotalWorkingYears
        - WorkLifeBalance
        - YearsAtCompany
        """)

    with st.expander("Bagaimana cara menggunakan aplikasi ini?"):
        st.write("""
        Anda dapat menggunakan aplikasi ini dengan dua cara:
        1. Single Predict: Memasukkan data secara manual untuk satu karyawan dan mendapatkan prediksi.
        2. Multi Predict: Mengupload file dataset berisi data beberapa karyawan dan mendapatkan prediksi untuk semua karyawan dalam file tersebut.
        """)

    with st.expander("Apa yang harus dilakukan jika terdapat error?"):
        st.write("""
        Jika Anda mengalami error, pastikan format data yang Anda masukkan sudah benar dan sesuai dengan kolom yang dibutuhkan. Jika error masih terjadi, Anda bisa menghubungi saya untuk bantuan lebih lanjut.
        
        Email: hafizhjunior54@gmail.com
        """)

    with st.expander("Apa keuntungan menggunakan aplikasi ini?"):
        st.write("""
        Aplikasi ini membantu Departemen Human Resource dalam mengidentifikasi karyawan yang berisiko meninggalkan perusahaan, sehingga perusahaan dapat mengambil tindakan pencegahan yang diperlukan untuk mempertahankan karyawan tersebut.
        """)
