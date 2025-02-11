# csv2xlsx_util library / utilities
# converting csv output of the plotted graph into a .xlsx file using openpyxl


import openpyxl
from PyQt6.QtWidgets import QFileDialog

# creating xlsx file directly graph data
def save_xlsx(self, values):

    if not isinstance(values, list) or len(values) < 4:
        print("[E]: Invalid values:", values)
        return

    mac_id = str(values[3])
    file_name = f"{mac_id.replace(':', '-')}_{values[2]}m_{values[0] * 60 + values[1]}s.xlsx"
    xlsx_file_path,_ = QFileDialog.getSaveFileName(self, "Save XLSX File", file_name, "Excel Files (*.xlsx)")

    if not xlsx_file_path:
        return  # User canceled the dialog

    x_data, y_data = self.line.getData()

    if not x_data or not y_data:
        print("[E]: No data available to save.")
        return

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "RSSI Data"
    ws.append(["Time (s)", "RSSI (-dBm)"])

    for i in range(len(x_data)):
        ws.append([x_data[i], y_data[i]])

    wb.save(xlsx_file_path)
    print(f"[I]: Saved .xlsx file to: {xlsx_file_path}")


# ========================csv dependency=============================================

# import csv
# import openpyxl
# import os
#
# def csv_to_xlsx(csv_file, xlsx_file = None):
#
#     if not os.path.exists(csv_file):
#         print ("[W] No csv file found at location")
#         return None
#
#     xl_book = openpyxl.Workbook()
#     xl_line = xl_book.active
#
#     with open(csv_file, 'r', newline = '',encoding = 'utf-8') as x:
#         reader = csv.reader(x, delimiter = ',')
#         for row in reader:
#             xl_line.append(row)
#
#     if xlsx_file is None:
#         xlsx_file = csv_file.replace(".csv", ".xlsx")
#
#     print (f"saving xlsx file to location {xlsx_file}")
#     xl_book.save(xlsx_file)
#     return xlsx_file