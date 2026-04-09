# 🫀 Stroke Analytics System

> A modular Python CLI application that analyzes 172,000 simulated stroke patient records — running 11 statistical queries on risk factors like hypertension, smoking, and heart disease, with results saved to CSV. Built without Pandas or NumPy.

---

## 📌 Overview

This project is a Python-based stroke data analytics system designed to assist clinicians in monitoring patient vital signs and lifestyle factors to help prevent stroke-related fatalities. It processes a real-world-style dataset of 172,000 anonymized patient records and provides meaningful statistical insights through an interactive command-line interface.

The system is built entirely using Python's built-in capabilities — **no Pandas, NumPy, or CSV module** — demonstrating clean modular design and core programming concepts.

---

## 🗂️ Project Structure

```
stroke-analytics-system/
│
├── data.csv                  # Stroke dataset (172,000 records, 21 features)
├── dataset_module.py         # Loads CSV into a nested dictionary
├── query_module.py           # 11 statistical query functions + CSV export
├── ui_module.py              # Interactive CLI menu integrating all modules
├── main.ipynb                # Jupyter Notebook entry point
└── README.md
```

---

## ⚙️ Modules

### `dataset_module.py`
- Reads `data.csv` using Python's built-in file I/O (no external libraries)
- Parses records into a **nested dictionary** with incremental integer keys
- Handles missing files and malformed rows gracefully

### `query_module.py`
Contains 11 analytical query functions plus utility functions (`avg`, `median`, `mode`, `save_csv`):

| Query | Description |
|-------|-------------|
| Q1  | Avg / modal / median age — smokers with hypertension who had stroke |
| Q2  | Age stats + avg glucose level — heart disease patients with stroke |
| Q3  | Age stats by gender — hypertension with and without stroke |
| Q4  | Age stats by smoking habit — stroke vs no stroke |
| Q5  | Age stats by residence type (urban/rural) — stroke patients |
| Q6  | Dietary habits — stroke vs no stroke patients |
| Q7  | All patients with hypertension that resulted in stroke |
| Q8  | All hypertension patients — with and without stroke |
| Q9  | All heart disease patients who also had stroke |
| Q10 | Descriptive statistics (mean, std dev, min, max, 25/50/75%) for any feature |
| Q11 | Average sleep hours — stroke vs no stroke patients |

All results are saved automatically as `.csv` files.

### `ui_module.py`
- Interactive menu-driven CLI (queries 1–11 + exit option)
- Displays results in a clean, readable table format
- Handles invalid inputs without crashing
- Integrates `dataset_module` and `query_module` seamlessly

### `main.ipynb`
- Jupyter Notebook entry point
- Single cell that imports and runs `ui_module.main()`
- Displays query results inline below each selection

---

## 🚀 Getting Started

### Prerequisites
- Python 3.x
- Jupyter Notebook (for running `main.ipynb`)

Install Jupyter if not already installed:
```bash
pip install notebook
```

### Running the Application

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/stroke-analytics-system.git
   cd stroke-analytics-system
   ```

2. Make sure `data.csv` is in the same folder as all `.py` files.

3. **Option A — Jupyter Notebook (recommended):**
   ```bash
   jupyter notebook main.ipynb
   ```
   Run the single code cell. The query menu will appear below it.

4. **Option B — VS Code / Terminal:**
   ```bash
   python ui_module.py
   ```

5. Select a query number (1–11) or enter `0` to exit. Results are displayed in the terminal and saved as CSV files in the project folder.

---

## 📊 Dataset

- **Source:** [Stroke Predictions Dataset – Kaggle (ankushpanday1)](https://www.kaggle.com/datasets/ankushpanday1/stroke-predictions-dataset-of-indians)
- **Records:** 172,000 simulated patient entries
- **Features (21):** Age, Gender, Hypertension, Heart Disease, Smoking Status, BMI, Average Glucose Level, Sleep Hours, Dietary Habits, Physical Activity, Stroke Occurrence, Stroke Risk Score, Region, and more

---

## 📁 Output Files

Each query saves its results as a CSV file:

```
query1_smokers_hypertension_stroke_age.csv
query2_heart_disease_stroke_stats.csv
query3_hypertension_age_summary.csv
query4_smokers_age_summary.csv
query5_residence_stroke_age_summary.csv
query6_dietary_habits_stroke.csv
query7_hypertension_stroke_patients.csv
query8_hypertension_all_stroke_status.csv
query9_heart_disease_stroke_patients.csv
query10_age_statistics.csv
query11_sleep_hours_stroke.csv
```

---

## 🔒 Constraints & Rules

- ❌ No Pandas, NumPy, or CSV module used in `dataset_module`
- ✅ Pure Python file I/O for data loading
- ✅ All statistics computed from scratch (mean, median, mode, std dev, percentiles)
- ✅ Exception handling throughout — no crashes on bad input or missing files

---

## 💡 Possible Extensions

- GUI using `tkinter` or a web interface with `Flask`
- Real-time data integration from Electronic Health Records (EHR)
- Predictive stroke risk modeling using `scikit-learn`
- Replace incremental IDs with UUIDs or original dataset IDs for scalability

---

## 🤝 Acknowledgements

Dataset provided via Kaggle. Project developed as part of the *Programming Concepts and Practice* module (Level 7).

---

## 📄 License

This project is for educational purposes. Feel free to fork and build on it.

## Author

- NAME : VAUTREY AKSHIT
- EMAIL : vautreyakshit@gmail.com
