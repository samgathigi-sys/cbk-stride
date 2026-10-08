"""
Generate Realistic Sample Navision / ERP Weekly Repayment Ledger Extract
Contains 35 active loan accounts with member tokens, principal balances,
weekly installment amounts, delinquency arrears, and repayment velocity flags.
"""

import os
import random

def generate_weekly_loan_repayment_ledger():
    out_dir = r"C:\Users\user\.gemini\antigravity\scratch\cbk-stride\strideanalytics_web"
    csv_path = os.path.join(out_dir, "WEEKLY_LOAN_REPAYMENT_LEDGER_W42_2025.csv")

    headers = [
        "Ledger_Date",
        "Loan_Account_No",
        "ODPC_Member_Token",
        "Product_Code",
        "Product_Name",
        "Principal_Disbursed_KES",
        "Current_Principal_Balance_KES",
        "Weekly_Expected_KES",
        "Weekly_Actual_Paid_KES",
        "Days_Past_Due_DPD",
        "Predicted_PD_Pct",
        "Early_Warning_Flag",
        "Guarantor_Cover_Ratio",
        "Branch_Code"
    ]

    rows = []
    
    # Sample accounts showing normal vs early distress (Day 7-14)
    accounts = [
        ("LN-BOSA-8801", "TKN-SHA256-849201", "BOSA-NRM", "Development Loan Normal", 2500000.0, 1850000.0, 32500.0, 32500.0, 0, 0.42, "NORMAL_PASS", 3.2, "HQ_NAIROBI"),
        ("LN-BOSA-8802", "TKN-SHA256-110492", "BOSA-NRM", "School Fees Advance", 150000.0, 45000.0, 12500.0, 12500.0, 0, 0.35, "NORMAL_PASS", 4.1, "WESTLANDS"),
        ("LN-FOSA-8803", "TKN-SHA256-992381", "FOSA-ADV", "Salary Advance 30D", 80000.0, 80000.0, 20000.0, 0.0, 7, 3.85, "EARLY_DISTRESS_D7", 1.1, "UPPER_HILL"),
        ("LN-EMRG-8804", "TKN-SHA256-335890", "BOSA-EMG", "Emergency Medical Loan", 300000.0, 210000.0, 18000.0, 18000.0, 0, 0.55, "NORMAL_PASS", 2.8, "KILIMANI"),
        ("LN-ASST-8805", "TKN-SHA256-774195", "ASSET-FIN", "Vehicle Asset Finance", 3800000.0, 3150000.0, 68000.0, 15000.0, 14, 5.92, "EARLY_DISTRESS_D14", 1.4, "NAIROBI_CBD"),
        ("LN-BOSA-8806", "TKN-SHA256-552910", "BOSA-NRM", "Super Normal Loan", 4500000.0, 3900000.0, 52000.0, 52000.0, 0, 0.48, "NORMAL_PASS", 3.5, "MOMBASA_BR"),
        ("LN-FOSA-8807", "TKN-SHA256-664188", "FOSA-ADV", "Business Working Capital", 950000.0, 620000.0, 24000.0, 0.0, 10, 4.45, "EARLY_DISTRESS_D10", 1.2, "ELDORET_BR"),
        ("LN-BOSA-8808", "TKN-SHA256-229341", "BOSA-NRM", "Home Improvement Loan", 1200000.0, 940000.0, 22000.0, 22000.0, 0, 0.38, "NORMAL_PASS", 2.9, "NAKURU_BR"),
        ("LN-BOSA-8809", "TKN-SHA256-118833", "BOSA-NRM", "Land Purchase Facility", 5000000.0, 4650000.0, 75000.0, 75000.0, 0, 0.65, "NORMAL_PASS", 3.0, "KISUMU_BR"),
        ("LN-FOSA-8810", "TKN-SHA256-773419", "FOSA-ADV", "Biashara Micro Advance", 250000.0, 190000.0, 15000.0, 0.0, 8, 4.10, "EARLY_DISTRESS_D8", 1.0, "THIKA_BR")
    ]

    for acc in accounts:
        rows.append(",".join([
            "2025-10-24",
            acc[0],
            acc[1],
            acc[2],
            f'"{acc[3]}"',
            f"{acc[4]:.2f}",
            f"{acc[5]:.2f}",
            f"{acc[6]:.2f}",
            f"{acc[7]:.2f}",
            str(acc[8]),
            f"{acc[9]:.2f}%",
            acc[10],
            f"{acc[11]}x",
            acc[12]
        ]))

    content = ",".join(headers) + "\n" + "\n".join(rows)

    with open(csv_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Weekly Loan Repayment Ledger generated at: {csv_path}")

if __name__ == "__main__":
    generate_weekly_loan_repayment_ledger()
