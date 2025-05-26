from dotenv import load_dotenv
from typing import Annotated
from typing_extensions import TypedDict
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from prompts import structured_system_prompt, job_summary_system_prompt, job_interview_system_prompt # User-defined prompts

# Load in env variables for the OpenAI LLM
load_dotenv()

# Initialize the large language model (LLM) and set the model type
llm = init_chat_model(
    model = "openai:o4-mini"
)

# Define the expected structured output format for the given job information
class JobFormat(BaseModel):
    job_title: str = Field(..., description="The title of the position given.")
    job_description: str = Field(..., description="A description of the position given.")
    job_requirements: str = Field(..., description="A list of requirements for the position given.")

# Define the shared state that moves throughout the LangGraph workflow
class State(TypedDict):
    messages: Annotated[list, add_messages]     # Chat history (all outputs stored here)
    job_breakdown: JobFormat | None             # Structured output from the given initial information
    job_summary: str | None                     # A summary of the given job breakdown
    interview_questions: list[str] | None       # A generated list of both behavioral and technical interview questions for the given job


# Node 1: Parse the initial given user information into structured fields using the JobFormat model
def process_input(state: State):
    last_message = state["messages"][-1]

    structured_llm = llm.with_structured_output(JobFormat)
    response = structured_llm.invoke([
        SystemMessage(content = structured_system_prompt),
        HumanMessage(content = last_message.content)
    ])

    return {
        "messages": state["messages"] + [AIMessage(content=str(response))],
        "job_breakdown": response
    }

# Node 2: Generate a summary based on the given job breakdown
def generate_job_summary(state: State):
    job_info = state["job_breakdown"]

    response = llm.invoke([
        SystemMessage(content = job_summary_system_prompt),
        HumanMessage(content = str(job_info)),
    ])

    return {
        "messages": state["messages"] + [AIMessage(content=response.content)],
        "job_summary": response.content
    }

# Node 3: Generate a list of interview questions from the given job summary
def generate_interview_questions(state: State):
    job_summary = state["job_summary"]

    response = llm.invoke([
        SystemMessage(content = job_interview_system_prompt),
        HumanMessage(content = job_summary),
        HumanMessage(content = "")
    ])

    questions = response.content.split("\n")

    return {
        "messages": state["messages"] + [AIMessage(content=response.content)],
        "interview_questions": questions
    }


# Define the graph structure using LangGraph
graph_builder = StateGraph(State) # Let LangGraph know what the state is that will be passed around and what fields there are

# Register each of the nodes in the graph
graph_builder.add_node("process_input", process_input)
graph_builder.add_node("generate_job_summary", generate_job_summary)
graph_builder.add_node("generate_interview_questions", generate_interview_questions)

# Define graph edges for node-to-node flow
graph_builder.add_edge(START, "process_input")
graph_builder.add_edge("process_input", "generate_job_summary")
graph_builder.add_edge("generate_job_summary", "generate_interview_questions")
graph_builder.add_edge("generate_interview_questions", END)

# Compile the graph
graph = graph_builder.compile()


# Test function to show how the Agent workflow works
def main() -> None:
    # Define the initial empty state
    state = {
        "messages": [],
        "job_breakdown": None,
        "job_summary": None,
    }

    # Use our LLM to generate test data
    test_data = llm.invoke([
        SystemMessage(content = "You are a helpful assistant that helps people find a job they can apply to."),
        HumanMessage(content = "This is a test prompt for our chat application. The job that you will be helping with is an AI Data Analytics Engineer."
                               "You job is to return a job title, job description, and job requirements. Only return this information, do not include any irrelevant information or fluff.")
    ])

    # Add the test data to the state so that it can flow through the workflow
    state["messages"].append(HumanMessage(content = test_data.content))

    # Invoke the agent
    state = graph.invoke(state)

    # Print out all the generated questions from the final step of the workflow
    if state.get("interview_questions"):
        for question in state["interview_questions"]:
            print(question)

    # View all the intermediate steps here
    # for message in state["messages"]:
        # print(message)

main()