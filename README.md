# 📊 Unemployment Analysis with Python

** Data Science Project 2 **

A comprehensive Python-based analysis of unemployment trends in India, with a focus on the impact of COVID-19, state-wise patterns, and rural vs urban comparisons.

---

## 📁 Datasets

| File | Description | Period |
|------|-------------|--------|
| `Unemployment_Rate_upto_11_2020.csv` | State-level monthly data with geo info | Jan–Nov 2020 |
| `Unemployment_in_India.csv` | Rural & Urban breakdown by state | May 2019–Jun 2020 |

---

## 🔍 Key Findings

| Metric | Value |
|--------|-------|
| Pre-COVID avg unemployment | 9.23% |
| During-COVID avg unemployment | 12.96% |
| COVID spike | +3.73 percentage points |
| Peak unemployment month | May 2020 — **23.2%** |
| Highest state avg | Haryana (27.5%) |
| Lowest state avg | Meghalaya (3.9%) |

---

## 📈 Visualizations

| Plot | Description |
|------|-------------|
| `01_national_trend.png` | National monthly unemployment trend with lockdown annotation |
| `02_covid_impact.png` | Pre vs During COVID comparison — national + top 12 states |
| `03_statewise_avg.png` | State-wise average unemployment bar chart |
| `04_heatmap_state_month.png` | State × Month heatmap showing COVID surge clearly |
| `05_rural_vs_urban.png` | Rural vs Urban unemployment trend lines |
| `06_participation_vs_unemployment.png` | Labour participation rate vs unemployment scatter plot |

---

## 🚀 How to Run

```bash
git clone https://github.com/sanjaikv2255/UnemploymentAnalysis
cd UnemploymentAnalysis

pip install pandas numpy matplotlib seaborn

jupyter notebook unemployment_analysis.ipynb
# or
python unemployment_analysis.py
```

---

## 🛠 Tech Stack

`Python` · `Pandas` · `NumPy` · `Matplotlib` · `Seaborn`

---

## 📌 Key Conclusions

- **COVID-19 caused a massive unemployment spike** — India went from ~9% to 23% in just 2 months
- **May 2020** was the worst month, coinciding with the strictest national lockdown
- **Urban workers** were hit harder than rural workers due to service/industry shutdowns
- **Haryana, Tripura, and Himachal Pradesh** were the most severely affected states
- By **October 2020**, unemployment was recovering toward pre-COVID levels as restrictions eased

---

*Made by [Sanjai KV](https://github.com/sanjaikv2255) 
