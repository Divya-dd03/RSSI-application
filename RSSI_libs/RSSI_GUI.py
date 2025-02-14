# ====================RSSI_GUI Application===============================
# This script is used to define, setup and initialize the 
# application's User Interface for scanning nearby BLE devices

# Importing required libraries
# GUI -> handles graphics -> font, image, icon
# Widgets -> UI components -> buttons, windows, layouts
# Widgets -> File dialog for file handling, downloading, etc.
# PyQtGraph -> for real-time plotting: RSSI vs time, downloading CSV and image files
# Core -> core functionalities -> event handling, threading

# Import custom libraries
# RSSI_GUI -> UI components, handling signals and slots
# graph2xlsx_util -> converting graph image file to .xlsx file
# Bluetooth_script1 -> devices available printed at tab3
# RT_rssi_util -> Recording Real-Time RSSI graph at tab4

from PyQt6.QtWidgets import *
from PyQt6.QtCore import pyqtSignal
from pyqtgraph.exporters import ImageExporter, CSVExporter
import pyqtgraph as pg

from RSSI_libs import graph2xlsx_util
from RSSI_libs.Bluetooth_script1 import BleTable
from RSSI_libs.RT_rssi_util import RtBLEScanning


class MainWindow(QMainWindow):
    """
    Main window for the RSSI_GUI application.
    """

    # Signals should be directly under a class and not instances of tabs created
    signal1 = pyqtSignal(int)
    signal2 = pyqtSignal(int)
    signal3 = pyqtSignal(int)
    signal4 = pyqtSignal(str)
    signal_cluster = pyqtSignal(list)

    def __init__(self, *args, **kwargs):
        """
        Initialize the main window.
        """
        super(MainWindow, self).__init__(*args, **kwargs)
        self.values = [0, 0, 0, 0]

        self.setWindowTitle("RSSI_GUI")
        self.setGeometry(100, 100, 600, 400)

        # Set table for tab3
        self.ble = BleTable()

        # Update table by connecting signal -> tab3
        self.ble.devices_found.connect(self.update_table)

        # Set graph for tab4
        self.rt = RtBLEScanning()

        # Update graph by connecting signal -> tab4
        self.rt.plot_list_signal.connect(self.rt_graph_update)

        # Create base layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.tab = QGridLayout()
        self.central_widget.setLayout(self.tab)

        # UI -> Tabs inside main window = 4
        self.tab1 = QTextEdit("Inputs")
        self.tab2 = QTextEdit("Outputs")
        self.tab3 = QTableWidget()
        self.tab4 = pg.PlotWidget()

        # Connect the signals to the respective functions
        self.setup_tabs()
        self.input_layout_setup()
        self.output_layout_setup()
        self.device_table_setup()
        self.rt_graph_setup(self.values)

    def setup_tabs(self):
        """
        Setup the tabs in the main window.
        """
        self.tab1.setFixedWidth(270)
        self.tab2.setFixedWidth(270)
        self.tab1.setFixedHeight(250)
        self.tab2.setFixedHeight(250)

        self.tab.addWidget(self.tab1, 0, 0)
        self.tab.addWidget(self.tab2, 1, 0)
        self.tab.addWidget(self.tab3, 0, 1)
        self.tab.addWidget(self.tab4, 1, 1)

        self.tab1.setReadOnly(True)
        self.tab2.setReadOnly(True)

    def input_layout_setup(self):
        """
        Setup the input layout in tab1.
        """
        input_layout = QFormLayout()
        input_layout.setContentsMargins(30, 30, 30, 0)

        state1 = QPushButton("scan start")
        state2 = QPushButton("scan stop")

        state = QHBoxLayout()
        state.addWidget(state1)
        state.addWidget(state2)

        state1.setCheckable(True)
        state1.clicked.connect(self.ble.scan_start)

        state2.setCheckable(True)
        state2.clicked.connect(self.ble.scan_stop)

        self.tab1.time_min_spinbox = QSpinBox()
        self.tab1.time_min_spinbox.setMinimum(0)
        self.tab1.time_min_spinbox.setMaximum(60)
        self.tab1.time_min_spinbox.setValue(0)

        self.tab1.time_sec_spinbox = QSpinBox()
        self.tab1.time_sec_spinbox.setMinimum(0)
        self.tab1.time_sec_spinbox.setMaximum(60)
        self.tab1.time_sec_spinbox.setValue(0)

        self.tab1.distance_spinbox = QSpinBox()
        self.tab1.distance_spinbox.setMinimum(0)
        self.tab1.distance_spinbox.setMaximum(100)
        self.tab1.distance_spinbox.setValue(0)

        self.tab1.mac_id = QLineEdit()

        self.tab1.time = QHBoxLayout()
        self.tab1.time.addWidget(self.tab1.time_min_spinbox)
        self.tab1.minute = QLabel("min")
        self.tab1.time.setSpacing(10)
        self.tab1.sec = QLabel("sec")
        self.tab1.time.addWidget(self.tab1.minute)
        self.tab1.time.addWidget(self.tab1.time_sec_spinbox)
        self.tab1.time.addWidget(self.tab1.sec)

        self.tab1.inputs = QLineEdit()
        self.tab1.inputs.setReadOnly(True)

        func = QHBoxLayout()
        self.tab1.done = QPushButton("Submit")
        func.addWidget(self.tab1.done)
        self.tab1.done.setFixedWidth(100)
        self.tab1.done.setCheckable(True)
        self.tab1.done.toggled.connect(self.user_ack)

        self.tab1.clear = QPushButton("clear")
        func.addWidget(self.tab1.clear)
        self.tab1.clear.setFixedWidth(100)
        self.tab1.clear.setCheckable(True)
        self.tab1.clear.clicked.connect(self.clear_field)

        input_layout.addRow(state1)
        input_layout.addRow(state2)
        input_layout.addRow("Time", self.tab1.time)
        input_layout.addRow("Distance (m)", self.tab1.distance_spinbox)
        input_layout.addRow("MAC ID", self.tab1.mac_id)
        input_layout.addRow("i/p given", self.tab1.inputs)
        input_layout.addRow(func)

        self.tab1.setLayout(input_layout)

        self.tab1.time_min_spinbox.valueChanged.connect(lambda value: self.internal_update(0, value))
        self.tab1.time_sec_spinbox.valueChanged.connect(lambda value: self.internal_update(1, value))
        self.tab1.distance_spinbox.valueChanged.connect(lambda value: self.internal_update(2, value))
        self.tab1.mac_id.textChanged.connect(lambda text: self.internal_update(3, text))

        self.signal_cluster.connect(self.update_inputs_qline)

    def internal_update(self, index, value):
        """
        Internal update function to handle value changes.

        Args:
            index (int): The index of the value to update.
            value (any): The new value.
        """
        self.values[index] = value
        print("[I]: Internal update, emitting signal: signal_cluster", self.values)
        self.signal_cluster.emit(self.values)

    def update_inputs_qline(self):
        """
        Update the input QLineEdit field with the current values.
        """
        self.tab1.inputs.setText(f"{self.values}")

    def user_ack(self):
        """
        Handle user acknowledgment for the inputs.
        """
        if self.tab1.done.isChecked():
            print("[I]: Received ack from user for inputs...")
            self.signal_cluster.connect(self.rt.start_scanning)
            self.signal_cluster.connect(self.rt_graph_setup)
            self.signal_cluster.emit(self.values)

    def clear_field(self):
        """
        Clear all input fields.
        """
        if self.tab1.clear.isChecked():
            self.tab1.time_min_spinbox.clear()
            self.tab1.time_sec_spinbox.clear()
            self.tab1.distance_spinbox.clear()
            self.tab1.mac_id.clear()
            self.tab1.inputs.clear()
        print("[I]: Cleared all input fields")

    def output_layout_setup(self):
        """
        Setup the output layout in tab2.
        """
        output_layout = QFormLayout()
        output_layout.setContentsMargins(30, 30, 30, 30)

        button1 = QPushButton(".csv Download")
        button2 = QPushButton(".xlsx Download")
        button3 = QPushButton("Graph Download")

        button1.setCheckable(True)
        button1.clicked.connect(lambda: self.save_csv(self.values))

        button2.setCheckable(True)
        button2.clicked.connect(lambda: self.save_xlsx(self.values))

        button3.setCheckable(True)
        button3.clicked.connect(lambda: self.save_graph(self.values))

        self.tab2.avg_rssi = QLineEdit()
        self.tab2.avg_rssi.setReadOnly(True)
        self.tab2.pkt_drop = QLineEdit()
        self.tab2.pkt_drop.setReadOnly(True)

        self.tab2.avg_rssi.setText("-")
        self.tab2.pkt_drop.setText("-")

        func = QHBoxLayout()
        refresh_app = QPushButton("Refresh")
        func.addWidget(refresh_app)
        refresh_app.setCheckable(True)
        refresh_app.setFixedWidth(100)
        refresh_app.clicked.connect(self.refresh_app)

        exit_app = QPushButton("Exit")
        func.addWidget(exit_app)
        exit_app.setCheckable(True)
        exit_app.setFixedWidth(100)
        exit_app.clicked.connect(self.exit_app)

        output_layout.addRow(button1)
        output_layout.addRow(button2)
        output_layout.addRow(button3)
        output_layout.addRow("Average RSSI", self.tab2.avg_rssi)
        output_layout.addRow("Packet drop %", self.tab2.pkt_drop)
        output_layout.addRow(func)

        self.tab2.setLayout(output_layout)

    def device_table_setup(self):
        """
        Setup the device table in tab3.
        """
        self.tab3.setColumnCount(4)
        self.tab3.setHorizontalHeaderLabels(["RSSI", "MAC ID", "Device name", "Manufuc.data"])
        self.tab3.setColumnWidth(0, 70)
        self.tab3.setColumnWidth(1, 100)
        self.tab3.setColumnWidth(2, 150)
        self.tab3.setColumnWidth(3, 700)

    def update_table(self, dev_list):
        """
        Update the device table with scanned devices.

        Args:
            dev_list (list): A list of tuples containing device details.
        """
        self.tab3.setRowCount(len(dev_list))

        for row, (mac, rssi, name, manuf_data) in enumerate(dev_list):
            self.tab3.setItem(row, 0, QTableWidgetItem(str(rssi)))
            self.tab3.setItem(row, 1, QTableWidgetItem(mac))
            self.tab3.setItem(row, 2, QTableWidgetItem(name if name else "None"))
            self.tab3.setItem(row, 3, QTableWidgetItem(str(manuf_data)))

    def save_xlsx(self, values):
        """
        Save the graph data as an XLSX file.

        Args:
            values (list): A list containing the necessary values for the file name and data validation.
        """
        graph2xlsx_util.save_xlsx(self, values)

    def save_csv(self, values):
        """
        Save the graph data as a CSV file.

        Args:
            values (list): A list containing the necessary values for the file name and data validation.
        """
        mac_id = str(values[3])
        file_name = f"{mac_id.replace(':', '-')}_{values[2]}m_{values[0] * 60 + values[1]}s.csv"
        csv_file_path, _ = QFileDialog.getSaveFileName(self, "Save CSV File", file_name, "CSV Files (*.csv)")
        if csv_file_path:
            csv_file = CSVExporter(self.tab4.plotItem)
            csv_file.export(csv_file_path)
            print(f"[I]: Saved .csv file to location: {csv_file_path}")
        return csv_file_path

    def save_graph(self, values):
        """
        Save the graph as an image file.

        Args:
            values (list): A list containing the necessary values for the file name and data validation.
        """
        mac_id = str(values[3])
        file_name = f"{mac_id.replace(':', '-')}_{values[2]}m_{values[0] * 60 + values[1]}s.png"
        image_file_path, _ = QFileDialog.getSaveFileName(self, "Save Graph Image", file_name, "PNG files (*.png);;JPEG (*.jpg);;PDF Files (*.pdf)")

        if image_file_path:
            image = ImageExporter(self.tab4.plotItem)
            image.export(image_file_path)
            print(f"[I]: Saved graph to location: {image_file_path}")

    def rt_graph_setup(self, values):
        """
        Setup the real-time graph in tab4.

        Args:
            values (list): A list containing the necessary values for the graph setup.
        """
        print(f"[I]: Graph setup received values: {values}")

        self.tab4.setBackground("k")
        self.tab4.setTitle(
            f"RSSI graph for dev: {values[3]}, distance = {values[2]}m, scanned_duration = {values[0]}m{values[1]}s",
            color="c",
            size="10pt",
        )
        self.tab4.setLabels(left="RSSI (-dBm)", bottom="Time (s)")
        self.tab4.setYRange(-130, 0)
        self.tab4.setXRange(0, 120)
        self.tab4.addLegend()
        self.tab4.showGrid(x=True, y=True)

        self.tab4.getAxis("left").setPen(pg.mkPen(color="w", width=2))
        self.tab4.getAxis("bottom").setPen(pg.mkPen(color="w", width=2))

        pen = pg.mkPen("g", width=2)
        self.line = self.tab4.plot([], [], pen=pen, symbol="+", symbolSize=5, symbolBrush="g")

        print(f"[I]: Graph title updated to: RSSI graph for dev: {values}")

    def rt_graph_update(self, plot_list):
        """
        Update the real-time graph with new data.

        Args:
            plot_list (list): A list containing the time stamps and RSSI values.
        """
        print("[I]: Incoming plot details:", plot_list)

        if not plot_list or len(plot_list) < 2:
            print("[E]: Dev not found / Not enough values captured. Scan again...")
            return

        time_stamps, rssi_list = plot_list[:2]

        print("[I]: Plotting - X:", time_stamps)
        print("[I]: Plotting - Y:", rssi_list)

        self.tab4.setXRange(min(time_stamps), max(time_stamps))
        self.line.setData(time_stamps, rssi_list)

        if len(plot_list) == 4:
            avg_rssi = plot_list[2]
            pkt_drop = plot_list[3]
            if avg_rssi is not None and pkt_drop is not None:
                self.tab2.avg_rssi.setText(f"{avg_rssi:.2f}dBm")
                self.tab2.pkt_drop.setText(f"{pkt_drop:.2f}%")
            else:
                self.tab2.avg_rssi.setText("-")
                self.tab2.pkt_drop.setText("-")

    def refresh_app(self):
        """
        Refresh the application UI.
        """
        print("[I]: Refreshing Application...")

        self.tab1.time_min_spinbox.setValue(0)
        self.tab1.time_sec_spinbox.setValue(0)
        self.tab1.distance_spinbox.setValue(0)
        self.tab1.mac_id.clear()
        self.tab1.inputs.clear()

        self.tab2.avg_rssi.setText("-")
        self.tab2.pkt_drop.setText("-")

        self.ble.scan_stop()
        self.tab3.setRowCount(0)

        self.rt.scan_stop()
        self.line.setData([], [])

        print("[I]: Application UI has been refreshed!")

    def exit_app(self):
        """
        Exit the application.
        """
        print("[I]: Exiting app now...")

        self.refresh_app()
        QApplication.quit()

        print("[I]: App exit--- \nThank you for trying me out \nSee you next time ;)")


# Uncomment the following lines if you want to run this file directly
# if __name__ == "__main__":
#     RSSI_GUI = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     RSSI_GUI.exec()