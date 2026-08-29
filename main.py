import pandas as pd

file_path = "data/Partner_Payment_System_MVP.xlsx"

partners = pd.read_excel(
    file_path,
    sheet_name="partners"
)

commission_rules = pd.read_excel(
    file_path,
    sheet_name="commission_rules"
)

deals = pd.read_excel(
    file_path,
    sheet_name="deals"
)

print("=== FILE LOADED SUCCESSFULLY ===")

print("\nPartners:")
print(partners.head())

print("\nCommission Rules:")
print(commission_rules.head())

print("\nDeals:")
print(deals.head())

print("\n=== DATA QUALITY CHECK ===")

print("\nMissing values - Partners:")
print(partners.isnull().sum())

print("\nMissing values - Commission Rules:")
print(commission_rules.isnull().sum())

print("\nMissing values - Deals:")
print(deals.isnull().sum())

print("\n=== CALCULATING COMMISSIONS ===")

deals_with_commission = deals.merge(
    commission_rules[
        ["partner_id", "product", "commission_rate"]
    ],
    on=["partner_id", "product"],
    how="left"
)

deals_with_commission["commission_amount"] = (
    deals_with_commission["funded_amount"]
    * deals_with_commission["commission_rate"]
)

print(deals_with_commission)

print("\n=== PARTNER VALIDATION ===")

deals_with_commission = deals_with_commission.merge(
    partners[["partner_id", "partner_name", "active"]],
    on="partner_id",
    how="left"
)

deals_with_commission["partner_valid"] = (
    deals_with_commission["active"] == True
)

print(
    deals_with_commission[
        [
            "deal_id",
            "partner_id",
            "partner_name",
            "active",
            "partner_valid",
            "commission_amount"
        ]
    ]
)

print("\n=== PAYMENT STATUS ===")

deals_with_commission["payment_status"] = (
    deals_with_commission["partner_valid"]
    .map({
        True: "Approved",
        False: "Rejected"
    })
)

print(
    deals_with_commission[
        [
            "deal_id",
            "partner_name",
            "commission_amount",
            "payment_status"
        ]
    ]
)

print("\n=== DEAL STATUS VALIDATION ===")

deals_with_commission["deal_valid"] = (
    deals_with_commission["status"] == "Funded"
)

print(
    deals_with_commission[
        [
            "deal_id",
            "status",
            "deal_valid",
            "commission_amount"
        ]
    ]
)

print("\n=== FINAL PAYMENT VALIDATION ===")

deals_with_commission["payment_approved"] = (
    deals_with_commission["partner_valid"]
    & deals_with_commission["deal_valid"]
)

deals_with_commission["payment_status"] = (
    deals_with_commission["payment_approved"]
    .map({
        True: "Approved",
        False: "Rejected"
    })
)

print(
    deals_with_commission[
        [
            "deal_id",
            "partner_name",
            "status",
            "commission_amount",
            "payment_status"
        ]
    ]
)

print("\n=== EXCEPTION REASONS ===")

def get_exception_reason(row):
    reasons = []

    if not row["partner_valid"]:
        reasons.append("Partner inactive")

    if pd.isna(row["commission_rate"]):
        reasons.append("Missing commission rule")

    if not row["deal_valid"]:
        reasons.append("Deal not funded")

    if len(reasons) == 0:
        return "None"

    return "; ".join(reasons)


deals_with_commission["exception_reason"] = (
    deals_with_commission.apply(
        get_exception_reason,
        axis=1
    )
)

print(
    deals_with_commission[
        [
            "deal_id",
            "partner_name",
            "payment_status",
            "exception_reason"
        ]
    ]
)

print("\n=== APPROVED PAYMENTS ===")

approved_payments = deals_with_commission[
    deals_with_commission["payment_status"] == "Approved"
]

print(
    approved_payments[
        [
            "deal_id",
            "partner_id",
            "partner_name",
            "product",
            "funded_amount",
            "commission_rate",
            "commission_amount"
        ]
    ]
)


print("\n=== EXCEPTIONS ===")

exceptions = deals_with_commission[
    deals_with_commission["payment_status"] == "Rejected"
]

print(
    exceptions[
        [
            "deal_id",
            "partner_id",
            "partner_name",
            "payment_status",
            "exception_reason"
        ]
    ]
)

print("\n=== PAYMENT SUMMARY BY PARTNER ===")

