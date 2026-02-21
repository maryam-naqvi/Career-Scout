# 🎯 CareerScout: Data Science Salary Intelligence

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-Machine%20Learning-orange.svg)

CareerScout is a full-stack Machine Learning web application designed to analyze and predict Data Science salaries. Trained on a 2025 dataset of over 93,000 real-world records, it provides both market intelligence dashboards and an interactive AI salary predictor with downloadable PDF reports.

## 🚀 Features
* **Market Dashboard:** Interactive charts displaying salary distributions, top-paying roles, and experience-level breakdowns.
* **AI Salary Predictor:** A Random Forest ML model that predicts expected salaries based on Job Title, Experience Level, and Remote Work Ratio.
* **PDF Report Generation:** Instantly exports the user's customized salary prediction and market context into a professional, multi-page PDF document.

## 📂 Project Architecture

We separated our application into a clean, 3-step pipeline:

1. `1_data_prep_and_eda.py` 
   * **Purpose:** Data Engineering. Cleans the raw CSV, removes massive outliers, calculates aggregates, and generates the static visualization charts (PNGs).
2. `2_model_training.py`
   * **Purpose:** Machine Learning. Loads the clean data, performs One-Hot Encoding, trains a `RandomForestRegressor`, evaluates metrics (MAE/R²) and exports the model as `.pkl` files.
3. `app.py`
   * **Purpose:** The Frontend. A Streamlit web application featuring a custom "GitHub Dark" aesthetic, interactive inputs, and `fpdf2` integration for report generation.

## 💻 Installation & Usage

**1. Clone the repository**
```bash
git clone [https://github.com/maryam-naqvi/Career-Scout.git](https://github.com/maryam-naqvi/Career-Scout.git)
cd Career-Scout
```

**2. Install dependencies**
```bash
pip install pandas matplotlib seaborn scikit-learn joblib streamlit fpdf2
```

**3. Run the application**
```bash
streamlit run app.py
```

## 👥 The Team
This project was built collaboratively by our ML Fellowship team:
* **Shahan:** Data Cleaning & Exploratory Data Analysis (EDA)
* **Ruhmma:** Project Research & Dataset Sourcing
* **Mahad:** Project Documentation
* **Maryam (Team Lead):** ML Pipeline Architecture, Streamlit Web Application & PDF Integration
