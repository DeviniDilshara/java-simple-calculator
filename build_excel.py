import json
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

v1 = json.load(open("v1_results.json"))
v2 = json.load(open("v2_results.json"))
v1_by_id = {t["id"]: t for t in v1}
v2_by_id = {t["id"]: t for t in v2}

GITHUB_URL_PLACEHOLDER = "PASTE_YOUR_GITHUB_REPO_URL_HERE_AFTER_PUSHING"

wb = Workbook()

# ---------- Sheet 1: Test Case Results ----------
ws = wb.active
ws.title = "Test Case Results"

HEADER_FILL = PatternFill("solid", fgColor="1F4E78")
HEADER_FONT = Font(name="Arial", bold=True, color="FFFFFF", size=11)
PASS_FILL = PatternFill("solid", fgColor="C6EFCE")
FAIL_FILL = PatternFill("solid", fgColor="FFC7CE")
BASE_FONT = Font(name="Arial", size=10)
TITLE_FONT = Font(name="Arial", bold=True, size=14)
SUB_FONT = Font(name="Arial", italic=True, size=10, color="404040")
thin = Side(style="thin", color="B7B7B7")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)

ws.merge_cells("A1:K1")
ws["A1"] = "Simple Calculator - Test Case Scenarios & Results"
ws["A1"].font = TITLE_FONT

ws["A2"] = "GitHub Project URL:"
ws["A2"].font = Font(name="Arial", bold=True, size=10)
ws.merge_cells("B2:K2")
ws["B2"] = GITHUB_URL_PLACEHOLDER
ws["B2"].font = Font(name="Arial", size=10, color="CC0000", italic=True)

ws.merge_cells("A3:K3")
ws["A3"] = ("Application: Python CLI Calculator  |  Tested versions: v1.0.0 (initial) "
            "and v2.0.0 (bug-fix release)")
ws["A3"].font = SUB_FONT

headers = [
    "TC ID", "Test Scenario / Description", "Operation", "Input(s)", "Expected Result",
    "Actual Result (v1.0.0)", "Status (v1.0.0)",
    "Actual Result (v2.0.0)", "Status (v2.0.0)",
    "Defect Raised?", "Notes / Fix Applied",
]
header_row = 5
for col, h in enumerate(headers, start=1):
    c = ws.cell(row=header_row, column=col, value=h)
    c.font = HEADER_FONT
    c.fill = HEADER_FILL
    c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
    c.border = BORDER

notes_map = {
    "TC005": "Bug found: subtract() returned b-a instead of a-b. Fixed in v2.0.0 by swapping operand order.",
    "TC007": "Bug found: divide() crashed with unhandled ZeroDivisionError. Fixed in v2.0.0: now returns a graceful 'Error: Cannot divide by zero' message.",
    "TC011": "Bug found: square_root() crashed with unhandled ValueError for negative input. Fixed in v2.0.0: now returns a graceful 'Error: Cannot compute square root of a negative number' message.",
}

row = header_row + 1
for tc in v1:
    tc_id = tc["id"]
    v1r = v1_by_id[tc_id]
    v2r = v2_by_id[tc_id]
    inputs_str = ", ".join(str(x) for x in tc["inputs"])
    expected = "Graceful error message (no crash)" if tc["expected"] == "ERROR_HANDLED" else tc["expected"]
    defect = "Yes" if v1r["status"] == "FAIL" else "No"
    note = notes_map.get(tc_id, "No issues found.")

    values = [
        tc_id, tc["description"], tc["function"], inputs_str, expected,
        v1r["actual"], v1r["status"],
        v2r["actual"], v2r["status"],
        defect, note,
    ]
    for col, val in enumerate(values, start=1):
        c = ws.cell(row=row, column=col, value=val)
        c.font = BASE_FONT
        c.alignment = Alignment(wrap_text=True, vertical="top")
        c.border = BORDER
        if col == 7:  # Status v1.0.0
            c.fill = PASS_FILL if val == "PASS" else FAIL_FILL
            c.font = Font(name="Arial", size=10, bold=True)
            c.alignment = Alignment(horizontal="center", vertical="center")
        if col == 9:  # Status v2.0.0
            c.fill = PASS_FILL if val == "PASS" else FAIL_FILL
            c.font = Font(name="Arial", size=10, bold=True)
            c.alignment = Alignment(horizontal="center", vertical="center")
    row += 1

