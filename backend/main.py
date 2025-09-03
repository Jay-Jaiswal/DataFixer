import pandas as pd
import numpy as np
import json
from io import StringIO
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from detection import DataIssueDetector
from solution import DataIssueSolver

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "message": "Data Cleaner API running.",
        "endpoints": {
            "analyze": "/api/upload-and-analyze/ (POST multipart/form-data file=...)",
            "clean": "/api/clean-file/ (POST multipart/form-data file=...)",
            "preview_cleaning": "/api/preview-cleaning/ (POST multipart/form-data file=...)",
            "docs": "/docs"
        },
        "cleaning_options": {
            "missing_threshold": "Configurable threshold for dropping columns (default: 0.8 = 80%)",
            "fill_strategy": "auto/drop/fill - controls how to handle high-missing-value columns",
            "preview_mode": "Use /api/preview-cleaning/ to see what will happen before cleaning"
        }
    }


@app.get("/health")
async def health():
    return {"status": "ok"}


def generate_data_report(df: pd.DataFrame) -> dict:
    report = {
        'overview': {
            'rows': int(df.shape[0]), 
            'columns': int(df.shape[1]),
            'total_missing_values': int(df.isnull().sum().sum()), 
            'duplicate_rows': int(df.duplicated().sum())
        },
        'column_details': {}
    }
    
    from collections import Counter
    column_counts = Counter(df.columns)
    
    for col in df.columns:
        col_data = df[col]
        missing_count = int(col_data.isnull().sum())
        details = {
            'dtype': str(col_data.dtype), 
            'missing_values': missing_count,
            'missing_percentage': float(round((missing_count / len(df)) * 100, 2)),
            'unique_values': int(col_data.nunique())
        }
        
        # Outlier detection for numeric columns
        details['outlier_count'] = 0
        if pd.api.types.is_numeric_dtype(col_data.dtype):
            try:
                q1, q3 = col_data.quantile(0.25), col_data.quantile(0.75)
                iqr = q3 - q1
                lower_bound, upper_bound = q1 - 1.5 * iqr, q3 + 1.5 * iqr
                outliers = col_data[(col_data < lower_bound) | (col_data > upper_bound)]
                details['outlier_count'] = int(len(outliers))
            except Exception:
                details['outlier_count'] = 0
        
        details['mixed_capitalization'] = False
        details['is_numeric_like'] = False
        
        if pd.api.types.is_object_dtype(col_data.dtype):
            try:
                lower_unique = col_data.dropna().str.lower().nunique()
                if details['unique_values'] > 0:
                    diff_ratio = (details['unique_values'] - lower_unique) / details['unique_values']
                else:
                    diff_ratio = 0
                if diff_ratio >= 0.2:
                    details['mixed_capitalization'] = True
            except Exception:
                details['mixed_capitalization'] = False
            
            try:
                numeric_vals = pd.to_numeric(col_data, errors='coerce')
                if (1 - numeric_vals.isnull().sum() / max(1, len(col_data))) * 100 > 90:
                    details['is_numeric_like'] = True
            except Exception:
                details['is_numeric_like'] = False
        
        reasons = []
        if details['missing_percentage'] > 20:
            reasons.append(f"High missing rate: {details['missing_percentage']}%")
        if details.get('mixed_capitalization'):
            reasons.append("Inconsistent capitalization")
        if details.get('outlier_count', 0) > 0:
            reasons.append(f"{details.get('outlier_count', 0)} potential outliers")
        if details.get('is_numeric_like'):
            reasons.append("Numeric-looking strings")
        
        if column_counts[col] > 1:
            details['has_problem'] = True
            details['reasons'] = reasons + [f"Duplicate column name: {col}"]
        else:
            details['has_problem'] = missing_count > 0
            details['reasons'] = reasons
        
        report['column_details'][col] = details
    
    return report


def generate_recommendations(df: pd.DataFrame, report: dict) -> list:
    recommendations = []
    
    if report['overview']['duplicate_rows'] > 0:
        recommendations.append(f"Found {report['overview']['duplicate_rows']} duplicate rows. Consider removing them.")
    
    if report['overview']['total_missing_values'] > 0:
        recommendations.append("The dataset contains missing values. Consider a strategy to fill or remove them.")
    
    if any(col.lower().startswith('unnamed:') for col in df.columns):
        recommendations.append("The file seems to be missing proper headers.")
    
    for col_name, details in report['column_details'].items():
        if details['missing_percentage'] > 20:
            recommendations.append(f"Column '{col_name}' is {details['missing_percentage']}% empty. Consider dropping it.")
        if details.get('mixed_capitalization'):
            recommendations.append(f"Column '{col_name}' has inconsistent capitalization. Standardize it.")
        if details.get('is_numeric_like'):
            recommendations.append(f"Column '{col_name}' seems numeric but is stored as text. Convert its data type.")
        if details.get('outlier_count', 0) > 0:
            recommendations.append(f"Column '{col_name}' has {details['outlier_count']} potential outliers.")
    
    if not recommendations:
        recommendations.append("Good News: No major data quality issues found!")
    
    return recommendations


