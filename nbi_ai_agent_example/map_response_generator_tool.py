# Copyright (c) Mehmet Bektas <mbektasgh@outlook.com>

from typing import Union
from notebook_intelligence import Tool, ToolPreInvokeResponse, ChatRequest, ChatResponse, HTMLFrameData

class MapResponseGeneratorTool(Tool):
    @property
    def name(self) -> str:
        return "map_response_generator"

    @property
    def title(self) -> str:
        return "Show a map centered at geo-coordinates"
    
    @property
    def tags(self) -> list[str]:
        return ["ai-agent-example-tool"]

    @property
    def description(self) -> str:
        return "This is a tool that shows a map centered at geo-coordinates"
    
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
                        "geo_coordinates": {
                            "type": "object",
                            "description": "Geo-coordinates for an address",
                            "properties": {
                                "latitude": {
                                    "type": "number",
                                    "description": "latitude of geo-coordinates",
                                },
                                "longitude": {
                                    "type": "number",
                                    "description": "longitude of geo-coordinates",
                                }
                            },
                            "required": ["latitude", "longitude"],
                            "additionalProperties": False,
                        }
                    },
                    "required": ["geo_coordinates"],
                    "additionalProperties": False,
                },
            },
        }

    def pre_invoke(self, request: ChatRequest, tool_args: dict) -> Union[ToolPreInvokeResponse, None]:
        geo_coordinates = tool_args.get('geo_coordinates')
        latitude = geo_coordinates.get('latitude')
        longitude = geo_coordinates.get('longitude')
        return ToolPreInvokeResponse(
            message=f"Showing a map centered at latitude: {latitude} and longitude: {longitude}"
        )

    async def handle_tool_call(self, request: ChatRequest, response: ChatResponse, tool_context: dict, tool_args: dict) -> dict:
        geo_coordinates = tool_args.get('geo_coordinates')
        latitude = geo_coordinates.get('latitude')
        longitude = geo_coordinates.get('longitude')

        response.stream(HTMLFrameData(f"""<iframe width="100%" height="100%" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" id="gmap_canvas" src="https://maps.google.com/maps?width=400&amp;height=400&amp;hl=en&amp;q={latitude},{longitude}&amp;t=&amp;z=11&amp;ie=UTF8&amp;iwloc=B&amp;output=embed"></iframe>""", height=400))
        response.finish()

        return {"result": "I showed the map"}
