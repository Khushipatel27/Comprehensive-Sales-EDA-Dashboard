# 📊 Comprehensive Sales EDA Dashboard

An interactive Streamlit dashboard for performing **exploratory data analysis** on sales data using the Superstore dataset. Gain actionable insights through detailed statistical summaries, visualizations, and key business metrics.

## 🌟 Features

### 📋 Dataset Overview
- Full dataset information and statistical summary
- Preview and explore sample data with dark-themed tables
- Identify missing values, duplicates, and basic data integrity checks
- Key metric summaries (Total Sales, Total Profit, Average Profit Margin, etc.)

### 📊 Yearly and Category Analysis
- Year-over-year sales and profit comparisons
- Monthly and quarterly trend visualizations
- Product category and sub-category performance insights
- Regional and segment-wise analysis

### 🔍 Advanced Analytics
- Correlation and distribution analysis
- Customer segmentation insights
- Quantity vs. Profit vs. Discount visualizations
- Heatmaps for metric relationships
- Seasonal and trend pattern identification

## 🚀 Quick Start

### Prerequisites

```bash
pip install streamlit pandas matplotlib seaborn plotly
```

## Installation

1. Clone the repository
   ```
   git clone https://github.com/Khushipatel27/sales-eda-dashboard.git
   cd sales-eda-dashboard
   ```
2. Install dependencies
   ```
   pip install -r requirements.txt
   ```
3. Run the dashboard
   ```
   streamlit run dashboard.py
   ```
4. Access the application
- Open your browser and go to http://localhost:8501

## Project Structure
```
sales-eda-dashboard/
│
├── dashboard.py                 # Main Streamlit application
├── index.ipynb                  # Jupyter notebook for detailed analysis
├── Dataset_Superstore.csv       # Superstore dataset
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation
└── screenshots/                 # Sample visualizations
    ├── overview.png
    ├── yearly_analysis.png
    └── correlation_heatmap.png
```

## 📊 Dataset Information

The Superstore dataset contains **9,994 records** with columns such as:

| Column        | Description                                   |
|---------------|-----------------------------------------------|
| Order Info    | Row ID, Order ID, Order Date, Ship Date, Ship Mode |
| Customer Info | Customer ID, Customer Name, Segment          |
| Location      | Country, City, State, Postal Code, Region    |
| Product Info  | Product ID, Category, Sub-Category, Product Name |
| Metrics       | Sales, Quantity, Discount, Profit            |

## 🎛️ Dashboard Screenshots


<img width="3839" height="1961" alt="Screenshot 2025-09-06 144657" src="https://github.com/user-attachments/assets/332df41d-9cbe-4785-bf3b-626ee4f24edc" />
<img width="3714" height="1971" alt="Screenshot 2025-09-06 144824" src="https://github.com/user-attachments/assets/c2537761-389d-474c-bff8-95aecd30a456" />
<img width="3066" height="1454" alt="Screenshot 2025-09-06 144834" src="https://github.com/user-attachments/assets/c104aa6c-b9ba-43d2-9fb9-55530e1ce3e3" />
<img width="3062" height="1821" alt="Screenshot 2025-09-06 144855" src="https://github.com/user-attachments/assets/20dbfea7-584f-4e98-845e-654bd41d0e43" />
<img width="3049" height="1900" alt="Screenshot 2025-09-06 144921" src="https://github.com/user-attachments/assets/2222ef3d-1516-4049-bf6a-16e80a1a1baf" />
<img width="3088" height="1890" alt="Screenshot 2025-09-06 145002" src="https://github.com/user-attachments/assets/d5a11bd9-a4cc-4cfb-8033-6cdaf9ae539e" />
<img width="3134" height="1855" alt="Screenshot 2025-09-06 145015" src="https://github.com/user-attachments/assets/8ec50a70-0a15-4187-a1ea-be85ea7bd9b8" />
<img width="2947" height="1581" alt="Screenshot 2025-09-06 145046" src="https://github.com/user-attachments/assets/49a3d30e-a2bf-48ab-9804-2ee5cb2ea95c" />
<img width="2385" height="1446" alt="Screenshot 2025-09-06 145111" src="https://github.com/user-attachments/assets/1dbdd7e8-36bb-40e0-955c-a5dba3298742" />
<img width="2810" height="1442" alt="Screenshot 2025-09-06 145147" src="https://github.com/user-attachments/assets/00dcafe7-6997-4f34-903b-54adbf884159" />
<img width="2661" height="1503" alt="Screenshot 2025-09-06 145154" src="https://github.com/user-attachments/assets/c70626c4-fbc4-4f9e-96ca-102220329a54" />
<img width="623" height="1647" alt="Screenshot 2025-09-06 145205" src="https://github.com/user-attachments/assets/f19b468a-bc79-463d-b36e-8e951c6db7d7" />


## Contributing

1. Fork the repository
2. Create a feature branch (git checkout -b feature/NewFeature)
3. Commit your changes (git commit -m 'Add NewFeature')
4. Push to the branch (git push origin feature/NewFeature)
5. Open a Pull Request

## Run the dashboard
```
streamlit run app1.py
```

















