
from app.tools.calculator import calculate
from app.tools.datetime_tool import get_current_datetime
from app.tools.knowledge import search_knowledge_base

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "name": "calculate",
        "description": "Evaluate a basic arithmetic expression.",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Arithmetic expression"
                }
            },
            "required": ["expression"],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "get_current_datetime",
        "description": "Get current UTC date and time.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "search_knowledge_base",
        "description": "Search AgentFlow project knowledge.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string"}
            },
            "required": ["query"],
            "additionalProperties": False
        },
        "strict": True
    }
]

def execute_tool(name: str, arguments: dict):
    if name == "calculate":
        return {"result": calculate(arguments["expression"])}

    if name == "get_current_datetime":
        return get_current_datetime()

    if name == "search_knowledge_base":
        return search_knowledge_base(arguments["query"])

    raise ValueError(f"Unknown tool: {name}")
