from bleak import BleakScanner
import asyncio

# Scan for devices with a scan interval of 100 milliseconds
async def main():
    devices = await BleakScanner.discover(scan_interval=100)
    print (devices)

asyncio.run(main())