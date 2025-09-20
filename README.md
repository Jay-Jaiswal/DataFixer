# DataFixer

A comprehensive data cleaning and analysis tool that automatically detects data quality issues and provides intelligent cleaning recommendations for CSV and JSON files.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Frontend Components](#frontend-components)
- [Data Quality Detection](#data-quality-detection)
- [Data Cleaning Solutions](#data-cleaning-solutions)
- [Project Structure](#project-structure)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

DataFixer is a full-stack web application designed to help data analysts, researchers, and developers quickly identify and resolve common data quality issues. The tool provides:

- **Automated Data Analysis**: Comprehensive scanning of CSV and JSON files for quality issues
- **Intelligent Issue Detection**: Identifies missing values, duplicates, outliers, and data type inconsistencies
- **Smart Recommendations**: Actionable suggestions for data cleaning and improvement
- **One-Click Cleaning**: Automated data cleaning with configurable strategies
- **Professional Reports**: Detailed analysis reports with visual indicators and statistics

## Features

### Core Functionality
- **Multi-format Support**: Handles CSV and JSON files seamlessly
- **Real-time Analysis**: Instant data quality assessment and reporting
- **Automated Cleaning**: Smart algorithms for handling missing values, duplicates, and formatting issues
- **Download Cleaned Data**: Export cleaned datasets in their original format
- **Intelligent Missing Value Handling**: Advanced strategies for columns with high missing value rates
- **Cleaning Preview**: See what will happen before applying cleaning operations

### Data Quality Detection
- **Missing Value Analysis**: Identifies and quantifies missing data patterns
- **Duplicate Detection**: Finds duplicate rows and columns
- **Outlier Identification**: Statistical outlier detection for numerical columns
- **Data Type Analysis**: Detects inconsistent data types and formatting issues
- **Capitalization Issues**: Identifies mixed case inconsistencies in text data

### Reporting & Visualization
- **Comprehensive Reports**: Detailed analysis with actionable insights
- **Interactive UI**: Modern, responsive web interface
- **Data Preview**: Sample data display for verification
- **Progress Indicators**: Visual feedback during processing
- **Professional Data Profiling**: Full-featured HTML profiling reports using YData Profiling
- **Data Quality Scoring**: Intelligent cleanliness percentage calculation

## Architecture

DataFixer follows a modern client-server architecture with clear separation of concerns:

```
┌─────────────────┐    HTTP/JSON    ┌─────────────────┐
│   React Frontend │ ◄──────────────► │  FastAPI Backend │
│   (Vite + React) │                 │   (Python)      │
└─────────────────┘                 └─────────────────┘
                                              │
                                              ▼
                                    ┌─────────────────┐
                                    │  Data Processing │
                                    │  (Pandas/Numpy) │
                                    └─────────────────┘
```

### Backend Architecture
- **FastAPI**: High-performance Python web framework
- **Data Processing**: Pandas and NumPy for data manipulation
- **Modular Design**: Separate modules for detection, solution, and API handling
- **CORS Support**: Cross-origin resource sharing enabled for frontend integration

### Frontend Architecture
- **React 19**: Modern React with hooks and functional components
- **Vite**: Fast build tool and development server
- **Component-based**: Modular UI components for maintainability
- **Responsive Design**: Mobile-friendly interface

## Technology Stack

### Backend
- **Python 3.13+**: Core programming language
- **FastAPI**: Modern, fast web framework for building APIs
- **Pandas**: Data manipulation and analysis library
- **NumPy**: Numerical computing library
- **YData Profiling**: Advanced data profiling and HTML report generation
- **Uvicorn**: ASGI server for running FastAPI applications
- **Python-dotenv**: Environment variable management

### Frontend
- **React 19**: JavaScript library for building user interfaces
- **Vite**: Build tool and development server
- **ESLint**: Code linting and quality enforcement
- **CSS3**: Modern styling with custom design system

### Development Tools
- **Git**: Version control
- **Virtual Environment**: Python dependency isolation
- **Package Managers**: pip (Python), npm (Node.js)

## Installation & Setup

### Prerequisites
- Python 3.13 or higher
- Node.js 18 or higher
- Git

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd DataFixer/backend
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Note: For full profiling functionality, ensure `ydata-profiling` is installed:
   ```bash
   pip install ydata-profiling
   ```

4. **Run the backend server**
   ```bash
   python main.py
   ```
   
   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd ../data-cleaner-ui
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```
   
   The frontend will be available at `http://localhost:5173`

### Environment Configuration

Create a `.env` file in the backend directory:
```env
# Server Configuration
HOST=0.0.0.0
PORT=8000

# CORS Settings
ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# Data Processing
MAX_FILE_SIZE=10485760  # 10MB
SUPPORTED_FORMATS=csv,json
```

## Usage

### Web Interface

1. **Open the application** in your web browser
2. **Upload a file** by dragging and dropping or clicking the upload area
3. **Analyze data** by clicking the "Analyze Data" button
4. **Review the report** showing data quality issues, cleanliness score, and recommendations
5. **Generate professional profile** by clicking the "Generate Profile" button for comprehensive HTML reports
6. **Clean and download** the processed data using "Clean & Download"

### Supported File Formats

#### CSV Files
- Comma-separated values
- Automatic delimiter detection
- UTF-8 and Latin-1 encoding support
- Header row detection

#### JSON Files
- Array of objects format
- Nested object flattening
- Multiple encoding support

### File Size Limits
- **Maximum file size**: 10MB (configurable)
- **Recommended row limit**: 100,000 rows for optimal performance
- **Column limit**: No strict limit, but performance may degrade with 100+ columns

## API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Health Check
```http
GET /health
```
**Response:**
```json
{
  "status": "ok"
}
```

#### 2. Root Information
```http
GET /
```
**Response:**
```json
{
  "message": "Data Cleaner API running.",
  "endpoints": {
    "analyze": "/api/upload-and-analyze/ (POST multipart/form-data file=...)",
    "clean": "/api/clean-file/ (POST multipart/form-data file=...)",
    "profile_report": "/api/profile-report/ (POST multipart/form-data file=...)",
    "docs": "/docs"
  }
}
```

#### 3. Data Analysis
```http
POST /api/upload-and-analyze/
```
**Request:** Multipart form data with file
**Response:**
```json
{
  "report": {
    "overview": {
      "rows": 1000,
      "columns": 15,
      "total_missing_values": 45,
      "duplicate_rows": 12,
      "cleanliness_percentage": 73
    },
    "column_details": {
      "column_name": {
        "dtype": "object",
        "missing_values": 5,
        "missing_percentage": 0.5,
        "unique_values": 950,
        "outlier_count": 0,
        "mixed_capitalization": false,
        "is_numeric_like": false,
        "has_problem": true,
        "reasons": ["High missing rate: 0.5%"]
      }
    }
  },
  "preview": [...],
  "columns": ["col1", "col2", ...],
  "recommendations": ["Found 12 duplicate rows. Consider removing them."]
}
```

#### 4. Professional Data Profiling
```http
POST /api/profile-report/
```
**Request:** Multipart form data with file
**Response:** HTML profiling report download (generated using YData Profiling)
**Features:**
- Comprehensive statistical analysis
- Data visualizations and charts
- Missing value patterns
- Correlation matrices
- Data distribution analysis
- Interactive HTML report

**Note:** Requires `ydata-profiling` package to be installed. For large datasets (>10k rows), sampling is applied for performance.

#### 5. Data Cleaning
```http
POST /api/clean-file/
```
**Request:** Multipart form data with file
**Query Parameters:**
- `missing_threshold`: Float (0.0-1.0) - Threshold above which columns are dropped (default: 0.8)
- `fill_strategy`: String - Strategy for missing values ('auto', 'drop', 'fill')

**Response:** Cleaned file download (CSV or JSON) with cleaning metadata in headers

**Example:**
```http
POST /api/clean-file/?missing_threshold=0.6&fill_strategy=drop
```

#### 6. Cleaning Preview
```http
POST /api/preview-cleaning/
```
**Request:** Multipart form data with file
**Query Parameters:** Same as cleaning endpoint
**Response:** Detailed preview of what will happen during cleaning

**Example Response:**
```json
{
  "file_info": {
    "filename": "data.csv",
    "file_type": "csv",
    "total_rows": 1000,
    "total_columns": 15
  },
  "missing_value_analysis": {
    "column_name": {
      "column_name": "age",
      "data_type": "float64",
      "missing_count": 200,
      "missing_percentage": 20.0,
      "unique_values": 45,
      "will_be_dropped": false,
      "fill_strategy": "mean"
    }
  },
  "predicted_actions": [
    "Fill missing values in 'age' using mean"
  ],
  "columns_to_drop": [],
  "columns_to_fill": ["age"],
  "summary": {
    "total_missing_columns": 3,
    "high_missing_columns": 0,
    "columns_after_cleaning": 15,
    "estimated_improvement": "0.0% reduction in problematic columns"
  }
}
```

### Error Handling

The API returns appropriate HTTP status codes:
- **200**: Success
- **400**: Bad request (invalid file, parsing error)
- **500**: Internal server error

Error responses include descriptive messages:
```json
{
  "message": "Error parsing file: Invalid CSV format"
}
```

## Frontend Components

### App.jsx
Main application component that handles:
- File upload and management
- API communication
- State management
- User interface coordination

### Report.jsx
Data analysis display component featuring:
- **Data Quality Score**: Visual cleanliness percentage with color-coded status indicators
- **Overview Statistics**: Row count, column count, missing values, duplicates
- **Column Analysis**: Detailed breakdown of each column's data quality
- **Recommendations**: Actionable suggestions for data improvement
- **Data Preview**: Sample data display with expandable view

### Styling
- **Modern Design**: Clean, professional interface
- **Responsive Layout**: Works on desktop and mobile devices
- **Interactive Elements**: Hover effects, animations, and visual feedback
- **Color-coded Issues**: Problem indicators and status badges

## Data Quality Detection

### Missing Values
- **Detection**: Identifies null, NaN, and empty string values
- **Analysis**: Calculates missing percentage per column
- **Thresholds**: Flags columns with >20% missing data

### Duplicates
- **Row Duplicates**: Identifies identical rows across the dataset
- **Column Duplicates**: Detects columns with identical names
- **Impact Assessment**: Quantifies duplicate impact on data quality

### Outliers
- **Statistical Method**: Uses Interquartile Range (IQR) method
- **Threshold**: 1.5 × IQR from Q1 and Q3
- **Numeric Only**: Applied to numerical columns only

### Data Type Issues
- **Mixed Capitalization**: Detects inconsistent text formatting
- **Numeric-like Strings**: Identifies text that should be numeric
- **Type Inconsistencies**: Flags columns with mixed data types

### Format Issues
- **Column Naming**: Identifies problematic column names
- **Whitespace**: Detects leading/trailing spaces
- **Special Characters**: Flags non-standard characters in data

## Data Cleaning Solutions

### Automatic Cleaning Strategies

#### Missing Value Handling
- **Numeric Columns**: Fill with mean value
- **Categorical Columns**: Fill with mode (most frequent value)
- **Text Columns**: Fill with empty string or mode

#### Duplicate Removal
- **Row Deduplication**: Remove duplicate rows while preserving first occurrence
- **Column Deduplication**: Rename duplicate columns with suffixes

#### Data Standardization
- **Column Names**: Convert to lowercase, replace spaces with underscores
- **Text Cleaning**: Strip whitespace, standardize capitalization
- **Data Types**: Convert numeric-like strings to appropriate types

#### Format Standardization
- **CSV Output**: Consistent delimiter and encoding
- **JSON Output**: Proper formatting and structure
- **File Naming**: Prefixed with "cleaned_" for identification

### Customization Options
The cleaning process can be customized through API parameters and by modifying the `perform_standard_cleaning` function in `main.py`:

#### API-Level Customization
- **`missing_threshold`**: Control when columns are dropped (default: 0.8 = 80%)
- **`fill_strategy`**: Choose between 'auto', 'drop', or 'fill' strategies

#### Code-Level Customization
```python
def perform_standard_cleaning(df: pd.DataFrame, 
                            missing_threshold: float = 0.8,
                            fill_strategy: str = 'auto') -> pd.DataFrame:
    # Custom cleaning logic here
    pass
```

### Advanced Missing Value Handling

#### High-Missing-Value Scenarios
- **Columns with >80% missing values**: Automatically dropped by default
- **Configurable threshold**: Adjust via `missing_threshold` parameter
- **Multiple strategies**: Choose between dropping, filling, or automatic handling

#### Intelligent Filling Strategies
- **Numeric columns**: Mean → Median → 0 (fallback chain)
- **Text columns**: Mode → "Unknown" (fallback)
- **High missing rate**: Uses more robust statistics (median for numeric, "Unknown" for text)

#### Safety Features
- **Error handling**: Graceful fallbacks when calculations fail
- **Logging**: Detailed information about cleaning decisions
- **Preview mode**: See cleaning impact before applying changes

## Project Structure

```
DataFixer/
├── backend/                          # Python backend
│   ├── main.py                      # FastAPI application and main logic
│   ├── detection.py                 # Data issue detection classes
│   ├── solution.py                  # Data cleaning solution classes
│   ├── requirements.txt             # Python dependencies
│   ├── test_api.py                  # API testing utilities
│   └── venv/                        # Virtual environment
├── data-cleaner-ui/                 # React frontend
│   ├── src/
│   │   ├── App.jsx                  # Main application component
│   │   ├── components/
│   │   │   └── Report.jsx          # Data report display component
│   │   ├── App.css                 # Main stylesheet
│   │   └── main.jsx                # Application entry point
│   ├── package.json                 # Node.js dependencies
│   ├── vite.config.js              # Vite configuration
│   └── index.html                  # HTML template
└── README.md                        # This documentation file
```

### Key Files Description

#### Backend Files
- **`main.py`**: Core FastAPI application with endpoints and data processing logic
- **`detection.py`**: DataIssueDetector class for identifying data quality problems
- **`solution.py`**: DataIssueSolver class for implementing cleaning strategies
- **`requirements.txt`**: Python package dependencies

#### Frontend Files
- **`App.jsx`**: Main React component handling file uploads and API calls
- **`Report.jsx`**: Component for displaying data analysis results
- **`App.css`**: Comprehensive styling for the user interface
- **`package.json`**: Node.js dependencies and build scripts

## Development

### Running in Development Mode

#### Backend Development
```bash
cd backend
python main.py
```
- Server runs on `http://localhost:8000`
- Auto-reload on code changes
- Interactive API documentation at `/docs`

#### Frontend Development
```bash
cd data-cleaner-ui
npm run dev
```
- Development server on `http://localhost:5173`
- Hot module replacement
- Real-time error reporting

### Building for Production

#### Frontend Build
```bash
cd data-cleaner-ui
npm run build
```
- Creates optimized production build in `dist/` directory
- Minified and bundled JavaScript/CSS
- Ready for deployment

#### Backend Production
```bash
cd backend
pip install -r requirements.txt
python main.py
```
- Configure production settings in environment variables
- Use production ASGI server (Gunicorn recommended)
- Set up reverse proxy (Nginx recommended)

### Testing

#### API Testing
```bash
cd backend
python test_api.py
```

#### Frontend Testing
```bash
cd data-cleaner-ui
npm run lint
```

### Code Quality

#### Python
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Document functions and classes

#### JavaScript/React
- Use ESLint for code quality
- Follow React best practices
- Maintain component reusability

## Contributing

### Development Workflow

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Test thoroughly**
5. **Commit with descriptive messages**
   ```bash
   git commit -m "Add feature: description of changes"
   ```
6. **Push to your branch**
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create a pull request**

### Code Standards

#### Python
- Use meaningful variable and function names
- Add docstrings for public functions
- Handle exceptions gracefully
- Write unit tests for new functionality

#### JavaScript/React
- Use functional components with hooks
- Maintain consistent naming conventions
- Add PropTypes for component validation
- Write clean, readable code

### Testing Guidelines

#### Backend Testing
- Test all API endpoints
- Verify error handling
- Test with various file formats
- Performance testing with large files

#### Frontend Testing
- Test user interactions
- Verify responsive design
- Cross-browser compatibility
- Accessibility testing

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- **FastAPI**: For the excellent Python web framework
- **Pandas**: For powerful data manipulation capabilities
- **React**: For the modern frontend framework
- **Vite**: For fast build tooling

## Support

For questions, issues, or contributions:
- **Issues**: Create an issue on the project repository
- **Discussions**: Use GitHub Discussions for questions
- **Contributions**: Submit pull requests for improvements

---

**DataFixer** - Making data cleaning simple, fast, and intelligent!
## Branding & Customization

The application uses a custom logo (`logo.gif`) as both the main interface logo and the browser tab favicon. To update the branding, simply replace the `logo.gif` file in the `public` folder of the frontend project. The favicon and all branding will update automatically.
