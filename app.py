"""
KPI Performance Analysis Tool - Main Application
A web-based analytics solution for comparing pre- and post-period KPI performance
"""

from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import numpy as np
from datetime import datetime
import os
import json
from werkzeug.utils import secure_filename
import io

import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'csv', 'xlsx', 'xls'}

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Store uploaded data in memory (in production, use a database with user isolation)
data_store = {}


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def load_data_file(filepath):
    """Load CSV or Excel file into pandas DataFrame"""
    ext = filepath.rsplit('.', 1)[1].lower()
    if ext == 'csv':
        return pd.read_csv(filepath)
    else:
        return pd.read_excel(filepath)


def calculate_kpis(df, date_col, kpi_cols, pre_start, pre_end, post_start, post_end):
    """
    Calculate KPIs for pre and post periods
    
    Args:
        df: DataFrame with data
        date_col: Name of the date column
        kpi_cols: List of KPI column names to analyze
        pre_start, pre_end: Pre-period date range
        post_start, post_end: Post-period date range
    
    Returns:
        Dictionary with KPI analysis results
    """
    # Convert date column to datetime
    df[date_col] = pd.to_datetime(df[date_col])
    
    # Filter data for pre and post periods
    pre_data = df[(df[date_col] >= pre_start) & (df[date_col] <= pre_end)]
    post_data = df[(df[date_col] >= post_start) & (df[date_col] <= post_end)]
    
    results = {
        'summary': {},
        'detailed': {},
        'trends': {},
        'pre_period': {'start': pre_start, 'end': pre_end, 'records': len(pre_data)},
        'post_period': {'start': post_start, 'end': post_end, 'records': len(post_data)}
    }
    
    for kpi in kpi_cols:
        if kpi not in df.columns or kpi == date_col:
            continue
            
        # Convert to numeric, coercing errors
        pre_values = pd.to_numeric(pre_data[kpi], errors='coerce').dropna()
        post_values = pd.to_numeric(post_data[kpi], errors='coerce').dropna()
        
        if len(pre_values) == 0 or len(post_values) == 0:
            continue
        
        pre_mean = pre_values.mean()
        post_mean = post_values.mean()
        change = post_mean - pre_mean
        change_pct = ((change / pre_mean) * 100) if pre_mean != 0 else 0
        
        results['summary'][kpi] = {
            'pre_mean': float(round(pre_mean, 2)),
            'post_mean': float(round(post_mean, 2)),
            'change': float(round(change, 2)),
            'change_pct': float(round(change_pct, 2)),
            'pre_total': float(round(pre_values.sum(), 2)),
            'post_total': float(round(post_values.sum(), 2))
        }
        
        # Detailed statistics
        results['detailed'][kpi] = {
            'pre': {
                'mean': float(round(pre_values.mean(), 2)),
                'median': float(round(pre_values.median(), 2)),
                'std': float(round(pre_values.std(), 2)),
                'min': float(round(pre_values.min(), 2)),
                'max': float(round(pre_values.max(), 2)),
                'count': int(len(pre_values))
            },
            'post': {
                'mean': float(round(post_values.mean(), 2)),
                'median': float(round(post_values.median(), 2)),
                'std': float(round(post_values.std(), 2)),
                'min': float(round(post_values.min(), 2)),
                'max': float(round(post_values.max(), 2)),
                'count': int(len(post_values))
            }
        }
        
        # Trend data for visualization
        trend_data = df[[date_col, kpi]].copy()
        trend_data[kpi] = pd.to_numeric(trend_data[kpi], errors='coerce')
        trend_data = trend_data.dropna()
        trend_data = trend_data.sort_values(date_col)
        
        results['trends'][kpi] = {
            'dates': trend_data[date_col].dt.strftime('%Y-%m-%d').tolist(),
            'values': [float(v) if not pd.isna(v) else None for v in trend_data[kpi].tolist()]
        }
    
    return results


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed. Please upload CSV or Excel files.'}), 400
    
    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Load and preview data
        df = load_data_file(filepath)
        
        # Store data info with unique ID
        file_id = str(uuid.uuid4())
        data_store[file_id] = {
            'filepath': filepath,
            'columns': df.columns.tolist(),
            'rows': len(df),
            'preview': df.head(10).to_dict('records')
        }
        
        return jsonify({
            'success': True,
            'file_id': file_id,
            'columns': df.columns.tolist(),
            'rows': len(df),
            'preview': df.head(10).to_dict('records')
        })
    
    except Exception as e:
        return jsonify({'error': f'Error processing file: {str(e)}'}), 500


