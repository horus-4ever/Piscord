import websockets
import json
import asyncio

from .Errors import TokenError,ConnexionError

class Gateway:

	def __init__(self, url, token, auth_op = 10, events_code = 0, heartbeat_code = 1, presence = None):
		self.url = url
		self.token = token
		self.auth_op = auth_op
		self.last_sequence = 0
		self.events_code = events_code
		self.heartbeat_code = heartbeat_code
		self.session_id = None
		self.presence = presence
		self.error = None
		self._running = False

	async def _on_connection_closed(self):
		"""
		When the bot loses the connection, we try to reconnect 5 times.
		If it fails, then we must exit.
		"""
		await self.websocket.close()
		if self.session_id and self.last_sequence:
			await self.websocket.close()
			for reconnect_attemps in range(5):
				websocket, msg = await self._reconnect()
				if msg:
					data = json.loads(msg)
					self.websocket = websocket
					self.interval = data["d"]["heartbeat_interval"]
					break
				else:
					await asyncio.sleep(1)
			else:
				self.error = ConnexionError("You've lost the connection to the server")
				self.heartbeat.cancel()
		else:
			self.heartbeat.cancel()
			self._running = False

	async def connect(self, action = None, shards = [0,1]):
		self._running = True
		self.loop = asyncio.get_event_loop()
		self.websocket = await websockets.connect(self.url, ping_interval = None, max_size=1_000_000_000)

		while self._running:
			if self.error:
				raise self.error
			try:
				msg = await self.websocket.recv()
			except Exception as error_code:
				if error_code.code in (1000, 1001, 1006): # 1006 => connection closed
					await self._on_connection_closed()
					continue
				elif error_code.code == 4004: # 4004 => invalid token
					self.error = TokenError()
				else:
					self.error = ConnexionError(f"Unknow Error - {e.code}")
				self.heartbeat.cancel()
				continue
			
			# if there were no errors, we decode the data
			data = json.loads(msg)
			# print(data)
			sequence = data.get("s")
			if sequence:
				self.last_sequence = sequence
			if data["op"] == self.auth_op:
				self.interval = data["d"]["heartbeat_interval"]
				self.heartbeat = asyncio.create_task(self.__heartbeat(self.websocket))
				payload = {
					"op": 2,
					"d": {
						"token": self.token,
						"properties": {
							"$browser": "piscord",
							"$device": "piscord"
						},
					"large_threshold": 250,
					"presence":self.presence,
				}}
				if shards[1] > 1:
					payload["shard"] = shards

				if action:
					await self.send(action)
				else:
					await self.send(payload)
			if data["op"] == self.events_code:
				if data["t"] == "READY":
					self.session_id = data["d"]["session_id"]
			yield data

	async def _reconnect(self):
		payload = {
			"op": 6,
			"d": {
				"token": self.token,
				"session_id": self.session_id,
				"seq": self.last_sequence
		}}
		websocket = await websockets.connect(self.url, ping_interval = None)
		msg = None
		try:
			await websocket.recv()
			await self.send(payload)
			msg = await websocket.recv()
		except Exception as e:
			await websocket.close()
		return websocket, msg

	async def __heartbeat(self, ws):
		while True:
			await asyncio.sleep(self.interval / 1000)
			if not self.websocket.closed:
				await self.send({"op": self.heartbeat_code,"d": self.last_sequence})

	async def send(self, payload):
		await self.websocket.send(json.dumps(payload))

	async def _stop(self):
		self.session_id = None
		await self.websocket.close()
		self.heartbeat.cancel()

	def stop(self):
		asyncio.run_coroutine_threadsafe(self._stop(), self.loop)