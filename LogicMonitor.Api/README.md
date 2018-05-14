# logicmonitor - Python package

LogicMonitor API for Python

Simple example for https://acme.logicmonitor.com/:

	client = LogicMonitorClient('acme', 'accessIdABCDEF', 'accessKeyGHIJKLMEOP')
	device = client.get('/device/devices/66')
	print(device['id'])

	# Update the device
	device = client.put('/device/devices/66', 
		queryParams='',
		data='{"name":"10.1.1.1","displayName":"MonitoredSvr01","preferredCollectorId":20,"hostGroupIds":"2","description":"a server we want to monitor"}')
	print(device['displayName'])

	# Update a specific property of the device
	device = client.patch('/device/devices/66',
		queryParams='?patchFields=description',
		data='{"description": "new device description!"}')
	print(device['description'])

	# Delete a device
	client.delete('/device/devices/66')

	# Create a new device
	new_device = client.post('/device/devices',
		queryParams='',
		data = '{"name":"10.0.1.1","displayName":"ProdServer01","preferredCollectorId":171,"hostGroupIds":2,"customProperties":[{"name":"snmp.version","value":"v3"},{"name":"location","value":"Somewhere"}]}')
	print(new_device['id])
