import json 
# JSON is used to parse the responses from the OpenAI API

from termcolor import colored
from code_search import similarity_search

def pretty_print_conversation(messages):
    role_to_color = {
        "system": "red",
        "user": "green",
        "assistant": "blue",
        "function": "magenta",
    }
    formatted_messages = []
    for message in messages:
        if message["role"] == "system":
            formatted_messages.append(f"system: {message['content']}\n")
        elif message["role"] == "user":
            formatted_messages.append(f"user: {message['content']}\n")
        elif message["role"] == "assistant" and message.get("function_call"):
            formatted_messages.append(f"assistant: {message['function_call']}\n")
        elif message["role"] == "assistant" and not message.get("function_call"):
            formatted_messages.append(f"assistant: {message['content']}\n")
        elif message["role"] == "function":
            # parse the JSON string back to a dictionary
            function_output = json.loads(message['content'])
            formatted_messages.append(f"function ({message['name']}): {function_output}\n")
    for formatted_message in formatted_messages:
        print(
            colored(
                formatted_message,
                role_to_color[messages[formatted_messages.index(formatted_message)]["role"]],
            )
        )

functions = [
    {
        "name": "similarity_search",
        "description": "Vectorstore embedding semantic search for code functions. It receives a query and the directory to search, and returns the most similar code snippets to the queries.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query designed to fetch code samples."
                },
                "directory": {
                    "type": "string",
                    "enum": ["db_webots", "db_ros2", "db_webots_ros2", "db_ros2_control"],
                    "description": "The directory in which to perform the search."
                }
            },
            "required": ["query", "directory"]
        }
    },
]

messages = [
    {
        "role": "system",
        "content": "You are a sophisticated AI that has the ability to analyze complex code and pseudocode documents. You are tasked with making necessary clarifications in a series of chat turns until you gather sufficient information to rewrite the code. You can utilize the 'search_code' function to fetch relevant code snippets based on semantic similarity, and subsequently improve the given file. After each search you should improve the file, do not make several calls to the function before improving the file."
    },
    {
        "role": "user",
        "content": f"I need your assistance in reviewing these code and pseudocode documents. Your final goal is to rewrite and finish the code to make it fully functional. The final goal is to create a project for variable impedance control providing force feedback. The project will use Webots, ROS2, webots_ros2, and ros2_control. You are required to identify potential problems, inefficiencies, and areas for improvements in these documents. Here are the documents you need to work on:\n\n{output_string}\n\nPlease first clarify any question that you need to finish the code with me. After you completely understand the goal of the user, use the search_code function to find relevant code that can help improve the code."  
    }
]

while True:
    chat_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k-0613",
        messages=messages,
        functions=functions,
    )
    assistant_message = chat_response['choices'][0]['message']
    messages.append(assistant_message)

    pretty_print_conversation(messages)
    
    if assistant_message.get("function_call"):
        # Extract the function name and arguments from the message
        function_name = assistant_message["function_call"]["name"]
        arguments = json.loads(assistant_message["function_call"]["arguments"])

        print(f"Function Name: {function_name}")
        print(f"Arguments: {arguments}")

        # Call the function and get the results
        if function_name == "similarity_search":
            # Initialize a results list
            all_results = []

            print("Calling similarity_search function...")
            try:
                result = similarity_search(query=arguments['query'], directories=arguments['directory'])
            except json.JSONDecodeError:
                print("Error: Invalid JSON format")
                result = {}

            print("similarity_search function returned.")
            print(f"Result: {result}")

            # Append the result to the messages
            messages.append({
                "role": "function",
                "name": function_name,
                "content": json.dumps(result)
            })