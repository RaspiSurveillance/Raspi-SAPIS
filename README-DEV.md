# Raspi-SurveillanceAPIServer (SAPIS)

## Endpoints

### PUT /start/camerastream

Authorization: Basic Auth
{
	"name": "<name>",
	"password": "<password>",
	"options": {
		"--reswidth": 1280,
		"--resheight": 900,
		"--framerate": 8,
		"--rotation_degrees": 0,
		"--awb": "auto",
		"--filter": "none"
	}
}

### PUT /start/surveillance

Authorization: Basic Auth

### PUT /stop

Authorization: Basic Auth

### PUT /shutdown

Authorization: Basic Auth

### PUT /startup

Authorization: Basic Auth
{
	"id": "<id>"
}

### PUT /shutdown/master

Authorization: Basic Auth
{
	"id": "<id>"
}
