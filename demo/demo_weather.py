%%writefile app.py
import streamlit as st
import pandas as pd
import numpy as np
import pickle

# ===============================
# LOAD MODELS & METADATA
# ===============================
rf_model = pickle.load(open("rf_model.pkl", "rb"))
knn_model = pickle.load(open("knn_model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))
feature_names = pickle.load(open("feature_names.pkl", "rb"))

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="🌦️ RainTomorrow Prediction",
    layout="centered"
)

st.title("🌦️ Dự báo mưa ngày mai")
st.write("Nhập thông tin thời tiết để dự đoán **RainTomorrow**.")

# ===============================
# INPUT FORM (giữ nguyên code phần input của bạn)
# ===============================
st.subheader("🔧 Thông tin thời tiết")

MinTemp = st.slider("MinTemp (°C)", -10.0, 35.0, 10.0)
MaxTemp = st.slider("MaxTemp (°C)", 0.0, 50.0, 25.0)
Rainfall = st.slider("Rainfall (mm)", 0.0, 300.0, 0.0)
Evaporation = st.slider("Evaporation (mm)", 0.0, 25.0, 5.0)
Sunshine = st.slider("Sunshine (hours)", 0.0, 15.0, 8.0)

WindGustDir = st.selectbox("WindGustDir (encoded)", list(range(16)))
WindGustSpeed = st.slider("WindGustSpeed (km/h)", 0, 150, 40)

WindDir9am = st.selectbox("WindDir9am (encoded)", list(range(16)))
WindDir3pm = st.selectbox("WindDir3pm (encoded)", list(range(16)))

WindSpeed9am = st.slider("WindSpeed9am (km/h)", 0, 80, 10)
WindSpeed3pm = st.slider("WindSpeed3pm (km/h)", 0, 80, 15)

Humidity9am = st.slider("Humidity9am (%)", 0, 100, 60)
Humidity3pm = st.slider("Humidity3pm (%)", 0, 100, 50)

Pressure9am = st.slider("Pressure9am (hPa)", 980.0, 1045.0, 1015.0)
Pressure3pm = st.slider("Pressure3pm (hPa)", 980.0, 1045.0, 1012.0)

Cloud9am = st.slider("Cloud9am (0–8)", 0, 8, 4)
Cloud3pm = st.slider("Cloud3pm (0–8)", 0, 8, 4)

Temp9am = st.slider("Temp9am (°C)", 0.0, 40.0, 18.0)
Temp3pm = st.slider("Temp3pm (°C)", 0.0, 45.0, 25.0)

RainToday = st.selectbox("Hôm nay có mưa không?", ["No", "Yes"])
RainToday = 1 if RainToday == "Yes" else 0

Month = st.slider("Month", 1, 12, 6)

Temp_Diff = MaxTemp - MinTemp

# ===============================
# BUILD INPUT VECTOR
# ===============================
row = {col: 0 for col in feature_names}

row.update({
    "MinTemp": MinTemp,
    "MaxTemp": MaxTemp,
    "Rainfall": Rainfall,
    "Evaporation": Evaporation,
    "Sunshine": Sunshine,
    "WindGustDir": WindGustDir,
    "WindGustSpeed": WindGustSpeed,
    "WindDir9am": WindDir9am,
    "WindDir3pm": WindDir3pm,
    "WindSpeed9am": WindSpeed9am,
    "WindSpeed3pm": WindSpeed3pm,
    "Humidity9am": Humidity9am,
    "Humidity3pm": Humidity3pm,
    "Pressure9am": Pressure9am,
    "Pressure3pm": Pressure3pm,
    "Cloud9am": Cloud9am,
    "Cloud3pm": Cloud3pm,
    "Temp9am": Temp9am,
    "Temp3pm": Temp3pm,
    "RainToday": RainToday,
    "Temp_Diff": Temp_Diff,
    "Month": Month
})

X_input = pd.DataFrame([row])
X_scaled = scaler.transform(X_input)

# ===============================
# MODEL SELECTION & PREDICTION
# ===============================
st.subheader("📌 Chọn mô hình")
model_choice = st.radio("Model", ["Random Forest", "KNN"])

if st.button("🔍 Dự đoán"):
    model = rf_model if model_choice == "Random Forest" else knn_model
    y_pred = model.predict(X_scaled)[0]
    prob = model.predict_proba(X_scaled)[0][1]

    if y_pred == 1:
        st.success(f"🌧️ **Ngày mai có khả năng mưa** — Xác suất: {prob:.2f}")
    else:
        st.info(f"☀️ **Ngày mai không mưa** — Xác suất mưa: {prob:.2f}")

st.markdown("---")
st.caption("© 2025 RainTomorrow Prediction – Streamlit Demo")
