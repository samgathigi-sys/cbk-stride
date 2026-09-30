"""
generate_secretariat_template.py
Creates an institutional, styled Excel template and CSV template for the
CBK Sports & Wellness Secretariat to populate employee sports registrations.
Includes Excel Data Validation dropdowns for Directorates and the 18 Sporting Disciplines (A-Z).
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
import pandas as pd

# Define directories & filenames
BASE_DIR = os.path.dirname(__file__)
XLSX_PATH = os.path.join(BASE_DIR, "CBK_STRIDE_Secretariat_Roster_Template.xlsx")
CSV_PATH = os.path.join(BASE_DIR, "CBK_STRIDE_Secretariat_Roster_Template.csv")

# Constants
CBK_DEPARTMENTS = [
    "Banking & Payment Services",
    "Currency Operations & Logistics",
    "Finance & Accounts",
    "Financial Markets & Reserves",
    "Governor's Executive Office",
    "Human Resources",
    "Internal Audit",
    "IT & Digital Services",
    "Legal & Board Secretariat",
    "Monetary Policy & Research"
]

ALL_18_SPORTS = [
    "Athletics & Track",
    "Badminton",
    "Basketball",
    "Chess",
    "Cycling",
    "Football (Soccer)",
    "Golf",
    "Lawn Tennis",
    "Martial Arts & Self Defense",
    "Netball",
    "Physical Fitness & Aerobics",
    "Scrabble & Darts",
    "Snooker / Pool",
    "Squash",
    "Swimming",
    "Table Tennis",
    "Tug of War",
    "Volleyball"
]

ROLES = [
    "Athlete / Player",
    "Team Captain",
    "Team Manager / Coach",
    "Medic / First Aid",
    "Secretariat Official"
]

MEDICAL_STATUSES = [
    "YES - Certified for Active Competition",
    "YES - Recreational Walking / Gym Only",
    "Pending Medical Examination"
]

def build_template():
    wb = openpyxl.Workbook()
    # Sheet 1: Main Data Entry Sheet
    ws_main = wb.active
    ws_main.title = "CBK_Athlete_Roster"
    ws_main.views.sheetView[0].showGridLines = True

    # Sheet 2: Instructions & Dictionary
    ws_inst = wb.create_sheet(title="Instructions_&_Guidelines")
    ws_inst.views.sheetView[0].showGridLines = True

    # Sheet 3: System Reference Lookups
    ws_lookups = wb.create_sheet(title="System_Lookup_Values")
    ws_lookups.views.sheetView[0].showGridLines = True

    # Styling Palettes (CBK STRIDE Dark Midnight & Championship Gold)
    navy_dark = "041021"
    gold_accent = "F5C542"
    navy_light = "0A254A"
    zebra_tint = "F0F7FF"
    white = "FFFFFF"
    grey_text = "64748B"
    border_color = "CBD5E1"

    thin_border = Border(
        left=Side(style='thin', color=border_color),
        right=Side(style='thin', color=border_color),
        top=Side(style='thin', color=border_color),
        bottom=Side(style='thin', color=border_color)
    )

    # =========================================================================
    # POPULATE SYSTEM LOOKUP VALUES (SHEET 3)
    # =========================================================================
    ws_lookups["A1"] = "CBK Directorates (A-Z)"
    ws_lookups["A1"].font = Font(name="Calibri", size=11, bold=True, color=white)
    ws_lookups["A1"].fill = PatternFill(start_color=navy_dark, end_color=navy_dark, fill_type="solid")
    for idx, dept in enumerate(CBK_DEPARTMENTS, start=2):
        ws_lookups[f"A{idx}"] = dept

    ws_lookups["B1"] = "18 Sporting Disciplines (A-Z)"
    ws_lookups["B1"].font = Font(name="Calibri", size=11, bold=True, color=white)
    ws_lookups["B1"].fill = PatternFill(start_color=navy_dark, end_color=navy_dark, fill_type="solid")
    for idx, sport in enumerate(ALL_18_SPORTS, start=2):
        ws_lookups[f"B{idx}"] = sport

    ws_lookups["C1"] = "Assigned Roles"
    ws_lookups["C1"].font = Font(name="Calibri", size=11, bold=True, color=white)
    ws_lookups["C1"].fill = PatternFill(start_color=navy_dark, end_color=navy_dark, fill_type="solid")
    for idx, role in enumerate(ROLES, start=2):
        ws_lookups[f"C{idx}"] = role

    ws_lookups["D1"] = "Medical Fitness Clearances"
    ws_lookups["D1"].font = Font(name="Calibri", size=11, bold=True, color=white)
    ws_lookups["D1"].fill = PatternFill(start_color=navy_dark, end_color=navy_dark, fill_type="solid")
    for idx, med in enumerate(MEDICAL_STATUSES, start=2):
        ws_lookups[f"D{idx}"] = med

    ws_lookups.column_dimensions["A"].width = 34
    ws_lookups.column_dimensions["B"].width = 32
    ws_lookups.column_dimensions["C"].width = 26
    ws_lookups.column_dimensions["D"].width = 40

    # =========================================================================
    # POPULATE MAIN ROSTER SHEET (SHEET 1)
    # =========================================================================
    # Banner Header Rows
    ws_main.merge_cells("A1:K1")
    ws_main["A1"] = "CENTRAL BANK OF KENYA • SPORTS & WELLNESS SECRETARIAT"
    ws_main["A1"].font = Font(name="Calibri", size=11, bold=True, color=gold_accent)
    ws_main["A1"].fill = PatternFill(start_color=navy_dark, end_color=navy_dark, fill_type="solid")
    ws_main["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws_main.row_dimensions[1].height = 24

    ws_main.merge_cells("A2:K2")
    ws_main["A2"] = "CBK STRIDE™ OFFICIAL ATHLETE ENROLLMENT & SQUAD ROSTER TEMPLATE"
    ws_main["A2"].font = Font(name="Calibri", size=15, bold=True, color=white)
    ws_main["A2"].fill = PatternFill(start_color=navy_dark, end_color=navy_dark, fill_type="solid")
    ws_main["A2"].alignment = Alignment(horizontal="center", vertical="center")
    ws_main.row_dimensions[2].height = 30

    ws_main.merge_cells("A3:K3")
    ws_main["A3"] = "Instructions: Complete staff details below. Columns A to E (*) are mandatory for QR badge issuance and attendance certification. Use dropdown selections where provided."
    ws_main["A3"].font = Font(name="Calibri", size=9, italic=True, color="CBD5E1")
    ws_main["A3"].fill = PatternFill(start_color=navy_light, end_color=navy_light, fill_type="solid")
    ws_main["A3"].alignment = Alignment(horizontal="center", vertical="center")
    ws_main.row_dimensions[3].height = 20

    # Table Column Headers
    headers = [
        ("Staff ID / Payroll No.*", "e.g. 1008 or CBK-1008", 22),
        ("Full Official Name*", "e.g. Sam Gathigi", 26),
        ("Institutional CBK Email*", "e.g. sgathigi@centralbank.go.ke", 32),
        ("Directorate / Department*", "Select from Dropdown List", 32),
        ("Primary Enrolled Sport*", "Select from 18 Disciplines", 28),
        ("Secondary Sport (Optional)", "Select or leave blank", 28),
        ("Mobile / WhatsApp Phone", "e.g. +254 722 000 000", 24),
        ("Assigned Squad Role*", "Default: Athlete / Player", 24),
        ("Medical Fitness Clearance*", "Competition / Recreational", 34),
        ("Emergency Contact (Name & Tel)", "e.g. Jane Doe - 0722000000", 30),
        ("Discipline Notes / Handicap / Position", "e.g. Golf Hcp 14, Goalkeeper, 5000m", 36)
    ]

    header_row = 5
    ws_main.row_dimensions[header_row].height = 28

    for col_idx, (h_title, h_sub, col_w) in enumerate(headers, start=1):
        cell = ws_main.cell(row=header_row, column=col_idx)
        cell.value = h_title
        cell.font = Font(name="Calibri", size=10, bold=True, color=white)
        cell.fill = PatternFill(start_color=navy_dark, end_color=navy_dark, fill_type="solid")
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = thin_border
        col_letter = get_column_letter(col_idx)
        ws_main.column_dimensions[col_letter].width = col_w

    # Sample Demonstration Rows
    sample_records = [
        ("CBK-1008", "Sam Gathigi", "sgathigi@centralbank.go.ke", "Finance & Accounts", "Golf", "Physical Fitness & Aerobics", "+254 722 100 800", "Athlete / Player", "YES - Certified for Active Competition", "Mary Gathigi - 0722111222", "Handicap 14 • 1st Tee Regular"),
        ("CBK-2401", "Bernard Kiprono", "bkiprono@centralbank.go.ke", "Currency Operations & Logistics", "Football (Soccer)", "None", "+254 721 240 100", "Team Captain", "YES - Certified for Active Competition", "Faith Kiprono - 0722333444", "Team Captain • Striker / Center Forward"),
        ("CBK-2402", "Grace Mutisya", "gmutisya@centralbank.go.ke", "IT & Digital Services", "Basketball", "Swimming", "+254 723 240 200", "Team Captain", "YES - Certified for Active Competition", "David Mutisya - 0722555666", "Team Captain • Point Guard"),
        ("CBK-2405", "Geoffrey Kemboi", "gkemboi@centralbank.go.ke", "Monetary Policy & Research", "Athletics & Track", "Cycling", "+254 720 240 500", "Team Captain", "YES - Certified for Active Competition", "Sarah Kemboi - 0722777888", "Team Captain • Middle Distance 5000m"),
        ("CBK-2406", "Eric Mwangi", "emwangi@centralbank.go.ke", "Governor's Executive Office", "Golf", "Snooker / Pool", "+254 722 240 600", "Team Captain", "YES - Certified for Active Competition", "Anne Mwangi - 0722888999", "Team Captain • Handicap 9"),
        ("CBK-1024", "Brian Kimani", "bkimani@centralbank.go.ke", "Internal Audit", "Athletics & Track", "None", "+254 722 102 400", "Athlete / Player", "YES - Certified for Active Competition", "Alice Kimani - 0722444555", "100m Sprint & 4x100m Relay"),
        ("CBK-8201", "Joyce Cheruiyot", "jcheruiyot@centralbank.go.ke", "Human Resources", "Lawn Tennis", "Badminton", "+254 722 820 100", "Team Captain", "YES - Certified for Active Competition", "Paul Cheruiyot - 0722999000", "Team Captain • Singles & Doubles"),
        ("CBK-5012", "Kevin Kariuki", "kkariuki@centralbank.go.ke", "Legal & Board Secretariat", "Swimming", "Water Polo", "+254 722 501 200", "Team Captain", "YES - Certified for Active Competition", "Esther Kariuki - 0722333111", "Team Captain • Freestyle & Butterfly"),
    ]

    for row_offset, rec in enumerate(sample_records):
        cur_row = header_row + 1 + row_offset
        ws_main.row_dimensions[cur_row].height = 21
        is_even = row_offset % 2 == 1
        row_fill = PatternFill(start_color=zebra_tint, end_color=zebra_tint, fill_type="solid") if is_even else PatternFill(fill_type=None)

        for col_idx, val in enumerate(rec, start=1):
            c = ws_main.cell(row=cur_row, column=col_idx, value=val)
            c.font = Font(name="Calibri", size=9.5)
            c.border = thin_border
            if is_even:
                c.fill = row_fill
            # Alignments
            if col_idx in [1, 7]:
                c.alignment = Alignment(horizontal="center", vertical="center")
            else:
                c.alignment = Alignment(horizontal="left", vertical="center")

    # Leave 300 blank formatted rows for Secretariat to populate
    start_blank = header_row + 1 + len(sample_records)
    total_data_rows = 500

    for cur_row in range(start_blank, start_blank + 300):
        ws_main.row_dimensions[cur_row].height = 20
        is_even = cur_row % 2 == 1
        row_fill = PatternFill(start_color=zebra_tint, end_color=zebra_tint, fill_type="solid") if is_even else PatternFill(fill_type=None)
        for col_idx in range(1, 12):
            c = ws_main.cell(row=cur_row, column=col_idx)
            c.border = thin_border
            c.font = Font(name="Calibri", size=9.5)
            if is_even:
                c.fill = row_fill

    # =========================================================================
    # ADD EXCEL DATA VALIDATIONS (DROPDOWNS)
    # =========================================================================
    # Directorate Validation on Col D
    dv_dept = DataValidation(
        type="list",
        formula1=f"=System_Lookup_Values!$A$2:$A${len(CBK_DEPARTMENTS)+1}",
        allow_blank=True
    )
    dv_dept.error ='Please select a valid Central Bank Directorate from the dropdown list.'
    dv_dept.errorTitle = 'Invalid Directorate'
    dv_dept.prompt = 'Select Directorate from the list'
    dv_dept.promptTitle = 'CBK Directorate'
    ws_main.add_data_validation(dv_dept)
    dv_dept.add(f"D{header_row+1}:D{total_data_rows}")

    # Primary Sport Validation on Col E
    dv_sport = DataValidation(
        type="list",
        formula1=f"=System_Lookup_Values!$B$2:$B${len(ALL_18_SPORTS)+1}",
        allow_blank=True
    )
    dv_sport.error ='Please select one of the 18 official CBK sporting disciplines.'
    dv_sport.errorTitle = 'Invalid Discipline'
    dv_sport.prompt = 'Choose primary registered discipline'
    dv_sport.promptTitle = '18 CBK Disciplines'
    ws_main.add_data_validation(dv_sport)
    dv_sport.add(f"E{header_row+1}:E{total_data_rows}")

    # Secondary Sport Validation on Col F
    dv_sport2 = DataValidation(
        type="list",
        formula1=f"=System_Lookup_Values!$B$2:$B${len(ALL_18_SPORTS)+1}",
        allow_blank=True
    )
    ws_main.add_data_validation(dv_sport2)
    dv_sport2.add(f"F{header_row+1}:F{total_data_rows}")

    # Role Validation on Col H
    dv_role = DataValidation(
        type="list",
        formula1=f"=System_Lookup_Values!$C$2:$C${len(ROLES)+1}",
        allow_blank=True
    )
    ws_main.add_data_validation(dv_role)
    dv_role.add(f"H{header_row+1}:H{total_data_rows}")

    # Medical Clearance Validation on Col I
    dv_med = DataValidation(
        type="list",
        formula1=f"=System_Lookup_Values!$D$2:$D${len(MEDICAL_STATUSES)+1}",
        allow_blank=True
    )
    ws_main.add_data_validation(dv_med)
    dv_med.add(f"I{header_row+1}:I{total_data_rows}")

    # Freeze header rows
    ws_main.freeze_panes = f"A{header_row+1}"

    # =========================================================================
    # POPULATE INSTRUCTIONS & GUIDELINES (SHEET 2)
    # =========================================================================
    ws_inst.column_dimensions["A"].width = 24
    ws_inst.column_dimensions["B"].width = 38
    ws_inst.column_dimensions["C"].width = 55

    ws_inst.merge_cells("A1:C1")
    ws_inst["A1"] = "CBK STRIDE™ — SECRETARIAT ROSTER POPULATION GUIDE"
    ws_inst["A1"].font = Font(name="Calibri", size=14, bold=True, color=white)
    ws_inst["A1"].fill = PatternFill(start_color=navy_dark, end_color=navy_dark, fill_type="solid")
    ws_inst["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws_inst.row_dimensions[1].height = 28

    instructions_data = [
        ("Field Name", "Requirement & Validation", "Description & Operational Guidance"),
        ("Staff ID / Payroll No.*", "MANDATORY (Unique)", "CBK Staff Payroll Number (e.g. 1008 or CBK-1008). Used as the primary key for QR pass issuance and stipend tracking."),
        ("Full Official Name*", "MANDATORY", "Official staff name as registered in CBK Human Resources records."),
        ("Institutional Email*", "MANDATORY (@centralbank.go.ke)", "Used to dispatch instant dual-gate verification receipts, digital QR passes, and magic access links."),
        ("Directorate / Department*", "MANDATORY (Dropdown)", "Select official directorate from the dropdown. Used for HR wellness participation metrics and inter-directorate cups."),
        ("Primary Enrolled Sport*", "MANDATORY (Dropdown)", "Choose from the 18 official CBK disciplines (A-Z). Links the athlete directly to their Captain's station and squad roster."),
        ("Secondary Sport", "OPTIONAL (Dropdown)", "Optional secondary game for multi-sport athletes. Athletes can participate across both disciplines."),
        ("Mobile / WhatsApp Phone", "OPTIONAL (Recommended)", "Mobile number for WhatsApp dispatching of the CBK STRIDE™ Digital QR Card."),
        ("Assigned Squad Role*", "MANDATORY (Dropdown)", "Default is 'Athlete / Player'. Use 'Team Captain' for discipline leads who operate the iPad kiosk terminals."),
        ("Medical Fitness Clearance*", "MANDATORY (Dropdown)", "Ensures compliance with CBK Occupational Health & Wellness policy prior to competitive tournament play."),
        ("Emergency Contact", "OPTIONAL (Safety)", "Next of kin or emergency contact details on file with the medical pavilion during sports camps."),
        ("Discipline Notes / Hcp", "OPTIONAL", "Relevant sports metadata (e.g. Golf handicap, track distance category, soccer squad position).")
    ]

    for idx, (f_name, f_req, f_desc) in enumerate(instructions_data, start=3):
        is_head = idx == 3
        ws_inst.row_dimensions[idx].height = 25 if is_head else 22
        for c_idx, val in enumerate([f_name, f_req, f_desc], start=1):
            c = ws_inst.cell(row=idx, column=c_idx, value=val)
            c.border = thin_border
            if is_head:
                c.font = Font(name="Calibri", size=10, bold=True, color=white)
                c.fill = PatternFill(start_color=navy_dark, end_color=navy_dark, fill_type="solid")
                c.alignment = Alignment(horizontal="center", vertical="center")
            else:
                c.font = Font(name="Calibri", size=9.5, bold=(c_idx==1))
                c.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)

    # Save Excel workbook
    wb.save(XLSX_PATH)
    print(f"Successfully generated Excel template: {XLSX_PATH}")

    # Generate companion CSV Template
    csv_rows = []
    for r in sample_records:
        csv_rows.append({
            "Staff ID": r[0],
            "Full Name": r[1],
            "CBK Email": r[2],
            "Department": r[3],
            "Primary Sport": r[4],
            "Secondary Sport": r[5],
            "Phone Number": r[6],
            "Role": r[7],
            "Medical Clearance": r[8],
            "Emergency Contact": r[9],
            "Discipline Notes": r[10]
        })
    df_csv = pd.DataFrame(csv_rows)
    df_csv.to_csv(CSV_PATH, index=False)
    print(f"Successfully generated CSV template: {CSV_PATH}")

if __name__ == "__main__":
    build_template()