last_data_row = row - 1

# Summary block
summary_row = row + 1
ws.cell(row=summary_row, column=1, value="Summary").font = Font(name="Arial", bold=True, size=12)
summary_row += 1
labels = [
    ("Total Test Cases", f"=COUNTA(A{header_row+1}:A{last_data_row})"),
    ("Passed on v1.0.0", f'=COUNTIF(G{header_row+1}:G{last_data_row},"PASS")'),
    ("Failed on v1.0.0", f'=COUNTIF(G{header_row+1}:G{last_data_row},"FAIL")'),
    ("Passed on v2.0.0", f'=COUNTIF(I{header_row+1}:I{last_data_row},"PASS")'),
    ("Failed on v2.0.0", f'=COUNTIF(I{header_row+1}:I{last_data_row},"FAIL")'),
    ("Defects Found & Fixed", f'=COUNTIF(J{header_row+1}:J{last_data_row},"Yes")'),
]
for label, formula in labels:
    ws.cell(row=summary_row, column=1, value=label).font = Font(name="Arial", bold=True, size=10)
    fc = ws.cell(row=summary_row, column=2, value=formula)
    fc.font = BASE_FONT
    fc.alignment = Alignment(horizontal="center")
    summary_row += 1

# Column widths
widths = [8, 34, 12, 14, 26, 30, 14, 30, 14, 12, 42]
for i, w in enumerate(widths, start=1):
    ws.column_dimensions[get_column_letter(i)].width = w

ws.freeze_panes = "A6"

# ---------- Sheet 2: Version History ----------
ws2 = wb.create_sheet("Version History")
ws2.merge_cells("A1:D1")
ws2["A1"] = "Version Control Log (GitHub)"
ws2["A1"].font = TITLE_FONT

vh_headers = ["Version (Git Tag)", "Date", "Change Summary", "Test Result"]
for col, h in enumerate(vh_headers, start=1):
    c = ws2.cell(row=3, column=col, value=h)
    c.font = HEADER_FONT
    c.fill = HEADER_FILL
    c.border = BORDER
    c.alignment = Alignment(horizontal="center", wrap_text=True)

vh_rows = [
    ["v1.0.0", "2026-09-27", "Initial commit: CLI calculator with add, subtract, multiply, divide, power, square root.", "9/12 test cases passed. 3 defects found: TC005 (subtract order), TC007 (divide-by-zero crash), TC011 (negative sqrt crash)."],
    ["v2.0.0", "2026-09-27", "Bug-fix release: corrected subtract() operand order; divide() and square_root() now return graceful error messages instead of crashing.", "12/12 test cases passed. All defects closed."],
]
r = 4
for row_vals in vh_rows:
    for col, val in enumerate(row_vals, start=1):
        c = ws2.cell(row=r, column=col, value=val)
        c.font = BASE_FONT
        c.border = BORDER
        c.alignment = Alignment(wrap_text=True, vertical="top")
    r += 1

ws2.column_dimensions["A"].width = 16
ws2.column_dimensions["B"].width = 12
ws2.column_dimensions["C"].width = 55
ws2.column_dimensions["D"].width = 55

ws2["A7"] = "GitHub Repository URL:"
ws2["A7"].font = Font(name="Arial", bold=True, size=10)
ws2["B7"] = GITHUB_URL_PLACEHOLDER
ws2["B7"].font = Font(name="Arial", size=10, color="CC0000", italic=True)
ws2.merge_cells("B7:D7")

wb.save("Calculator_Test_Cases.xlsx")
print("saved")
