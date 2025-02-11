# @author Divya Dharshini
# @date 31-01-2025
# @app RSSI_GUI

# importing existing req. libraries
# gui -> handles graphics -> font, image, icon
# widgets -> UI components -> buttons, windows, layouts
# widgets -> File dialog for file handling, downloading, etc.
# pyqtgraph -> for real-tile plotting : rssi vs time, downloading csv and img files
# core -> core functionalities -> event handling, threading

# import custom libraries
# RSSI_GUI -> UI components, handling signals and slots
# graph2xlsx_util -> converting graph image file to .xlsx file
# Bluetooth_script1 -> devices available printed at tab3
# RT_rssi_util -> Recording Real-Time RSSI graph at tab4

from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QFileDialog
from pyqtgraph.exporters import ImageExporter, CSVExporter
import pyqtgraph as pg

from RSSI_libs import graph2xlsx_util
from RSSI_libs.Bluetooth_script1 import BleTable
from RSSI_libs.RT_rssi_util import RtBLEScanning


# QThread? -> for managing async loops between RSSI_lib files, assisting asyncio imports


# QMainWindow for UI components
class MainWindow(QMainWindow):

# ================================OUTER TABS============================================================================

    # signals should be directly under a class and not instances of tabs created
    signal1 = pyqtSignal(int)
    signal2 = pyqtSignal(int)
    signal3 = pyqtSignal(int)
    signal4 = pyqtSignal(str)

    signal_cluster = pyqtSignal(list)

    # __init__ -> constructor method -> accepts optional arguments.
    def __init__(self, *args, **kwargs):

        # initialize main window : RSSI_GUI
        super(MainWindow, self).__init__(*args, **kwargs)
        # QObject.__init__(self)
        self.values = [0, 0, 0, 0]

        self.setWindowTitle("RSSI_GUI")
        self.setGeometry(100, 100, 600, 400)

        # set table for tab3
        self.ble = BleTable()

        # update table by connecting signal -> tab3
        self.ble.devices_found.connect(self.update_table)

        # update graph by connecting signal_cluster -> tab4
        # self.signal_cluster.connect(self.rt_graph_setup)

        # set graph for tab4
        self.rt = RtBLEScanning()

        # update RT_rssi_util by connecting it to RtBLEScanning class -> utils
        # self.signal_cluster.connect(self.rt.start_scanning)

        # connect avg_rssi and packet_drop to update output layout
        # self.rt.param_signal.connect(self.output_layout_setup)
        # self.rt.plot_list_signal.connect(self.update_output_layout)

        # update graph by connecting signal -> tab4
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

        # connect the signals to the respective functions
        # self.input_tuple_signal.connect(self.input_layout_setup)
        # calling all setup functions
        self.setup_tabs()
        self.input_layout_setup()
        self.output_layout_setup()
        self.device_table_setup()
        self.rt_graph_setup(self.values)


    def setup_tabs(self):

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