def perform_standard_cleaning(df: pd.DataFrame, 
                            missing_threshold: float = 0.8,
                            fill_strategy: str = 'auto') -> pd.DataFrame:
    """
    Clean the dataframe with intelligent handling of high-missing-value columns.
    
    Args:
        df: Input dataframe
        missing_threshold: Threshold above which columns are dropped (0.8 = 80%)
        fill_strategy: Strategy for filling missing values ('auto', 'drop', 'fill')
    
    Returns:
        Cleaned dataframe
    """
    df_cleaned = df.copy()
    
    # Remove duplicates
    df_cleaned.drop_duplicates(inplace=True)
    
    # Analyze missing values and handle high-missing columns
    missing_percentages = {}
    for col in df_cleaned.columns:
        missing_count = df_cleaned[col].isnull().sum()
        missing_percentage = missing_count / len(df_cleaned)
        missing_percentages[col] = missing_percentage
    
    # Handle columns with extremely high missing values
    columns_to_drop = []
    for col, missing_pct in missing_percentages.items():
        if missing_pct >= missing_threshold:
            columns_to_drop.append(col)
            print(f"Warning: Column '{col}' has {missing_pct*100:.1f}% missing values - will be dropped")
    
    # Drop high-missing columns if strategy allows
    if fill_strategy != 'fill' and columns_to_drop:
        df_cleaned = df_cleaned.drop(columns=columns_to_drop)
        print(f"Dropped {len(columns_to_drop)} columns with >{missing_threshold*100}% missing values")
    
    # Fill missing values for remaining numeric columns
    for col in df_cleaned.select_dtypes(include=np.number).columns:
        if df_cleaned[col].isnull().sum() > 0:
            try:
                # Try to fill with mean, but handle cases where all values might be NaN
                col_mean = df_cleaned[col].mean()
                if pd.isna(col_mean):
                    # If mean is NaN, try median
                    col_median = df_cleaned[col].median()
                    if pd.isna(col_median):
                        # If both mean and median are NaN, fill with 0
                        df_cleaned[col].fillna(0, inplace=True)
                        print(f"Warning: Column '{col}' had all NaN values - filled with 0")
                    else:
                        df_cleaned[col].fillna(col_median, inplace=True)
                        print(f"Column '{col}' filled with median due to mean being NaN")
                else:
                    df_cleaned[col].fillna(col_mean, inplace=True)
            except Exception as e:
                print(f"Error filling missing values in column '{col}': {e}")
                # Fallback: fill with 0
                df_cleaned[col].fillna(0, inplace=True)
    
    # Fill missing values for object columns
    for col in df_cleaned.select_dtypes(include=['object']).columns:
        if df_cleaned[col].isnull().sum() > 0:
            try:
                # Get non-null values for mode calculation
                non_null_values = df_cleaned[col].dropna()
                if len(non_null_values) > 0:
                    mode_value = non_null_values.mode()
                    if len(mode_value) > 0:
                        df_cleaned[col].fillna(mode_value[0], inplace=True)
                    else:
                        # If no mode, fill with "Unknown"
                        df_cleaned[col].fillna("Unknown", inplace=True)
                        print(f"Column '{col}' filled with 'Unknown' (no mode available)")
                else:
                    # All values are null, fill with "Unknown"
                    df_cleaned[col].fillna("Unknown", inplace=True)
                    print(f"Column '{col}' had all null values - filled with 'Unknown'")
            except Exception as e:
                print(f"Error filling missing values in column '{col}': {e}")
                # Fallback: fill with "Unknown"
                df_cleaned[col].fillna("Unknown", inplace=True)
    
    # Strip whitespace from object columns
    for col in df_cleaned.select_dtypes(include=['object']).columns:
        try:
            df_cleaned[col] = df_cleaned[col].astype(str).str.strip()
        except Exception as e:
            print(f"Error stripping whitespace from column '{col}': {e}")
    
    # Clean column names
    try:
        df_cleaned.columns = (df_cleaned.columns
                             .str.strip()
                             .str.lower()
                             .str.replace(' ', '_')
                             .str.replace(r'[^a-z0-9_]', '', regex=True))
    except Exception as e:
        print(f"Error cleaning column names: {e}")
    
    return df_cleaned


