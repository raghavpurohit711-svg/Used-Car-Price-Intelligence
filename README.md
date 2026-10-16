# 🚗 Used Car Price Intelligence — Arbitrage Engine

A machine learning pipeline that scrapes live used-car listings, cleans the data, trains a price prediction model, and surfaces **mispriced (undervalued) deals** through an interactive web app.

---

## ✨ Features

- **Web Scraper** — Selenium-based scraper targeting [Cars24](https://www.cars24.com/) with infinite-scroll handling and deduplication
- **Data Cleaning Pipeline** — Structured notebooks for raw data processing and feature engineering
- **ML Model** — CatBoost regression model trained to predict fair market value (saved as `arbitrage_model.pkl`)
- **Streamlit App** — Instant valuation UI where users enter car details and get an estimated fair market price in ₹

---

## 🗂️ Project Structure

```
Used Car Arbitrage/
├── Notebooks/
│   ├── 01_Scraper_Testing_1.ipynb   # Scraper prototyping
│   ├── 02_data_cleaning.ipynb       # Data preprocessing & feature engineering
│   └── 03_model_training.ipynb      # Model training & evaluation
├── src/
│   ├── app/
│   │   └── app.py                   # Streamlit web application
│   └── data/
│       └── scraper.py               # Production scraper
├── data/
│   ├── raw/                         # Raw scraped CSV files
│   └── Processed/                   # Cleaned datasets
├── models/
│   └── arbitrage_model.pkl          # Trained CatBoost model
└── requirements.txt
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/used-car-price-intelligence.git
cd used-car-price-intelligence
```

### 2. Create a virtual environment & install dependencies

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r "Used Car Arbitrage/requirements.txt"
```

### 3. Run the Streamlit app

> Make sure you are inside the `Used Car Arbitrage/` directory.

```bash
cd "Used Car Arbitrage"
streamlit run src/app/app.py
```

---

## 🔄 Reproduce the Pipeline

| Step | Notebook / Script | Description |
|------|-------------------|-------------|
| 1 | `src/data/scraper.py` | Scrape live listings from Cars24 |
| 2 | `Notebooks/02_data_cleaning.ipynb` | Clean & engineer features |
| 3 | `Notebooks/03_model_training.ipynb` | Train & save the CatBoost model |

Run the notebooks in order if you want to retrain the model on fresh data.

---

## 🧠 Model Details

| Property | Value |
|----------|-------|
| Algorithm | CatBoost Regressor |
| Target | Car Price (₹) |
| Key Features | Brand, Model, Fuel Type, Transmission, Car Age, Km Driven, Km/Year |

---

## 🛠️ Tech Stack

- **Python** · Pandas · Scikit-learn · CatBoost
- **Selenium** · BeautifulSoup · lxml
- **Streamlit** · Joblib

---

## 📄 License

This project is for educational purposes. Scraping any website should comply with its Terms of Service.
