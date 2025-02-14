# ==========================csv2xlsx_util===============================
# This script is used to convert the CSV data to an XLSX file 
# for better data visualization.

import openpyxl
from PyQt6.QtWidgets import QFileDialog

def save_xlsx(self, values):
    """
    Create and save an XLSX file from the graph data.

    Args:
        values (list): A list containing the necessary
        values for the file name and data validation.
    """
    if not isinstance(values, list) or len(values) < 4:
        print("[E]: Invalid values:", values)
        return

    mac_id = str(values[3])
    file_name = f"{mac_id.replace(':', '-')}_{values[2]}m_{values[0] * 60 + values[1]}s.xlsx"
    xlsx_file_path, _ = QFileDialog.getSaveFileName(self, "Save XLSX File", file_name, "Excel Files (*.xlsx)")

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