import streamlit as st

st.set_page_config(
    page_title="RainTomorrow Demo",
    layout="centered"
)

st.title("🌦️ RainTomorrow – Streamlit Demo")

st.write("""
Ứng dụng này dùng để **demo giao diện Streamlit**  
cho bài toán dự báo mưa ngày hôm sau.
""")

st.subheader("🔧 Input mẫu")
humidity = st.slider("Humidity3pm (%)", 0, 100, 70)
cloud = st.slider("Cloud3pm (0–8)", 0, 8, 6)
pressure = st.slider("Pressure3pm (hPa)", 980, 1045, 1008)

st.write("### Giá trị đã nhập")
st.write({
    "Humidity3pm": humidity,
    "Cloud3pm": cloud,
    "Pressure3pm": pressure
})

if st.button("🔍 Dự đoán (demo)"):
    st.success("🌧️ Khả năng mưa: **CAO** (demo)")
