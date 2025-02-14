# =======================Bluetooth_script1====================
# This script is used to scan for BLE devices in the vicinity 
# and continuously update the GUI with the scanned devices.

import asyncio
from bleak import BleakScanner
from PyQt6.QtCore import QThread, pyqtSignal


class BleTable(QThread):
    """
    BLE Scanning Thread to continuously scan for BLE devices 
    and update the GUI with the scanned devices.
    """

    # Signal triggered to update GUI with scanned devices
    devices_found = pyqtSignal(list)

    def __init__(self):
        """
        Initialize the BLE scanning thread.
        """
        super().__init__()
        self._running = False

    async def devices_in_vicinity(self) -> list:
        """
        Scan for BLE devices for 20 seconds 
        and return a list of discovered devices.

        Returns:
            list: A list of tuples containing device 
            address, RSSI, name, and manufacturer data.
        """
        print("[I]: Entered devices_in_vicinity")
        print("     |__wait for 20s for next iteration...")
        device = await BleakScanner.discover(timeout=10.0, return_adv=True)

        # Convert scanned devices into a list of tuples
        dev_list = [
            (d.address, adv_data.rssi, d.name, adv_data.manufacturer_data)
            for address, (d, adv_data) in device.items()
        ]
        return dev_list

    def run(self):
        """
        Run the event loop to continuously scan for devices 
        and emit the scanned devices to the GUI.
        """
        print("[E]: Entering run...")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        while self._running:
            dev_list = loop.run_until_complete(self.devices_in_vicinity())
            self.devices_found.emit(dev_list)  # Send devices to UI
        print("[I]: Found devices successfully!")

    def scan_start(self):
        """
        Start scanning for BLE devices. 
        Triggered by the scan_start pushbutton.
        """
        print("[I]: Entering scan_start...")
        if not self.isRunning():
            self._running = True
            self.start()
            print("[I]: Started scanning successfully!")

    def scan_stop(self):
        """
        Stop scanning for BLE devices. 
        Triggered by the scan_stop pushbutton.
        """
        print("[I]: Entering scan_stop...")
        self._running = False
        self.quit()
        self.wait()
        print("[I]: Stopped scanning successfully!")


async def main():
    """
    Main function for standalone execution (for testing).
    """
    print("[I]: Entering main loop...")
    scanning = BleTable()
    await scanning.devices_in_vicinity()
    print("[I]: Exiting Lib... BYE BYE")


# Entry point
if __name__ == "__main__":
    asyncio.run(main())
    print(__name__)