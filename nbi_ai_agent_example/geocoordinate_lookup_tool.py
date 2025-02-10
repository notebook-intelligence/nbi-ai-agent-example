# Copyright (c) Mehmet Bektas <mbektasgh@outlook.com>

from typing import Union
from notebook_intelligence import Tool, ChatRequest, ChatResponse, ToolPreInvokeResponse
from geopy.geocoders import Nominatim

GEOLOCATOR_APP_NAME = "NBI_AI_AGENT_EXAMPLE"
geolocator = Nominatim(user_agent=GEOLOCATOR_APP_NAME)

class GeoCoordinateLookupTool(Tool):
    @property
    def name(self) -> str:
        return "geo_coordinate_lookup"

    @property
    def title(self) -> str:
        return "Get geo-coordinates from an address"
    
    @property
    def tags(self) -> list[str]:
        return ["ai-agent-example-tool"]
    
    @property
    def description(self) -> str:
        return "This is a tool that converts an address to a geo-coordinates"
    
    @property
    def schema(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "address": {
                            "type": "string",
                            "description": "Address to convert to geo-coordinates",
                        }
                    },
                    "required": ["address"],
                    "additionalProperties": False,
                },
            },
        }

    def pre_invoke(self, request: ChatRequest, tool_args: dict) -> Union[ToolPreInvokeResponse, None]:
        address = tool_args.get('address')
        return ToolPreInvokeResponse(
            message=f"Getting coordinates for '{address}'"
        )

    async def handle_tool_call(self, request: ChatRequest, response: ChatResponse, tool_context: dict, tool_args: dict) -> dict:
        address = tool_args.get('address')
        location = geolocator.geocode(address)
        return {"latitude": location.latitude, "longitude": location.longitude}