@app.post("/api/upload-and-analyze/")
async def upload_and_analyze(file: UploadFile = File(...)):
    try:
        content = await file.read()
        file_extension = file.filename.split('.')[-1].lower() if file.filename else ''
        
        if file_extension == 'csv':
            try:
                txt = content.decode('utf-8')
            except Exception:
                txt = content.decode('latin-1')
            df = pd.read_csv(StringIO(txt), sep=None, engine='python')
        elif file_extension == 'json':
            try:
                obj = json.loads(content.decode('utf-8'))
            except Exception:
                obj = json.loads(content.decode('latin-1'))
            if isinstance(obj, list):
                df = pd.DataFrame(obj)
            else:
                df = pd.json_normalize(obj)
        else:
            return JSONResponse(status_code=400, content={"message": "Unsupported file type"})
        
        report = generate_data_report(df)
        recommendations = generate_recommendations(df, report)
        preview = df.head().to_dict(orient='records')
        
        payload = {
            "report": report, 
            "preview": preview, 
            "columns": df.columns.tolist(), 
            "recommendations": recommendations
        }
        
        safe = jsonable_encoder(payload)
        
        def _make_json_safe(obj):
            if isinstance(obj, dict):
                return {k: _make_json_safe(v) for k, v in obj.items()}
            if isinstance(obj, list):
                return [_make_json_safe(v) for v in obj]
            try:
                if isinstance(obj, float):
                    if np.isnan(obj) or np.isinf(obj):
                        return None
            except Exception:
                pass
            return obj
        
        safe2 = _make_json_safe(safe)
        return JSONResponse(content=safe2)
        
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": f"Error parsing file: {str(e)}"})


@app.post("/api/clean-file/")
async def clean_file(file: UploadFile = File(...), 
                    missing_threshold: float = 0.8,
                    fill_strategy: str = "auto"):
    """
    Clean file with configurable missing value handling.
    
    Args:
        file: File to clean
        missing_threshold: Threshold above which columns are dropped (0.8 = 80%)
        fill_strategy: Strategy for missing values ('auto', 'drop', 'fill')
    """
    try:
        content = await file.read()
        file_extension = file.filename.split('.')[-1].lower() if file.filename else ''
        
        if file_extension == 'csv':
            try:
                txt = content.decode('utf-8')
            except Exception:
                txt = content.decode('latin-1')
            df = pd.read_csv(StringIO(txt), sep=None, engine='python')
        elif file_extension == 'json':
            try:
                obj = json.loads(content.decode('utf-8'))
            except Exception:
                obj = json.loads(content.decode('latin-1'))
            if isinstance(obj, list):
                df = pd.DataFrame(obj)
            else:
                df = pd.json_normalize(obj)
        else:
            return JSONResponse(status_code=400, content={"message": "Unsupported file type"})
        
        # Analyze missing values before cleaning
        missing_analysis = {}
        for col in df.columns:
            missing_count = df[col].isnull().sum()
            missing_percentage = missing_count / len(df)
            missing_analysis[col] = {
                'missing_count': int(missing_count),
                'missing_percentage': float(missing_percentage * 100),
                'will_be_dropped': missing_percentage >= missing_threshold and fill_strategy != 'fill'
            }
        
        # Perform cleaning with specified strategy
        cleaned_df = perform_standard_cleaning(df, missing_threshold, fill_strategy)
        
        # Generate cleaning summary
        original_columns = len(df.columns)
        final_columns = len(cleaned_df.columns)
        dropped_columns = original_columns - final_columns
        
        if file_extension == 'csv':
            output_bytes = cleaned_df.to_csv(index=False).encode('utf-8')
            media_type = "text/csv"
            filename = f"cleaned_{file.filename}"
        else:
            output_bytes = cleaned_df.to_json(orient='records', indent=4).encode('utf-8')
            media_type = "application/json"
            filename = f"cleaned_{file.filename}"
        
        # Add cleaning metadata to response headers
        headers = {
            "Content-Disposition": f"attachment; filename={filename}",
            "X-Cleaning-Strategy": fill_strategy,
            "X-Missing-Threshold": str(missing_threshold),
            "X-Original-Columns": str(original_columns),
            "X-Final-Columns": str(final_columns),
            "X-Dropped-Columns": str(dropped_columns)
        }
        
        return StreamingResponse(
            iter([output_bytes]), 
            media_type=media_type, 
            headers=headers
        )
        
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": f"An error occurred during cleaning: {str(e)}"})


