import os
from typing import TypedDict, Annotated
import operator

import psycopg
from langgraph.graph import StateGraph, START, END 
from langgraph.checkpoint.postgres import PostgresSaver
from langchain_core.messages import (
    AnyMessage,  
    HumanMessage,  
    AIMessage,  
    SystemMessage,  
)

from langchain_groq import ChatGroq

from tavily_tool import tavily_search
from flight_tool import Flight_search
from dotenv import load_dotenv

load_dotenv()

databse_url = os.getenv("database_url")
llm = ChatGroq(model='llama-3.3-70b-versatile', api_key=os.getenv("groq_api_key"))

class Travel(TypedDict):
    message: Annotated[list[AnyMessage], operator.add]
    user_query: str
    flight_results: str
    hotel_results: str
    itinerary: str
    llm_calls: int

def flight_agent(state: Travel):
    query = state['user_query']
    flight_results = Flight_search(query)
    
    if not flight_results:
        flight_results = "No flights found via API at this time."

    return {
        'flight_results': flight_results,
        'message': [AIMessage(content=f'Flight results processed for query: {query}')],
        'llm_calls': state.get('llm_calls', 0) + 1
    }
    
def hotel_agent(state: Travel):
    # Optimize query so Tavily looks specifically for hotels
    optimized_hotel_query = f"best hotels accommodation options in {state['user_query']}"
    hotel_results = tavily_search(optimized_hotel_query)
    
    return {
        'hotel_results': hotel_results,
        'message': [AIMessage(content=f'Hotel results fetched for query: {optimized_hotel_query}')],
        'llm_calls': state.get('llm_calls', 0) + 1
    }

def itinerary_agent(state: Travel):
    # Explicitly instruct the model to use the data provided in the string context
    prompt = f'''Create a comprehensive travel itinerary.
User Query: {state['user_query']}

Available Flight Info:
{state['flight_results']}

Available Hotel Info:
{state['hotel_results']}

CRITICAL INSTRUCTION: You must explicitly use the actual hotel names and flight transit methods found in the data above. Do not invent, guess, or extrapolate room prices (e.g., "$47/night") unless those exact pricing figures are explicitly stated next to that specific hotel in the provided data. If a price is unclear, just omit it and list the hotel name.'''

    response = llm.invoke([
        SystemMessage(content='You are an expert travel planner that relies strictly on real-time data provided to you.'),
        HumanMessage(content=prompt)
    ])

    return {
        'itinerary': response.content,
        'message': [response],
        'llm_calls': state.get('llm_calls', 0) + 1
    } 

def final_agent(state: Travel):
    # Pass all information to the final polish agent
    final_prompt = f'''Review and completely finalize this travel itinerary. Make sure it incorporates the real-world hotel details and flight context seamlessly.
User Query: {state['user_query']}
Flight Info: {state['flight_results']}
Hotel Info: {state['hotel_results']}
Draft Itinerary: {state['itinerary']}'''

    response = llm.invoke([
        SystemMessage(content="You are a meticulous travel editor. Produce the final polished copy based on the draft, ensuring real names from the context are preserved."),
        HumanMessage(content=final_prompt)
    ])

    # CRITICAL FIX: Save the finalized result back into the 'itinerary' key 
    # so the main printer block captures it!
    return {
        'itinerary': response.content,
        'message': [response],
        'llm_calls': state.get('llm_calls', 0) + 1
    }

graph = StateGraph(Travel)

graph.add_node('flight_agent', flight_agent)
graph.add_node('hotel_agent', hotel_agent)
graph.add_node('itinerary_agent', itinerary_agent)
graph.add_node('final_agent', final_agent)

graph.add_edge(START, 'flight_agent')
graph.add_edge('flight_agent', 'hotel_agent')
graph.add_edge('hotel_agent', 'itinerary_agent')
graph.add_edge('itinerary_agent', 'final_agent')
graph.add_edge('final_agent', END)

connection_string = "postgresql://postgres:5322@localhost:5432/flight_database"

def get_app():
    try:
        conn = psycopg.connect(connection_string, autocommit=True)
        checkpointer = PostgresSaver(conn)
        checkpointer.setup()
        return graph.compile(checkpointer=checkpointer)
    except Exception as e:
        print(f"Database connection failed, falling back to Memory: {e}")
        from langgraph.checkpoint.memory import InMemorySaver
        return graph.compile(checkpointer=InMemorySaver())

app = get_app()

if __name__ == "__main__":
    config = {
        'configurable': {
            'thread_id': 'user_12345'
        }
    }

    user_input = input("Enter your travel query: ")
    
    result = app.invoke(
        {
            "message": [HumanMessage(content=user_input)], 
            "user_query": user_input
        }, 
        config=config
    )

    print('\nFinal Itinerary:\n')
    # This will now correctly grab the final updated copy from final_agent
    if 'itinerary' in result and result['itinerary']:
        print(result['itinerary'])
    else:
        # Fallback to printing the last message in the list
        print(result['message'][-1].content)