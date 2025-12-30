# Weather-forecasting-model
# 🌦️ RainTomorrow – Dự báo mưa bằng Học máy

## 1. Giới thiệu đề tài

### 1.1. Bài toán
Dự báo mưa là một bài toán quan trọng trong lĩnh vực khí tượng, có ảnh hưởng trực tiếp đến nông nghiệp, giao thông, quản lý tài nguyên nước và phòng chống thiên tai.  
Trong đề tài này, bài toán được đặt ra là **dự đoán khả năng xảy ra mưa vào ngày hôm sau (RainTomorrow)** dựa trên các thông tin thời tiết được ghi nhận trong ngày hiện tại.

Đây là một **bài toán phân loại nhị phân (Binary Classification)** với hai lớp:
- `Yes`: Có mưa vào ngày hôm sau  
- `No`: Không mưa vào ngày hôm sau  

---

### 1.2. Mục tiêu
- Khai phá và phân tích mối quan hệ giữa các yếu tố thời tiết và khả năng xảy ra mưa
- Trực quan hóa dữ liệu để rút ra các quy luật khí tượng quan trọng
- Xây dựng và so sánh các mô hình học máy để dự báo RainTomorrow
- Đánh giá mô hình bằng các chỉ số phù hợp, đặc biệt chú trọng khả năng phát hiện ngày mưa

---

## 2. Dataset

### 2.1. Nguồn dữ liệu
Bộ dữ liệu được sử dụng là **WeatherAUS** – dữ liệu thời tiết Australia, được sử dụng phổ biến trong các bài toán dự báo mưa.

- Nguồn: Kaggle  
- Link tải dataset:  
  https://www.kaggle.com/datasets/jsphyg/weather-dataset-rattle-package

> Do dung lượng lớn, dataset **không được đẩy lên GitHub**. Người dùng cần tải thủ công theo link trên.

---

### 2.2. Mô tả dữ liệu
- Mỗi dòng dữ liệu tương ứng với **một ngày quan sát thời tiết** tại một địa điểm
- Biến mục tiêu: `RainTomorrow` (Yes/No)
- Dữ liệu gồm các nhóm đặc trưng chính:
  - Nhiệt độ (MinTemp, MaxTemp, Temp9am, Temp3pm)
  - Độ ẩm (Humidity9am, Humidity3pm)
  - Áp suất (Pressure9am, Pressure3pm)
  - Mưa/nắng (Rainfall, Sunshine, Evaporation)
  - Gió (hướng và tốc độ gió)
  - Mây che phủ (Cloud9am, Cloud3pm)
  - Thời gian & địa điểm (Date, Location)

Danh sách chi tiết các feature được trình bày trong báo cáo.

---

## 3. Pipeline xử lý dữ liệu và huấn luyện mô hình

Pipeline tổng thể của đề tài gồm các bước sau:

### 3.1. Phân tích dữ liệu ban đầu (EDA)
- Kiểm tra kích thước dữ liệu, kiểu dữ liệu
- Phân tích phân bố các biến số
- Phát hiện dữ liệu thiếu và giá trị bất thường
- Trực quan hóa mối quan hệ giữa các feature và RainTomorrow

---

### 3.2. Tiền xử lý dữ liệu
- **Xử lý missing values**:
  - Loại bỏ các hàng thiếu quá nhiều cột
  - Điền median/mode cho các cột thiếu ít
  - Áp dụng MICE (IterativeImputer) cho các cột numeric quan trọng
- **Xử lý ngoại lệ**:
  - Ràng buộc miền giá trị hợp lý (ví dụ: lượng mưa, giờ nắng không âm)
- **Mã hóa biến phân loại**:
  - RainToday, RainTomorrow: Yes → 1, No → 0
  - Hướng gió: Label Encoding
- **Xử lý thời gian**:
  - Trích xuất `Month` từ `Date` để phản ánh yếu tố mùa vụ
- **Chuẩn hóa dữ liệu**:
  - Sử dụng StandardScaler cho KNN
  - Random Forest dùng dữ liệu gốc (không bắt buộc scale)

---

### 3.3. Huấn luyện mô hình
- Chia dữ liệu thành tập huấn luyện và tập kiểm tra
- Huấn luyện từng mô hình riêng biệt
- Đánh giá trên tập test để đảm bảo tính khách quan

---

## 4. Mô hình sử dụng

### 4.1. K-Nearest Neighbors (KNN)
KNN dự đoán nhãn của một mẫu mới dựa trên nhãn của K mẫu gần nhất trong không gian đặc trưng.

**Lý do chọn KNN**:
- Đơn giản, trực quan
- Là mô hình baseline để so sánh
- Giúp đánh giá mức độ phân tách tự nhiên của dữ liệu

---

### 4.2. Random Forest (RF)
Random Forest là mô hình ensemble kết hợp nhiều cây quyết định độc lập thông qua bootstrap sampling và chọn đặc trưng ngẫu nhiên.

**Lý do chọn Random Forest**:
- Học tốt các mối quan hệ phi tuyến
- Ổn định, ít overfitting
- Ít nhạy với nhiễu và outlier
- Cung cấp feature importance để giải thích mô hình

---

### 4.3. So sánh ưu / nhược điểm các mô hình

| Mô hình | Ưu điểm | Nhược điểm |
|---|---|---|
| KNN | Đơn giản, dễ hiểu, không cần train phức tạp | Nhạy với nhiễu, phụ thuộc scaling, kém hiệu quả khi dữ liệu lớn |
| Random Forest | Hiệu quả cao, học phi tuyến tốt, ổn định | Khó giải thích chi tiết từng quyết định, model nặng hơn |

---

## 5. Kết quả và đánh giá mô hình

Các mô hình được đánh giá bằng nhiều chỉ số:

- **Accuracy**: Tỷ lệ dự đoán đúng tổng thể
- **Precision**: Độ chính xác khi dự đoán mưa
- **Recall**: Khả năng phát hiện đúng ngày mưa (rất quan trọng)
- **F1-score**: Cân bằng giữa Precision và Recall
- **Confusion Matrix**: Phân tích chi tiết các loại dự đoán sai/đúng
- **ROC-AUC**: Khả năng phân biệt hai lớp

Kết quả cho thấy:
- Random Forest đạt hiệu quả tổng thể tốt hơn KNN
- Các feature như Humidity3pm, Cloud3pm, Pressure3pm có ảnh hưởng lớn đến RainTomorrow

(Chi tiết số liệu được trình bày trong notebook và báo cáo)

---

## 6. Hướng dẫn chạy dự án

### 6.1. Cài môi trường hoặc chạy trực tiếp bằng colab ở dưới
(https://colab.research.google.com/)

Cài các thư viện cần thiết:
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random
import io
import pickle
import os
