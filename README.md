# 📊 KPI Performance Analysis Tool

A comprehensive web-based analytics solution designed to compare pre- and post-period KPI performance. This tool enables users to upload raw data files, select date ranges, generate detailed KPI reports, visualize trends through interactive dashboards, and export insights in CSV or Excel formats.

## ✨ Features

- **📁 File Upload**: Support for CSV and Excel (.xlsx, .xls) file formats
- **📅 Date Range Selection**: Define custom pre-period and post-period date ranges
- **📊 KPI Analysis**: 
  - Automatic calculation of mean, median, standard deviation, min, max
  - Pre vs Post period comparison
  - Change detection with percentage calculations
  - Total aggregations
- **📈 Interactive Dashboards**: Dynamic line charts for trend visualization using Chart.js
- **💾 Export Functionality**: 
  - CSV export with comprehensive analysis results
  - Excel export with multiple sheets (Summary & Detailed)
- **🎨 Modern UI**: Clean, responsive interface with step-by-step workflow
- **⚡ Real-time Analysis**: Fast data processing with pandas

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Sneha7306876/KPI-Monitoring-Reporting-System.git
cd KPI-Monitoring-Reporting-System
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your web browser and navigate to:
```
http://localhost:5000
```

## 📖 How to Use

### Step 1: Upload Data File
- Click on the upload area or drag and drop your CSV/Excel file
- The system will automatically detect columns and display a preview
- Supported formats: `.csv`, `.xlsx`, `.xls`

### Step 2: Configure Analysis
1. **Select Date Column**: Choose the column containing date information
2. **Select KPI Columns**: Check the metrics you want to analyze
3. **Define Time Periods**:
   - **Pre-Period**: Set start and end dates for the baseline period
   - **Post-Period**: Set start and end dates for the comparison period
4. Click **Analyze KPIs** to process the data

### Step 3: View Results & Export
- Review the **KPI Summary Cards** showing key metrics and changes
- Examine **Detailed Statistics** with comprehensive statistical measures
- Explore **Trend Charts** for visual time-series analysis
- Export results using **Export to CSV** or **Export to Excel** buttons

## 📊 Sample Data

A sample dataset (`sample_data.csv`) is included with the following structure:
- Date: Transaction date
- Revenue: Daily revenue
- Orders: Number of orders
- Customers: Number of customers
- Conversion_Rate: Conversion percentage
- Average_Order_Value: Average value per order

Example usage:
1. Upload `sample_data.csv`
2. Select "Date" as the date column
3. Check all KPI columns (Revenue, Orders, Customers, etc.)
4. Set Pre-Period: 2024-01-01 to 2024-01-15
5. Set Post-Period: 2024-02-01 to 2024-02-15
6. Analyze and view results

## 🔧 Technical Architecture

### Backend (Python/Flask)
- **Framework**: Flask 3.0.0
- **Data Processing**: pandas, numpy
- **File Handling**: openpyxl for Excel, Werkzeug for secure uploads
- **Date Handling**: python-dateutil

### Frontend
- **HTML5/CSS3**: Modern, responsive design
- **JavaScript**: Vanilla JS for interactivity
- **Visualization**: Chart.js for interactive charts
- **Design**: Gradient-based theme with card layouts

### API Endpoints
- `GET /`: Main application interface
- `POST /upload`: File upload and data preview
- `POST /analyze`: KPI analysis computation
- `POST /export/<format>`: Export results (csv/excel)

## 📁 Project Structure

```
KPI-Monitoring-Reporting-System/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── sample_data.csv       # Sample dataset
├── templates/
│   └── index.html        # Frontend interface
├── uploads/              # Uploaded files storage
│   └── .gitkeep
├── .gitignore
└── README.md
```

## 🔒 Security Features

- File type validation (only CSV and Excel allowed)
- Secure filename handling with Werkzeug
- File size limit (16MB max)
- Input sanitization for user-provided data

## 📈 KPI Metrics Calculated

For each selected KPI, the tool calculates:

### Summary Metrics
- **Pre-Period Mean**: Average value in the pre-period
- **Post-Period Mean**: Average value in the post-period
- **Change**: Absolute difference (Post - Pre)
- **Change %**: Percentage change
- **Pre-Period Total**: Sum of all values in pre-period
- **Post-Period Total**: Sum of all values in post-period

### Detailed Statistics
- **Mean**: Average value
- **Median**: Middle value
- **Standard Deviation**: Measure of variability
- **Min**: Minimum value
- **Max**: Maximum value
- **Count**: Number of data points

## 🌟 Use Cases

1. **Marketing Campaign Analysis**: Compare KPIs before and after campaign launches
2. **Product Launch Impact**: Measure performance changes after new product releases
3. **Operational Efficiency**: Assess impact of process improvements
4. **Seasonal Analysis**: Compare different time periods for seasonal trends
5. **A/B Testing Results**: Evaluate test results with statistical analysis

## 🛠️ Customization

### Adding New KPI Calculations
Edit the `calculate_kpis()` function in `app.py` to add custom metrics:
```python
# Example: Add custom calculation
custom_metric = (post_mean - pre_mean) / pre_values.std()
results['summary'][kpi]['custom_metric'] = round(custom_metric, 2)
```

### Styling Customization
Modify the `<style>` section in `templates/index.html` to customize colors, fonts, and layout.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

Sneha7306876

## 🐛 Issues and Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

**Built with ❤️ using Flask and Chart.js**