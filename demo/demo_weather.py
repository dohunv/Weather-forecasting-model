%%writefile app.py
import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("weatherAUS.csv")
    return df

df = load_data()

st.set_page_config(page_title="🌧️ Dự Báo Mưa Ngày Mai", layout="centered")
st.title("🌦️ Dự Báo Mưa Ngày Mai tại Úc")
st.markdown("Nhập các thông số thời tiết hôm nay để dự đoán ngày mai có mưa không.")

# Nếu chưa có model thì train nhanh và lưu
if not os.path.exists("model.pkl") or not os.path.exists("scaler.pkl"):
    st.info("Đang chuẩn bị mô hình lần đầu... (chỉ mất ~30 giây)")
    
    # Tiền xử lý nhanh
    data = df.copy()
    data = data.dropna(subset=['RainTomorrow'])
    
    # Feature cơ bản
    features = ['MinTemp', 'MaxTemp', 'Rainfall', 'Evaporation', 'Sunshine',
                'WindGustSpeed', 'Humidity9am', 'Humidity3pm', 'Pressure9am',
                'Pressure3pm', 'Cloud9am', 'Cloud3pm', 'Temp9am', 'Temp3pm']
    
    data = data[features + ['RainToday', 'RainTomorrow']].dropna()
    
    # Encode RainToday
    data['RainToday'] = data['RainToday'].map({'No': 0, 'Yes': 1})
    data['RainTomorrow'] = data['RainTomorrow'].map({'No': 0, 'Yes': 1})
    
    X = data[features + ['RainToday']]
    y = data['RainTomorrow']
    
    # Train test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    # Lưu model và scaler
    pickle.dump(model, open("model.pkl", "wb"))
    pickle.dump(scaler, open("scaler.pkl", "wb"))
    pickle.dump(features + ['RainToday'], open("feature_names.pkl", "wb"))
    
    st.success("Mô hình đã sẵn sàng!")

# Load model
model = pickle.load(open("model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))
feature_names = pickle.load(open("feature_names.pkl", "rb"))

# Input form
st.subheader("📊 Nhập thông tin thời tiết hôm nay")

col1, col2 = st.columns(2)

with col1:
    MinTemp = st.slider("Nhiệt độ thấp nhất (°C)", -10.0, 40.0, 15.0)
    MaxTemp = st.slider("Nhiệt độ cao nhất (°C)", 0.0, 50.0, 25.0)
    Rainfall = st.slider("Lượng mưa hôm nay (mm)", 0.0, 200.0, 0.0)
    Humidity9am = st.slider("Độ ẩm 9h sáng (%)", 0, 100, 70)
    Humidity3pm = st.slider("Độ ẩm 3h chiều (%)", 0, 100, 50)
    Pressure9am = st.slider("Áp suất 9h sáng (hPa)", 980.0, 1040.0, 1015.0)

with col2:
    Pressure3pm = st.slider("Áp suất 3h chiều (hPa)", 980.0, 1040.0, 1013.0)
    Cloud9am = st.slider("Mây che 9h sáng (0-8)", 0, 8, 4)
    Cloud3pm = st.slider("Mây che 3h chiều (0-8)", 0, 8, 4)
    WindGustSpeed = st.slider("Tốc độ gió giật (km/h)", 0, 130, 35)
    Sunshine = st.slider("Số giờ nắng", 0.0, 15.0, 7.0)
    RainToday = st.selectbox("Hôm nay có mưa không?", ["Không", "Có"])

RainToday = 1 if RainToday == "Có" else 0

# Tạo vector input
input_data = pd.DataFrame([{
    'MinTemp': MinTemp,
    'MaxTemp': MaxTemp,
    'Rainfall': Rainfall,
    'Evaporation': 5.0,  # giá trị trung bình
    'Sunshine': Sunshine,
    'WindGustSpeed': WindGustSpeed,
    'Humidity9am': Humidity9am,
    'Humidity3pm': Humidity3pm,
    'Pressure9am': Pressure9am,
    'Pressure3pm': Pressure3pm,
    'Cloud9am': Cloud9am,
    'Cloud3pm': Cloud3pm,
    'Temp9am': (MinTemp + MaxTemp)/2 * 0.8,
    'Temp3pm': (MinTemp + MaxTemp)/2 * 1.1,
    'RainToday': RainToday
}])

# Scale
input_scaled = scaler.transform(input_data)

if st.button("🔮 Dự đoán ngày mai có mưa không?"):
    pred = model.predict(input_scaled)[0]
    prob = model.predict_proba(input_scaled)[0][1]
    
    if pred == 1:
        st.error(f"🌧️ **NGÀY MAI SẼ MƯA**")
        st.write(f"Xác suất mưa: **{prob:.1%}**")
    else:
        st.success(f"☀️ **NGÀY MAI KHÔNG MƯA**")
        st.write(f"Xác suất mưa: **{prob:.1%}**")
    
    st.balloons()

st.markdown("---")
st.caption("Demo dự báo mưa sử dụng Random Forest trên dữ liệu WeatherAUS")
