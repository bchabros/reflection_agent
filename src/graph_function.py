from dotenv import load_dotenv
from typing import List, Sequence

from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, MessageGraph

from src.chains import generate_chain, reflect_chain
from src.const import REFLECT, GENERATE

load_dotenv()


def generation_node(state: Sequence[BaseMessage]):
    return generate_chain.invoke({"messages": state})


def reflection_node(messages: Sequence[BaseMessage]) -> List[BaseMessage]:
    res = reflect_chain.invoke({"messages": messages})
    return [HumanMessage(content=res.content)]


def should_continue(state: List[BaseMessage]):
    if len(state) > 6:
        return END
    return REFLECT


def build_reflection_agent():
    builder = MessageGraph()
    builder.add_node(GENERATE, generation_node)
    builder.add_node(REFLECT, reflection_node)
    builder.set_entry_point(GENERATE)

    builder.add_conditional_edges(GENERATE, should_continue)
    builder.add_edge(REFLECT, GENERATE)

    return builder


app = build_reflection_agent()
app = app.compile()
