# Copyright (c) Mehmet Bektas <mbektasgh@outlook.com>

from os import path
from typing import Union
from notebook_intelligence import Tool, ChatRequest, ChatResponse, ToolPreInvokeResponse, AnchorData
import nbss_upload

class NotebookShareTool(Tool):
    @property
    def name(self) -> str:
        return "share_notebook"

    @property
    def title(self) -> str:
        return "Share notebook publicly"
    
    @property
    def tags(self) -> list[str]:
        return ["ai-agent-example-tool"]
    
    @property
    def description(self) -> str:
        return "This is a tool that shares a notebook publicly and creates a link"
    
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
                        "notebook_file_path": {
                            "type": "string",
                            "description": "File path of the notebook to share",
                        }
                    },
                    "required": ["notebook_file_path"],
                    "additionalProperties": False,
                },
            },
        }

    def pre_invoke(self, request: ChatRequest, tool_args: dict) -> Union[ToolPreInvokeResponse, None]:
        file_path = tool_args.get('notebook_file_path')
        file_name = path.basename(file_path)
        return ToolPreInvokeResponse(
            message=f"Sharing notebook '{file_name}'",
            confirmationTitle="Confirm sharing",
            confirmationMessage=f"Are you sure you want to share the notebook at '{file_path}'? This will upload the notebook to public internet and cannot be undone."
        )

    async def handle_tool_call(self, request: ChatRequest, response: ChatResponse, tool_context: dict, tool_args: dict) -> dict:
        file_path = tool_args.get('notebook_file_path')
        file_name = path.basename(file_path)
        share_url = nbss_upload.upload_notebook(file_path, False, False, 'https://notebooksharing.space')
        response.stream(AnchorData(share_url, f"Click here to view the shared notebook '{file_name}'"))

        return {"result": f"Notebook '{file_name}' has been shared at: {share_url}"}