# ==============================INPUT GRID -1===========================================================================


    def input_layout_setup(self):

        # create QFormLayout layout and add buttons
        # text entering & input number entering
        input_layout = QFormLayout()

        # Top margin set to 10 for spacing
        input_layout.setContentsMargins(30, 30, 30, 0)

        # state buttons - for scanning
        state1 = QPushButton("scan start")
        state2 = QPushButton("scan stop")

        # states layouts
        state = QHBoxLayout()
        state.addWidget(state1)
        state.addWidget(state2)

        # make states responsive
        state1.setCheckable(True)
        state1.clicked.connect(self.ble.scan_start)

        state2.setCheckable(True)
        state2.clicked.connect(self.ble.scan_stop)

        # set min. max. init. values for time - min
        self.tab1.time_min_spinbox = QSpinBox()
        self.tab1.time_min_spinbox.setMinimum(0)
        self.tab1.time_min_spinbox.setMaximum(60)
        self.tab1.time_min_spinbox.setValue(0)

        # set min. max. init. values for time - sec
        self.tab1.time_sec_spinbox = QSpinBox()
        self.tab1.time_sec_spinbox.setMinimum(0)
        self.tab1.time_sec_spinbox.setMaximum(60)
        self.tab1.time_sec_spinbox.setValue(0)

        # set min. max. init. values for distance - meter
        self.tab1.distance_spinbox = QSpinBox()
        self.tab1.distance_spinbox.setMinimum(0)
        self.tab1.distance_spinbox.setMaximum(100)
        self.tab1.distance_spinbox.setValue(0)

        # MAC_ID field as a string input
        self.tab1.mac_id = QLineEdit()

        # for time min and sec
        self.tab1.time = QHBoxLayout()
        self.tab1.time.addWidget(self.tab1.time_min_spinbox)
        self.tab1.minute = QLabel("min")
        self.tab1.time.setSpacing(10)
        self.tab1.sec = QLabel("sec")
        self.tab1.time.addWidget(self.tab1.minute)
        self.tab1.time.addWidget(self.tab1.time_sec_spinbox)
        self.tab1.time.addWidget(self.tab1.sec)

        # a QLine component to view the given input
        self.tab1.inputs = QLineEdit()
        self.tab1.inputs.setReadOnly(True)

        func = QHBoxLayout()

        # acknowledgement from user upon entering the inputs
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

        # create input interactions
        input_layout.addRow(state1)
        input_layout.addRow(state2)
        input_layout.addRow("Time", self.tab1.time )
        input_layout.addRow("Distance (m)", self.tab1.distance_spinbox)
        input_layout.addRow("MAC ID", self.tab1.mac_id)
        input_layout.addRow("i/p given", self.tab1.inputs)
        input_layout.addRow(func)

        self.tab1.setLayout(input_layout)

        # Connect individual signal value changes to the update function
        self.tab1.time_min_spinbox.valueChanged.connect(lambda value: self.internal_update(0, value))
        self.tab1.time_sec_spinbox.valueChanged.connect(lambda value: self.internal_update(1, value))
        self.tab1.distance_spinbox.valueChanged.connect(lambda value: self.internal_update(2, value))
        self.tab1.mac_id.textChanged.connect(lambda text: self.internal_update(3, text))

        self.signal_cluster.connect(self.update_inputs_qline)


    # the values are being appended -> suffix since prepending with prefix affects the signal
    def internal_update(self, index, value):

        self.values[index] = value
        print("[I]: Internal update, emitting signal: signal_cluster",self.values)
        self.signal_cluster.emit(self.values)

    # update values at qLineText field -> inputs
    # setText to continuously check for changes in the text
    def update_inputs_qline(self):
        self.tab1.inputs.setText(f"{self.values}")


    # for submit button -> finalizing the inputs
    def user_ack(self):

        """ emit to the following:
        1. values list -> Rt_rssi_util.RtBLEScanning class
        2. values list -> rt_graph_update - display details
        3. values list -> image name: <" "-mac_id-distance-time_duration>
        """

        if self.tab1.done.isChecked():
            # print ("values:", self.values)
            print ("[I]: Received ack from user for inputs...")

            # received ack? fire signal and connect to util: RT_rssi_util
            self.signal_cluster.connect(self.rt.start_scanning)

            # update graph by connecting signal_cluster -> tab4
            self.signal_cluster.connect(self.rt_graph_setup)

            self.signal_cluster.emit(self.values)

            # print ("|_Fired signal to slot -> RtBLEScanning class")
            # self.signal_cluster.emit(self.values, self.rt_graph_update)
            # print ("|_Fired signal to slot -> rt_graph_update")
            # self.signal_cluster.emit(self.values)
            # print ("|_Fired signal to slot -> rt_graph_setup")


    # for clear button -> clears all input fields
    def clear_field(self):
        if self.tab1.clear.isChecked():
            # clear the fields for the next input
            self.tab1.time_min_spinbox.clear()
            self.tab1.time_sec_spinbox.clear()
            self.tab1.distance_spinbox.clear()
            self.tab1.mac_id.clear()
            self.tab1.inputs.clear()
        print ("[I]: |_cleared all input fields")

