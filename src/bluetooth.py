import asyncio
import os
from ble_serial.bluetooth.ble_interface import BLE_interface

MAC = os.getenv('BOARD_MAC')
ADAPTER = None
SERVICE_UUID = None
WRITE_UUID = None
READ_UUID = None

ble = None
registered_callbacks = []

async def send_command(cmd):
	ble.queue_command(cmd)


def register_callback(callback, once = False):
	registered_callbacks.push({"callback": callback, "once": once})


def receiver_callback(value: bytes):
	print("Recieved:", value)
	for obj in registered_callbacks:
		obj.callback(value)
	registered_callbacks = [c for c in registered_callbacks if not c.once]


async def init():
	ble = BLE_interface(ADAPTER, SERVICE_UUID)
	ble.set_receiver(receiver_callback)

	try:
		await ble.connect(MAC, "public", 10.0)
		await ble.setup_chars(WRITE_UUID, READ_UUID, "rw")
		await asyncio.gather(ble.send_loop())
	finally:
		await ble.disconnect()
