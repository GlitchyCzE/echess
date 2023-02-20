import asyncio
import os
from ble_serial.bluetooth.ble_interface import BLE_interface

MAC = os.getenv('BOARD_MAC')
ADAPTER = None
SERVICE_UUID = None
WRITE_UUID = None
READ_UUID = None

def receiver_callback(value: bytes):
	print("Recieved:", value)


async def main_loop(ble: BLE_interface):
	while True:
		await asyncio.sleep(3.0)
		print("Ping!")


async def init():
	ble = BLE_interface(ADAPTER, SERVICE_UUID)
	ble.set_receiver(receiver_callback)

	try:
		await ble.connect(MAC, "public", 10.0)
		await ble.setup_chars(WRITE_UUID, READ_UUID, "rw")
		await asyncio.gather(ble.send_loop(), main_loop(ble))
	finally:
		await ble.disconnect()
