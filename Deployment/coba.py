import streamlit as st
import pandas as pd
import joblib

# Memuat model dari file joblib
url = "Data/result_model.pkl"
model = joblib.load(url)
print(model)