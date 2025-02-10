# Copyright (c) Mehmet Bektas <mbektasgh@outlook.com>

from typing import Union
from notebook_intelligence import Tool, ChatRequest, ChatResponse, ToolPreInvokeResponse, MarkdownData
import nbformat as nbf
import datetime as dt

class MapNotebookCreatorTool(Tool):
    @property
    def name(self) -> str:
        return "map_notebook_creator"

    @property
    def title(self) -> str:
        return "Create notebook centered at geo-coordinates"
    
    @property
    def tags(self) -> list[str]:
        return ["ai-agent-example-tool"]

    @property
    def description(self) -> str:
        return "This is a tool that creates a notebook centered at geo-coordinates"
    
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
            message=f"Creating a map notebook for latitude: {latitude} and longitude: {longitude}"
        )

    async def handle_tool_call(self, request: ChatRequest, response: ChatResponse, tool_context: dict, tool_args: dict) -> dict:
        geo_coordinates = tool_args.get('geo_coordinates')
        latitude = geo_coordinates.get('latitude')
        longitude = geo_coordinates.get('longitude')

        now = dt.datetime.now()
        map_file_name = f"map_{now.strftime('%Y%m%d_%H%M%S')}.ipynb"

        nb = nbf.v4.new_notebook()
        header = """\
### This map notebook was created by an AI Agent using [Notebook Intelligence](https://github.com/notebook-intelligence)
"""

        install_code_cell = "%%capture\n%pip install folium"

        map_code_cell = f"""\
import folium

map = folium.Map(location=[{latitude}, {longitude}], zoom_start=13)
map"""

        nb['cells'] = [
            nbf.v4.new_markdown_cell(header),
            nbf.v4.new_code_cell(install_code_cell),
            nbf.v4.new_code_cell(map_code_cell)
        ]
        nb.metadata["kernelspec"] = { "name": "python3"}
        nbf.write(nb, map_file_name)

        await response.run_ui_command("docmanager:open", {"path": map_file_name})

        return {"result": "I created and opened the map notebook"}