@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze KPIs for selected date ranges"""
    try:
        data = request.json
        file_id = data.get('file_id')
        date_col = data.get('date_column')
        kpi_cols = data.get('kpi_columns', [])
        pre_start = data.get('pre_start')
        pre_end = data.get('pre_end')
        post_start = data.get('post_start')
        post_end = data.get('post_end')
        
        if not all([file_id, date_col, kpi_cols, pre_start, pre_end, post_start, post_end]):
            return jsonify({'error': 'Missing required parameters'}), 400
        
        if file_id not in data_store:
            return jsonify({'error': 'File not found. Please upload again.'}), 404
        
        # Load data
        df = load_data_file(data_store[file_id]['filepath'])
        
        # Calculate KPIs
        results = calculate_kpis(
            df, date_col, kpi_cols,
            pre_start, pre_end, post_start, post_end
        )
        
        return jsonify({
            'success': True,
            'results': results
        })
    
    except Exception as e:
        return jsonify({'error': f'Error analyzing data: {str(e)}'}), 500


@app.route('/export/<format>', methods=['POST'])
def export_data(format):
    """Export analysis results to CSV or Excel"""
    try:
        data = request.json
        results = data.get('results')
        
        if not results:
            return jsonify({'error': 'No results to export'}), 400
        
        # Create DataFrame from summary results
        summary_data = []
        for kpi, values in results.get('summary', {}).items():
            summary_data.append({
                'KPI': kpi,
                'Pre-Period Mean': values['pre_mean'],
                'Post-Period Mean': values['post_mean'],
                'Change': values['change'],
                'Change %': values['change_pct'],
                'Pre-Period Total': values['pre_total'],
                'Post-Period Total': values['post_total']
            })
        
        df_summary = pd.DataFrame(summary_data)
        
        # Create detailed DataFrame
        detailed_data = []
        for kpi, stats in results.get('detailed', {}).items():
            detailed_data.append({
                'KPI': kpi,
                'Period': 'Pre',
                'Mean': stats['pre']['mean'],
                'Median': stats['pre']['median'],
                'Std Dev': stats['pre']['std'],
                'Min': stats['pre']['min'],
                'Max': stats['pre']['max'],
                'Count': stats['pre']['count']
            })
            detailed_data.append({
                'KPI': kpi,
                'Period': 'Post',
                'Mean': stats['post']['mean'],
                'Median': stats['post']['median'],
                'Std Dev': stats['post']['std'],
                'Min': stats['post']['min'],
                'Max': stats['post']['max'],
                'Count': stats['post']['count']
            })
        
        df_detailed = pd.DataFrame(detailed_data)
        
        # Export based on format
        output = io.BytesIO()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if format == 'csv':
            # Combine both dataframes with headers
            combined_csv = f"KPI Analysis Summary\n{df_summary.to_csv(index=False)}\n\nDetailed Statistics\n{df_detailed.to_csv(index=False)}"
            output.write(combined_csv.encode('utf-8'))
            output.seek(0)
            return send_file(
                output,
                mimetype='text/csv',
                as_attachment=True,
                download_name=f'kpi_analysis_{timestamp}.csv'
            )
        
        elif format == 'excel':
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_summary.to_excel(writer, sheet_name='Summary', index=False)
                df_detailed.to_excel(writer, sheet_name='Detailed', index=False)
            output.seek(0)
            return send_file(
                output,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                as_attachment=True,
                download_name=f'kpi_analysis_{timestamp}.xlsx'
            )
        
        else:
            return jsonify({'error': 'Invalid export format'}), 400
    
    except Exception as e:
        return jsonify({'error': f'Error exporting data: {str(e)}'}), 500


if __name__ == '__main__':
    # For development only - set debug=False in production
    import os
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
