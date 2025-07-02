# demointernproj

# SAP Vendor Payments Report

This Python application extracts vendor payment data from SAP via RFC and sends it via email to the Finance department.

## Features

- Daily extraction of vendor payments from SAP
- Automatic email distribution with HTML report
- CSV attachment with detailed payment data
- Configurable date range and company code

## Installation

1. Clone this repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:
    pip install -r requirements.txt
4. Create a .env file with your configuration (use .env.example as template)

# Usage
python main.py