@app.post("/api/preview-cleaning/")
async def preview_cleaning(file: UploadFile = File(...), 
                          missing_threshold: float = 0.8,
                          fill_strategy: str = "auto"):
    """
    Preview what will happen during cleaning without actually cleaning the file.
    Useful for understanding the impact of different cleaning strategies.
    """
    try:
        content = await file.read()
        file_extension = file.filename.split('.')[-1].lower() if file.filename else ''
        
        if file_extension == 'csv':
            try:
                txt = content.decode('utf-8')
            except Exception:
                txt = content.decode('latin-1')
            df = pd.read_csv(StringIO(txt), sep=None, engine='python')
        elif file_extension == 'json':
            try:
                obj = json.loads(content.decode('utf-8'))
            except Exception:
                obj = json.loads(content.decode('latin-1'))
            if isinstance(obj, list):
                df = pd.DataFrame(obj)
            else:
                df = pd.json_normalize(obj)
        else:
            return JSONResponse(status_code=400, content={"message": "Unsupported file type"})
        
        # Analyze missing values and predict cleaning impact
        cleaning_preview = {
            'file_info': {
                'filename': file.filename,
                'file_type': file_extension,
                'total_rows': len(df),
                'total_columns': len(df.columns)
            },
            'missing_value_analysis': {},
            'cleaning_strategy': {
                'missing_threshold': missing_threshold,
                'fill_strategy': fill_strategy
            },
            'predicted_actions': [],
            'columns_to_drop': [],
            'columns_to_fill': []
        }
        
        # Analyze each column
        for col in df.columns:
            missing_count = df[col].isnull().sum()
            missing_percentage = missing_count / len(df)
            dtype = str(df[col].dtype)
            
            col_analysis = {
                'column_name': col,
                'data_type': dtype,
                'missing_count': int(missing_count),
                'missing_percentage': float(missing_percentage * 100),
                'unique_values': int(df[col].nunique()),
                'will_be_dropped': missing_percentage >= missing_threshold and fill_strategy != 'fill'
            }
            
            # Predict filling strategy
            if missing_count > 0 and missing_percentage < missing_threshold:
                if dtype.startswith(('int', 'float')):
                    # Numeric column
                    if missing_percentage > 0.5:  # High missing rate
                        col_analysis['fill_strategy'] = 'median (high missing rate)'
                    else:
                        col_analysis['fill_strategy'] = 'mean'
                else:
                    # Object/text column
                    if missing_percentage > 0.5:  # High missing rate
                        col_analysis['fill_strategy'] = 'Unknown (high missing rate)'
                    else:
                        col_analysis['fill_strategy'] = 'mode'
            elif missing_percentage >= missing_threshold:
                col_analysis['fill_strategy'] = 'column will be dropped'
                cleaning_preview['columns_to_drop'].append(col)
            else:
                col_analysis['fill_strategy'] = 'no action needed'
            
            cleaning_preview['missing_value_analysis'][col] = col_analysis
            
            # Add to appropriate action lists
            if col_analysis['will_be_dropped']:
                cleaning_preview['columns_to_drop'].append(col)
                cleaning_preview['predicted_actions'].append(f"Drop column '{col}' ({missing_percentage*100:.1f}% missing)")
            elif missing_count > 0:
                cleaning_preview['columns_to_fill'].append(col)
                cleaning_preview['predicted_actions'].append(f"Fill missing values in '{col}' using {col_analysis['fill_strategy']}")
        
        # Summary statistics
        total_missing_columns = len([col for col in df.columns if df[col].isnull().sum() > 0])
        high_missing_columns = len(cleaning_preview['columns_to_drop'])
        
        cleaning_preview['summary'] = {
            'total_missing_columns': total_missing_columns,
            'high_missing_columns': high_missing_columns,
            'columns_after_cleaning': len(df.columns) - high_missing_columns,
            'estimated_improvement': f"{(high_missing_columns / len(df.columns) * 100):.1f}% reduction in problematic columns"
        }
        
        return JSONResponse(content=cleaning_preview)
        
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": f"Error previewing cleaning: {str(e)}"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
