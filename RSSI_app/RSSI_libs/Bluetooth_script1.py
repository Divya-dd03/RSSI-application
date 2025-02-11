# ====================Read RSSI of devices continuously===============================

# from asyncio import create_task

import asyncio
from bleak import BleakScanner
from PyQt6.QtCore import QThread, pyqtSignal


# ======================= BLE Scanning Thread ===============================
class BleTable(QThread):

    # Signal triggered to update GUI with scanned devices
    devices_found = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self._running = False


    # scanning for BLE devices for 20s
    async def devices_in_vicinity(self) -> list:
        print ("[I]: Entering devices_in_vicinity...wait for 20s for next iteration...")
        device = await BleakScanner.discover(timeout = 20.0, return_adv = True)

        # Convert scanned devices into a list of tuples
        dev_list = [
            (d.address, adv_data.rssi, d.name, adv_data.manufacturer_data)
            for address, (d, adv_data) in device.items()
        ]
        return dev_list


    # running event_loop to continuously scan for devices
    def run(self):
        print ("[E]: Entering run...")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        while self._running:
            dev_list = loop.run_until_complete(self.devices_in_vicinity())

            # To avoid warning at emit () -> do the following...
            # copied classes connect and emit from pyqtSignal to pyqtBoundSignal
            self.devices_found.emit(dev_list)  # Send devices to UI

        print ("[I]: Found devices successfully!")


    # Start scanning -> triggered by scan_start pushbutton
    def scan_start(self):
        print ("[I]: Entering scan_start...")
        if not self.isRunning():
            self._running = True
            self.start()
            print("[I]: Started scanning successfully!")


    # Stop scanning -> triggered by scan_stop pushbutton
    def scan_stop(self):
        print ("[I]: Entering scan_stop...")
        self._running = False
        self.quit()
        self.wait()
        # self.terminate() -> unsafe but why?
        print ("[I]: Stopped scanning successfully!")


# Standalone execution (for testing)
async def main():

    print ("[I]: Entering main loop...")
    scanning = BleTable()
    await scanning.devices_in_vicinity()
    print("[I]: Exiting Lib... BYE BYE")

# entry point
if __name__ == "__main__":
    asyncio.run(main())
    print (__name__)
#
# # SECOND: Search for the target device
# # OUT: return device MAC_ID
# async def device_of_interest():
#     Target_device = input ("Enter the target device: ")
#     await BleakScanner.find_device_by_address(Target_device, 15.0, )
#
#
# # Create tasks for individual function
# async def nested():
#     task1 = asyncio.create_task(devices_in_vicinity())
#     # task2 = asyncio.create_task(device_of_interest())
#     await task1
#
#
# # main loop - entry point
# async def main():
#     # print ("Entering main loop........")
#     print ("Scanning for nearby devices........")
#     # await devices_in_vicinity()
#     await nested()
# asyncio.run(main())
#
#
#
#
#
#
# async def monitor_rssi(scan_interval=5):
#     try:
#         while True:
#             print("Scanning for devices...")
#             devices = await BleakScanner.discover()
#
#             for d in devices:
#                 print(f"Dev: {d.name}, Addr: {d.address}, RSSI: {d.rssi} dBm")
#
#             print("Waiting before next scan...\n")
#             await asyncio.sleep(scan_interval)  # Wait before scanning again
#
#     except asyncio.CancelledError:
#         print("RSSI monitoring stopped.")
#
#
# # Run the RSSI monitoring loop
# async def main():
#     try:
#         await monitor_rssi(scan_interval=2)  # Set scan interval to 2 seconds
#     except KeyboardInterrupt:
#         print("\nProgram interrupted.")
#
#
# if __name__ == "__main__":
#     asyncio.run(main())