# ================================OUTPUT GRID -2========================================================================

    def output_layout_setup(self):

        # create output interactions
        output_layout = QFormLayout()

        # Top margin set to 10 for spacing
        output_layout.setContentsMargins(30, 30, 30, 30)

        # create output buttons
        button1 = QPushButton(".csv Download")
        button2 = QPushButton(".xlsx Download")
        button3 = QPushButton("Graph Download")

        # make button 1,2,3 responsive
        button1.setCheckable(True)
        # button1.clicked.connect(button_clicked)
        button1.clicked.connect(lambda: self.save_csv(self.values))

        button2.setCheckable(True)
        # button2.clicked.connect(button_clicked)
        button2.clicked.connect(lambda: self.save_xlsx(self.values))

        button3.setCheckable(True)
        # button3.clicked.connect(button_clicked)
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

        # add-ons : refresh, exit
        output_layout.addRow(func)

        self.tab2.setLayout(output_layout)



# =============================DEVICES AVAILABLE========================================================================

    # the Bluetooth_script1 haas function devices_in_vicinity which returns a list of tuples containing device details.
    # the length of the details would be my row count, and it will be modified each time
    # Call this function inside an async Qt event loop

    # prepare the table for incoming entries
    def device_table_setup(self):

        # set number of columns
        self.tab3.setColumnCount(4)

        # set table headers
        self.tab3.setHorizontalHeaderLabels(["RSSI", "MAC ID", "Device name", "Manufuc.data"])

        # set table dimensions
        self.tab3.setColumnWidth(0, 70)
        self.tab3.setColumnWidth(1, 100)
        self.tab3.setColumnWidth(2, 150)
        self.tab3.setColumnWidth(3, 700)


    # updating table for listing devices available at the instant
    def update_table(self, dev_list):

        # set the row count based on the number of devices scanned
        self.tab3.setRowCount(len(dev_list))

        # Update the table with scanned devices
        for row, (mac, rssi, name, manuf_data) in enumerate(dev_list):
            self.tab3.setItem(row, 0, QTableWidgetItem(str(rssi)))
            self.tab3.setItem(row, 1, QTableWidgetItem(mac))
            self.tab3.setItem(row, 2, QTableWidgetItem(name if name else "None"))
            self.tab3.setItem(row, 3, QTableWidgetItem(str(manuf_data)))


    # saving tab4 graph instances as a .xlsx file
    def save_xlsx(self, values):

        # convert directly from graph plotting data:
        graph2xlsx_util.save_xlsx(self, values)

        # relies on csv file.
        # mac_id = str(values[3])
        # file_name = f"{mac_id.replace(':','-')}_{values[2]}m_{values[0]*60+values[1]}s.csv"
        # xlsx_file_path,_ = QFileDialog.getSaveFileName(self, "save xlsx file", file_name, "XLSX files (*.xlsx)")
        # if xlsx_file_path:
        #     temp_file = csv_file_path
        #     xlsx_file = csv2xlsx_util.csv_to_xlsx(temp_file)
        #     xlsx_file.export(xlsx_file_path)
        #     print(f"saved .xlsx file to location: {xlsx_file_path}")


    # saving tab4 graph instances as a .csv file
    def save_csv(self, values):

        mac_id = str(values[3])
        file_name = f"{mac_id.replace(':','-')}_{values[2]}m_{values[0]*60 + values[1]}s.csv"
        csv_file_path,_ = QFileDialog.getSaveFileName(self, "save csv file", file_name, "CSV files (*.csv)")
        if csv_file_path:
            csv_file = CSVExporter(self.tab4.plotItem)
            csv_file.export(csv_file_path)
            print(f"[I]: Saved .csv file to location: {csv_file_path}")
        return csv_file_path


    # saving tab4 graph instances as an image.
    def save_graph(self, values):

        mac_id = str(values[3])
        file_name = f"{mac_id.replace(':','-')}_{values[2]}m_{values[0]*60+values[1]}s.csv"
        image_file_path,_ = QFileDialog.getSaveFileName(self, "save graph image", file_name, "PNG files (*.png);;JPEG (*.jpg);;PDF Files (*.pdf)" )

        if image_file_path:
            # self.tab4.plotItem -> makes sure that we capture the instance of graph at tab4 recorded.
            image = ImageExporter(self.tab4.plotItem)
            image.export(image_file_path)
            print(f"[I]: saved graph to location: {image_file_path}")


