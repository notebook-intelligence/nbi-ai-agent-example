# Copyright (c) Mehmet Bektas <mbektasgh@outlook.com>

import logging
from notebook_intelligence import ChatCommand, MarkdownData, NotebookIntelligenceExtension, Host, ChatParticipant, ChatRequest, ChatResponse, Tool

from .util import PARTICIPANT_ICON_URL

from .geocoordinate_lookup_tool import GeoCoordinateLookupTool
from .map_response_generator_tool import MapResponseGeneratorTool
from .map_notebook_creator_tool import MapNotebookCreatorTool
from .notebook_share_tool import NotebookShareTool

log = logging.getLogger(__name__)

class AIAgentChatParticipant(ChatParticipant):
    def __init__(self, host: Host):
        super().__init__()
        self.host = host

    @property
    def id(self) -> str:
        return "ai-agent"

    @property
    def name(self) -> str:
        return "AI Agent Example"
    
    @property
    def description(self) -> str:
        return "An example participant"

    @property
    def icon_path(self) -> str:
        return PARTICIPANT_ICON_URL

    @property
    def commands(self) -> list[ChatCommand]:
        return [
            ChatCommand(name='help', description='Show help'),
        ]
    
    @property
    def tools(self) -> list[Tool]:
        return [GeoCoordinateLookupTool(), MapResponseGeneratorTool(), MapNotebookCreatorTool(), NotebookShareTool()]

    async def handle_chat_request(self, request: ChatRequest, response: ChatResponse, options: dict = {}) -> None:
        if request.command == 'help':
            response.stream(MarkdownData("""I am an AI agent. I can help you with some tasks. Here are some example prompts you can try:\n
            \n```text\n@ai-agent Get geo-coordinates for "Eiffel Tower, Paris"\n```\n
            \n```text\n@ai-agent Show a map centered at "Golden Gate Bridge, San Francisco"\n```\n
            \n```text\n@ai-agent Create a notebook with a map centered at "Istanbul, Turkiye"\n```\n
            \n```text\n@ai-agent Share this notebook publicly\n```\n
            """))
            response.finish()
            return

        await self.handle_chat_request_with_tools(request, response, options)

class AIAgentExtension(NotebookIntelligenceExtension):
    @property
    def id(self) -> str:
        return "ai-agent-example-extension"

    @property
    def name(self) -> str:
        return "AI Agent Example Extension"

    @property
    def provider(self) -> str:
        return "Mehmet Bektas"

    @property
    def url(self) -> str:
        return "https://github.com/mbektas"

    def activate(self, host: Host) -> None:
        self.participant = AIAgentChatParticipant(host)
        host.register_chat_participant(self.participant)
        log.info("AI Agent example extension activated")
