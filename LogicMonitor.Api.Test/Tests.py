import unittest
import json
import time
from logicmonitor.LogicMonitorClient import LogicMonitorClient


"""
Unit test class
"""
class Tests(unittest.TestCase):

	"""
	Set up
	"""
	def setUp(self):
		with open('appsettings.json') as file:
			self._config = json.load(file)
			file.close()
		self._client = LogicMonitorClient(self._config['account'], self._config['accessId'], self._config['accessKey'])
		pass

	"""
	Get a device
	"""
	def test_01_getDevice_passes(self):
		device = self._client.get('/device/devices/{0}'.format(self._config['exampleDeviceId']))
		self.assertEqual(self._config['exampleDeviceId'], device['id'])

	"""
	Update a specific field of a device (HTTP PATCH)
	"""
	def test_02_updateDeviceField_passes(self):
		updated_description = 'some new description for this device'
		device_data = json.dumps({
			'description': updated_description
		})
		device = self._client.patch(
			'/device/devices/{}'.format(self._config['exampleDeviceId']), 
			queryParams='?patchFields=description',
			data=device_data)
		self.assertEqual(device['id'], self._config['exampleDeviceId'])
		self.assertEqual(updated_description, device['description'])

	"""
	Create a device SDT
	"""
	def test_03_createDeviceSdt_passes(self):
		sdt_start_time = int(time.time() * 1000)
		sdt_end_time = sdt_start_time + int(30 * 60 * 1000)  # 30 minute SDT
		sdt_comment = 'Test SDT Started At Time ' + str(sdt_start_time)
		device_sdt_data = json.dumps({    
			'sdtType': 1,
			'type': 'DeviceSDT',
			'deviceId': self._config['exampleDeviceId'],
			'startDateTime': sdt_start_time,
			'endDateTime': sdt_end_time,
			'comment': sdt_comment
		})
		sdt = self._client.post('/sdt/sdts', queryParams='', data=device_sdt_data)
		self.assertEqual(sdt['deviceId'], self._config['exampleDeviceId'])
		self.assertEqual(sdt['comment'], sdt_comment)
		self.assertEqual(sdt['startDateTime'], sdt_start_time)
		self.assertEqual(sdt['endDateTime'], sdt_end_time)
		Tests._sdt_id = sdt['id'] # Store SDT id so we can refer to it later

	"""
	Get a device SDT
	"""
	def test_04_getDeviceSdt_passes(self):
		sdt = self._client.get('/sdt/sdts/{}'.format(self._sdt_id))
		self.assertEqual(Tests._sdt_id, sdt['id'])

	"""
	Update a device SDT
	"""
	def test_05_updateDeviceSdt_passes(self):
		sdt_start_time = int(time.time() * 1000) + (60 * 60 * 1000) # Start SDT an hour from now
		sdt_end_time = sdt_start_time + (180 * 60 * 1000) # 3 hour SDT duration
		sdt_comment = 'SDT updated at {}'.format(int(time.time() * 1000))
		device_sdt_data = json.dumps({    
			'sdtType': 1,
			'type': 'DeviceSDT',
			'deviceId': self._config['exampleDeviceId'],
			'startDateTime': sdt_start_time,
			'endDateTime': sdt_end_time,
			'comment': sdt_comment
		})
		sdt = self._client.put('/sdt/sdts/{}'.format(Tests._sdt_id), queryParams='', data=device_sdt_data)
		self.assertEqual(sdt['id'], Tests._sdt_id)
		self.assertEqual(sdt['comment'], sdt_comment)
		self.assertEqual(sdt['startDateTime'], sdt_start_time)
		self.assertEqual(sdt['endDateTime'], sdt_end_time)

	"""
	Delete a device SDT
	"""
	def test_06_deleteDeviceSdt_passes(self):
		deleted_sdt = self._client.delete('/sdt/sdts/{}'.format(Tests._sdt_id))
		self.assertIsNone(deleted_sdt)

"""
Main
"""
if __name__ == '__main__':
	unittest.main()
