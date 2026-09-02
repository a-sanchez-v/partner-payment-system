# Partner Payment System

Python-based Finance Operations workflow for partner commission processing, validation, payment scheduling, and reporting.

## Overview

This project automates a partner commission payment workflow from raw Excel data through validation, commission calculation, payment scheduling, exception handling, and finance reporting.

The workflow is designed to simulate a Finance Operations process where partner payments need to be calculated accurately, validated against business rules, and transformed into actionable payment and cash-requirement reports.

## Features

* Load partner, commission rule, and deal data from Excel
* Perform data quality checks
* Calculate partner commissions automatically
* Validate partner eligibility
* Detect missing commission rules
* Validate deal status
* Approve or reject partner payments
* Generate exception reasons
* Calculate payment due dates based on payment terms
* Perform payment aging analysis
* Calculate cash requirements
* Generate finance operations summary
* Export Excel reports for Finance Operations review

## Tech Stack

* Python 3
* Pandas
* OpenPyXL
* Excel / LibreOffice

## Project Structure

```text
partner-payment-system/
├── data/
│   └── Partner_Payment_System_MVP.xlsx
├── reports/
│   ├── payment_report.xlsx
│   ├── exception_report.xlsx
│   └── finance_summary.xlsx
├── main.py
├── open_reports.sh
├── requirements.txt
└── README.md
```

## Workflow

```text
Excel Input
     ↓
Data Quality Checks
     ↓
Commission Calculation
     ↓
Partner Validation
     ↓
Payment Validation
     ↓
Exception Detection
     ↓
Payment Scheduling & Aging
     ↓
Cash Requirements
     ↓
Excel Reports
```

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

Run the Finance Operations workflow:

```bash
python main.py
```

The script processes the input Excel file and generates the reports in the `reports/` directory.

## Open Reports

If running the project through WSL with LibreOffice installed on Windows, use:

```bash
./open_reports.sh
```

This opens all generated Excel reports using the Windows application associated with `.xlsx` files.

Individual reports can also be opened manually from Windows.

## Outputs

### `payment_report.xlsx`

Contains approved partner payments, payment terms, due dates, aging information, and cash requirements.

### `exception_report.xlsx`

Contains rejected or invalid payment records together with the reasons for rejection.

### `finance_summary.xlsx`

Contains a high-level Finance Operations summary, including deal counts, funded amounts, commissions, overdue payments, pending payments, and total payment requirements.

## Example Finance Operations Summary

For the current sample dataset:

* Total deals: 5
* Approved deals: 4
* Rejected deals: 1
* Total funded amount: $57,000
* Total commissions: $3,040
* Overdue commissions: $840
* Pending commissions: $2,200

## Purpose

This project demonstrates how Python can be used to automate recurring Finance Operations processes, improve validation and control, reduce manual calculation, and produce structured reporting for payment decisions and cash planning.
