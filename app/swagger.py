from flask_swagger_ui import get_swaggerui_blueprint

def init_swagger(app):
    """Initialize Swagger UI for the Flask app"""
    
    # Swagger UI configuration
    SWAGGER_URL = '/api/docs'
    API_URL = '/api/swagger.json'
    
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "House Temperature Tracker API"
        }
    )
    
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

def get_swagger_spec():
    """Return the OpenAPI specification for the API"""
    return {
        "openapi": "3.0.0",
        "info": {
            "title": "House Temperature Tracker API",
            "description": "API for tracking house temperature and Nest device data",
            "version": "1.0.0"
        },
        "servers": [
            {
                "url": "http://localhost:5001",
                "description": "Development server"
            }
        ],
        "paths": {
            "/api/nest/devices": {
                "get": {
                    "summary": "Get all Nest devices",
                    "description": "Retrieve all Nest devices from the Google Smart Device Management API",
                    "responses": {
                        "200": {
                            "description": "List of Nest devices",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "devices": {
                                                "type": "array",
                                                "items": {
                                                    "$ref": "#/components/schemas/NestDevice"
                                                }
                                            },
                                            "count": {
                                                "type": "integer",
                                                "description": "Number of devices"
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "500": {
                            "description": "Failed to retrieve devices",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/Error"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/api/nest/device/{device_id}": {
                "get": {
                    "summary": "Get specific Nest device data",
                    "description": "Retrieve detailed data for a specific Nest device",
                    "parameters": [
                        {
                            "name": "device_id",
                            "in": "path",
                            "required": True,
                            "description": "The full device ID from the Nest API",
                            "schema": {
                                "type": "string"
                            }
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Device data",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/NestDeviceData"
                                    }
                                }
                            }
                        },
                        "500": {
                            "description": "Failed to retrieve device data",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/Error"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/api/temperatures": {
                "get": {
                    "summary": "Get temperature readings",
                    "description": "Retrieve temperature readings from the database",
                    "parameters": [
                        {
                            "name": "hours",
                            "in": "query",
                            "required": False,
                            "description": "Number of hours to look back (default: 24)",
                            "schema": {
                                "type": "integer",
                                "default": 24
                            }
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "List of temperature readings",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "$ref": "#/components/schemas/TemperatureReading"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/api/current": {
                "get": {
                    "summary": "Get current temperature",
                    "description": "Get the most recent temperature reading",
                    "responses": {
                        "200": {
                            "description": "Current temperature reading",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/TemperatureReading"
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "No data available"
                        }
                    }
                }
            },
            "/api/statistics": {
                "get": {
                    "summary": "Get temperature statistics",
                    "description": "Get statistical analysis of temperature data",
                    "parameters": [
                        {
                            "name": "hours",
                            "in": "query",
                            "required": False,
                            "description": "Period for statistics (default: 24)",
                            "schema": {
                                "type": "integer",
                                "default": 24
                            }
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Temperature statistics",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/TemperatureStatistics"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "components": {
            "schemas": {
                "NestDevice": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Device identifier"
                        },
                        "type": {
                            "type": "string",
                            "description": "Device type"
                        },
                        "assignee": {
                            "type": "string",
                            "description": "Room assignment"
                        },
                        "traits": {
                            "type": "object",
                            "description": "Device traits and capabilities"
                        }
                    }
                },
                "NestDeviceData": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Device identifier"
                        },
                        "type": {
                            "type": "string",
                            "description": "Device type"
                        },
                        "traits": {
                            "type": "object",
                            "properties": {
                                "sdm.devices.traits.Temperature": {
                                    "type": "object",
                                    "properties": {
                                        "ambientTemperatureCelsius": {
                                            "type": "number",
                                            "description": "Current temperature in Celsius"
                                        }
                                    }
                                },
                                "sdm.devices.traits.Humidity": {
                                    "type": "object",
                                    "properties": {
                                        "ambientHumidityPercent": {
                                            "type": "number",
                                            "description": "Current humidity percentage"
                                        }
                                    }
                                },
                                "sdm.devices.traits.ThermostatHvac": {
                                    "type": "object",
                                    "properties": {
                                        "status": {
                                            "type": "string",
                                            "description": "HVAC status (OFF, HEATING, COOLING)"
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "TemperatureReading": {
                    "type": "object",
                    "properties": {
                        "id": {
                            "type": "integer",
                            "description": "Reading ID"
                        },
                        "device_name": {
                            "type": "string",
                            "description": "Device name"
                        },
                        "temperature_c": {
                            "type": "number",
                            "description": "Temperature in Celsius"
                        },
                        "temperature_f": {
                            "type": "number",
                            "description": "Temperature in Fahrenheit"
                        },
                        "humidity": {
                            "type": "number",
                            "description": "Humidity percentage"
                        },
                        "target_temperature_c": {
                            "type": "number",
                            "description": "Target temperature in Celsius"
                        },
                        "target_temperature_f": {
                            "type": "number",
                            "description": "Target temperature in Fahrenheit"
                        },
                        "hvac_mode": {
                            "type": "string",
                            "description": "HVAC mode"
                        },
                        "hvac_state": {
                            "type": "string",
                            "description": "HVAC state"
                        },
                        "outside_temperature_c": {
                            "type": "number",
                            "description": "Outside temperature in Celsius"
                        },
                        "outside_temperature_f": {
                            "type": "number",
                            "description": "Outside temperature in Fahrenheit"
                        },
                        "timestamp": {
                            "type": "string",
                            "format": "date-time",
                            "description": "Reading timestamp"
                        }
                    }
                },
                "Error": {
                    "type": "object",
                    "properties": {
                        "error": {
                            "type": "string",
                            "description": "Error message"
                        }
                    }
                },
                "TemperatureStatistics": {
                    "type": "object",
                    "properties": {
                        "avg_temperature": {
                            "type": "number",
                            "description": "Average temperature in Celsius"
                        },
                        "min_temperature": {
                            "type": "number",
                            "description": "Minimum temperature in Celsius"
                        },
                        "max_temperature": {
                            "type": "number",
                            "description": "Maximum temperature in Celsius"
                        },
                        "avg_humidity": {
                            "type": "number",
                            "description": "Average humidity percentage"
                        },
                        "avg_outside_temperature": {
                            "type": "number",
                            "description": "Average outside temperature in Celsius"
                        },
                        "min_outside_temperature": {
                            "type": "number",
                            "description": "Minimum outside temperature in Celsius"
                        },
                        "max_outside_temperature": {
                            "type": "number",
                            "description": "Maximum outside temperature in Celsius"
                        },
                        "period_hours": {
                            "type": "integer",
                            "description": "Period in hours for the statistics"
                        }
                    }
                }
            }
        }
    }