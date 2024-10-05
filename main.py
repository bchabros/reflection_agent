import streamlit as st
from dotenv import load_dotenv
from src.graph_function import build_reflection_agent


def main():
    load_dotenv()

    builder = build_reflection_agent()
    graph = builder.compile()

    # graph.get_graph().print_ascii()

    # Streamlit app title
    st.title("Reflection Agent Twitter helper")

    # User input text field
    user_input = st.text_input(
        "Enter your Twitter:",
        value="""Make this tweet better:"
                                    @LangChainAI
            — newly Tool Calling feature is seriously underrated.

            After a long wait, it's  here- making the implementation of agents across different models with function calling - super easy.

            Made a video covering their newest blog post
                                  """,
    )

    if st.button("Submit"):
        with st.spinner("Processing..."):
            try:
                # Invoke the graph with user input
                res = graph.invoke(user_input)
                answer = res[-1].content
                st.write(answer)
            except Exception as e:
                st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
