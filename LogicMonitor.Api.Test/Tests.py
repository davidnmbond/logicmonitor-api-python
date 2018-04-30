import unittest
import json
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
	def test_getDevice_passes(self):
		device = self._client.get('/device/devices/{0}'.format(self._config['exampleDeviceId']))
		self.assertEqual(66, device['id'])

"""
Main
"""
if __name__ == '__main__':
	unittest.main()
