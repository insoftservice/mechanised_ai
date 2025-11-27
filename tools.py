from langchain_core.tools import StructuredTool

from langgraph.prebuilt import ToolNode
from agents import *
from models import *
from flow import *

def run_queries(search_queries: list[str], **kwargs):
    """Run the generated queries individually and aggregate results."""
    results = []
    for query in search_queries:
        response = llm.invoke(f"Search: {query}")
        results.append(f"Query: {query}\nResult: {response.content}")
    return "\n---\n".join(results) 


tool_node = ToolNode(
    [
        StructuredTool.from_function(run_queries, name=AnswerQuestion.__name__),
        StructuredTool.from_function(run_queries, name=ReviseAnswer.__name__),
    ]
)