payment_summary = (
    approved_payments
    .groupby(["partner_id", "partner_name"])
    .agg(
        total_deals=("deal_id", "count"),
        total_funded=("funded_amount", "sum"),
        total_commission=("commission_amount", "sum")
    )
    .reset_index()
)

print(payment_summary)

print("\n=== PAYMENT TERMS ===")

approved_payments = approved_payments.merge(
    partners[["partner_id", "payment_terms"]],
    on="partner_id",
    how="left"
)

print(
    approved_payments[
        [
            "deal_id",
            "partner_name",
            "funded_date",
            "payment_terms"
        ]
    ]
)

approved_payments["payment_days"] = (
    approved_payments["payment_terms"]
    .str.extract(r"(\d+)")
    .astype(int)
)
approved_payments["payment_due_date"] = (
    approved_payments["funded_date"]
    + pd.to_timedelta(
        approved_payments["payment_days"],
        unit="D"
    )
)
print("\n=== PAYMENT DUE DATES ===")

print(
    approved_payments[
        [
            "deal_id",
            "partner_name",
            "commission_amount",
            "payment_terms",
            "payment_due_date"
        ]
    ]
)

print("\n=== PAYMENT AGING ===")

today = pd.Timestamp.today().normalize()

approved_payments["days_until_due"] = (
    approved_payments["payment_due_date"] - today
).dt.days

approved_payments["aging_status"] = approved_payments[
    "days_until_due"
].apply(
    lambda x: "Overdue" if x < 0 else "Pending"
)

print(
    approved_payments[
        [
            "deal_id",
            "partner_name",
            "commission_amount",
            "payment_due_date",
            "days_until_due",
            "aging_status"
        ]
    ]
)

print("\n=== CASH REQUIREMENTS ===")

overdue_amount = approved_payments.loc[
    approved_payments["aging_status"] == "Overdue",
    "commission_amount"
].sum()

pending_amount = approved_payments.loc[
    approved_payments["aging_status"] == "Pending",
    "commission_amount"
].sum()

total_payment_required = approved_payments["commission_amount"].sum()

print(f"Overdue payments: ${overdue_amount:,.2f}")
print(f"Pending payments: ${pending_amount:,.2f}")
print(f"Total payment required: ${total_payment_required:,.2f}")

print("\n=== EXPORTING PAYMENT REPORT ===")

payment_report = approved_payments[
    [
        "deal_id",
        "partner_id",
        "partner_name",
        "product",
        "funded_amount",
        "commission_rate",
        "commission_amount",
        "payment_terms",
        "payment_due_date",
        "aging_status"
    ]
]

payment_report.to_excel(
    "reports/payment_report.xlsx",
    index=False
)

print("Payment report created successfully.")

print("\n=== EXPORTING EXCEPTION REPORT ===")

exception_report = exceptions[
    [
        "deal_id",
        "partner_id",
        "partner_name",
        "product",
        "funded_amount",
        "payment_status",
        "exception_reason"
    ]
]

exception_report.to_excel(
    "reports/exception_report.xlsx",
    index=False
)

print("Exception report created successfully.")

print("\n=== FINANCE OPERATIONS SUMMARY ===")

total_deals = len(deals)
approved_deals = len(approved_payments)
rejected_deals = len(exceptions)

total_funded = approved_payments["funded_amount"].sum()
total_commissions = approved_payments["commission_amount"].sum()

print(f"Total deals: {total_deals}")
print(f"Approved deals: {approved_deals}")
print(f"Rejected deals: {rejected_deals}")
print(f"Total funded amount: ${total_funded:,.2f}")
print(f"Total commissions: ${total_commissions:,.2f}")
print(f"Overdue commissions: ${overdue_amount:,.2f}")
print(f"Pending commissions: ${pending_amount:,.2f}")

summary = pd.DataFrame({
    "metric": [
        "Total deals",
        "Approved deals",
        "Rejected deals",
        "Total funded amount",
        "Total commissions",
        "Overdue commissions",
        "Pending commissions"
    ],
    "value": [
        total_deals,
        approved_deals,
        rejected_deals,
        total_funded,
        total_commissions,
        overdue_amount,
        pending_amount
    ]
})

summary.to_excel(
    "reports/finance_summary.xlsx",
    index=False
)

print("Finance summary created successfully.")