# ==================================GRAPH TAB=============================================================================


    def rt_graph_setup(self, values):


        print(f"[I]: Graph setup received values: {values}")

        # Initialize the plot widget
        self.tab4.setBackground("k")  # Set black background
        self.tab4.setTitle(
            f"RSSI graph for dev: {values[3]}, distance = {values[2]}m, scanned_duration = {values[0]}m{values[1]}s",
            color="c",
            size="10pt",
        )
        self.tab4.setLabels(left="RSSI (-dBm)", bottom="Time (s)")
        self.tab4.setYRange(-130, 0)  # Set fixed RSSI range
        self.tab4.setXRange(0, 120)  # Set X-axis range
        self.tab4.addLegend()
        self.tab4.showGrid(x=True, y=True)

        # Style axis lines
        self.tab4.getAxis("left").setPen(pg.mkPen(color="w", width=2))
        self.tab4.getAxis("bottom").setPen(pg.mkPen(color="w", width=2))

        # Create a line plot with initial empty data
        pen = pg.mkPen("g", width=2)  # Green line for RSSI data
        self.line = self.tab4.plot([], [], pen=pen, symbol="+", symbolSize=5, symbolBrush="g")

        print(f"[I]: Graph title updated to: RSSI graph for dev: {values}")


    def rt_graph_update(self, plot_list):


        print("[I]: Incoming plot details:", plot_list)

        if not plot_list or len(plot_list) < 2:
            print ("[E]: Dev not found / Not enough values captured. scan again...")
            return

        time_stamps, rssi_list = plot_list[:2]

        print("[I]: Plotting - X:", time_stamps)
        print("[I]: Plotting - Y:", rssi_list)

        # Update X-axis range dynamically
        self.tab4.setXRange(min(time_stamps), max(time_stamps))

        # Update the graph with new RSSI data
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

    # # update for output layout
    # def update_output_layout(self, plot_list):
    #
    #     avg_rssi, pkt_drop = plot_list[2], plot_list[3]
    #     if isinstance(self.rt.plot_list_signal, list):
    #         self.tab2.avg_rssi.setText(f"{avg_rssi:.2f}dBm")
    #         self.tab2.pkt_drop.setText(f"{pkt_drop:.2f}%")
    #     else:
    #         self.tab2.avg_rssi.setText("-")
    #         self.tab2.pkt_drop.setText("-")

    def refresh_app(self):

        # acknowledge refreshing at terminal
        print("[I]: Refreshing Application...")

        # clear tab1 input fields
        self.tab1.time_min_spinbox.setValue(0)
        self.tab1.time_sec_spinbox.setValue(0)
        self.tab1.distance_spinbox.setValue(0)
        self.tab1.mac_id.clear()
        self.tab1.inputs.clear()

        # clear tab2 output fields
        self.tab2.avg_rssi.setText("-")
        self.tab2.pkt_drop.setText("-")

        # stop scanning and clear tab3 table
        self.ble.scan_stop()
        self.tab3.setRowCount(0)

        # clear tab4 plotting field
        self.rt.scan_stop()
        self.line.setData([], [])
        # self.rt_graph_setup(self.line.setData([],[]))

        # ack completion at terminal
        print("[I]: Application UI has been refreshed!")


    def exit_app(self):

        # acknowledge exit start at terminal
        print ("[I]: exiting app now...")

        # refresh for cleaner exit
        MainWindow.refresh_app(self)

        # # stop loops and threads in RT_rssi_util
        # if self.loop and self.loop.is_running():
        #     self.loop.call_soon_threadsafe(self.loop.stop)

        # quit application's (closes mainwindow)
        QApplication.quit()

        print ("[I]: App exit--- \nThank you for trying me out \nSee you next time ;)")

# ===========================Functions==================================================================================
#
    # def button_clicked(self):
    #     print ("clicked!")
    #     # prints clicked! on the console
    #
    #
    # def button_toggled(self, checked):
    #     self.button_checked = checked
    #     print (self.button_checked)


# sets up and prepares application
# handles control flow, main settings
# creates and manages event loop, arguments
# no gui will be created without this line
# RSSI_GUI = QApplication(sys.argv)

# creating the main window
# window = MainWindow()

# shows the main window - UI
# window.show()

# RSSI_GUI.exec() -> enters the event loop
# continuously listens to user interactions
# keeps the application alive and running
# wc: creates window and exits immediately
# RSSI_GUI.exec()

# separate main.py file -> handling main components.
# if __name__ == "__main__":
#     RSSI_GUI = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     RSSI_GUI.exec()