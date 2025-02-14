# ============================RT_rssi_util=====================================================
# This script is used to scan for a BLE device by its MAC address in real-time using the Bleak library.
# for real time graph -> isolating the async function here and using a separate thread to run the event loop.
# with threads method, the event loop is running in a separate thread, and the main thread is used to interact with the GUI.

import asyncio
import threading
from PyQt6.QtCore import QObject, pyqtSignal
from bleak import BleakScanner


class RtBLEScanning(QObject):
    """
    Real-time BLE Scanning class to scan for BLE devices 
    and update the GUI with the scanned data.
    """

    plot_list_signal = pyqtSignal(list)
    param_signal = pyqtSignal(list)

    def __init__(self):
        """
        Initialize the real-time BLE scanning class.
        """
        super().__init__()

        # Create a thread for running the asyncio event loop
        self.loop = None

        # Use flag to terminate process for safer and smoother loop exit
        self._running = False

        self.loop_thread = threading.Thread(target=self._start_event_loop, daemon=True)
        self.loop_thread.start()

        # Wait for the event loop's initialization
        while self.loop is None:
            pass

    def _start_event_loop(self):
        """
        Start the asyncio event loop in a separate thread.
        """
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        print("[I]: Event loop started in a separate thread.")
        self.loop.run_forever()

    def start_scanning(self, values):
        """
        Start scanning for BLE devices.

        Args:
            values (list): A list containing the necessary 
            values for scanning.
        """
        if not self.loop or not self.loop.is_running():
            print("[E]: Event loop is not running! Try again...")
            return

        if self._running:
            return

        self._running = True
        print("[I]: Executing coroutine: scan_dev_by_mac now...")
        future = asyncio.run_coroutine_threadsafe(self.scan_dev_by_mac(values), self.loop)
        future.add_done_callback(self.scan_complete)

    def scan_complete(self, future):
        """
        Callback function to handle the completion 
        of the scanning coroutine.

        Args:
            future (asyncio.Future): 
            The future object representing the coroutine.
        """
        try:
            result = future.result()
            print("[I]: Scan completed:", result)
        except Exception as e:
            print("[E]: Scan failed. Reason:", e)

    def scan_stop(self):
        """
        Stop scanning for BLE devices.
        """
        print("[I]: Entering scan_stop...")
        self._running = False
        print("[I]: Stopped scanning successfully!")

    async def scan_dev_by_mac(self, values):
        """
        Coroutine to scan for a BLE device by its MAC address.

        Args:
            values (list): A list containing the necessary 
            values for scanning.
        """
        print("[I]: Scanning for the specified device...")

        if len(values) < 4:
            print("[E]: Received partial/no data")
            self._running = False
            return

        minute = values[0]
        sec = values[1]
        mac_id = values[3]
        duration = (minute * 60) + sec  # Convert to seconds

        scan_attempt = 0
        avg_rssi = 0.0
        packet_drop = 100.0
        rssi_list = []
        time_stamps = []
        start_time = asyncio.get_event_loop().time()

        print(f"[I]: Scan duration: {duration} seconds for device {mac_id}")

        while self._running:
            loop_time = asyncio.get_event_loop().time() - start_time
            if loop_time > duration:
                break  # Stop scanning after duration is reached

            print(f"[I]: Scanning... Elapsed time: {loop_time:.2f}s")
            scan_attempt += 1

            # Try to find the device by MAC address
            # Setting this to "passive" will result in a less frequent 
            # scanning pattern, effectively increasing the scanning interval.
            # Warning: check bleak library for scanning mode compatibility.
            # Passive mode not supported by MAC OS

            device = await BleakScanner.find_device_by_address(mac_id, timeout=1.0, scanning_mode="active")

            if device is not None:
                rssi = device.rssi
                if rssi is not None:
                    rssi_list.append(rssi)
                    time_stamps.append(loop_time)
                    print(f"[I]: Device found at {loop_time:.2f}s, RSSI: {rssi}")
            else:
                print("[E]: Device not found in this scan cycle.")

            await asyncio.sleep(0.1)

        # Average RSSI value
        scan_success = len(rssi_list)
        if scan_success > 0:
            avg_rssi = sum(rssi_list) / scan_success

        # Packet drop %
        if scan_attempt > 0:
            packet_drop = (1 - (scan_success / scan_attempt)) * 100

        print(f"[I]: Scan complete. Time stamps: {time_stamps}")
        print(f"[I]: RSSI values: {rssi_list}")
        self.plot_list_signal.emit([time_stamps, rssi_list, avg_rssi, packet_drop])
        self._running = False


if __name__ == "__main__":
    values = []
    scanner = RtBLEScanning()
    scanner.start_scanning(values)

# Future improvement sources -> corresponds to future updates:
# https://stackoverflow.com/questions/37307301/ble-scan-interval-windows-10
# https://github.com/hbldh/bleak/discussions/831
# https://github.com/hbldh/bleak/issues/394