# Partner Payment System

Python-based Finance Operations workflow for partner commission processing.

## Features

- Load partner, commission rule and deal data from Excel
- Calculate commissions automatically
- Validate partner eligibility
- Detect missing commission rules
- Generate approved payment reports
- Generate exception reports
- Calculate payment due dates
- Perform AP aging analysis
- Produce finance summary reports

## Tech Stack

- Python
- Pandas
- OpenPyXL

## Outputs

- payment_report.xlsx
- exception_report.xlsx
- finance_summary.xlsx

## Run

```bash
pip install -r requirements.txt
python main.py
```