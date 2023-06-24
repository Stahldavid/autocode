# Import langchain modules
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain.memory import ConversationBufferMemory, ReadOnlySharedMemory
from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.utilities import GoogleSearchAPIWrapper


# Import custom agents and tools
from research_agent import ResearchAgent
from approach_agent import ApproachAgent
from pseudo_code_agent import PseudoCodeAgent
from code_agent import CodeAgent
from reviewer_agent import ReviewerAgent
from graphcodebert import GraphCodeBERTTool
from unixcoder import UniXcoderTool
from codereviewer import CodeReviewerTool

# Import custom chains
from langchain import LLMChain
from summary_chain import SummaryChain
from pseudogen_chain import PseudoGenChain

# Import custom memories
from code_memory import CodeMemory
from conversation_memory import ConversationMemory

# Define memory keys
code_memory_key = "code"
conversation_memory_key = "conversation"

# Initialize shared memory for code and conversation
shared_memory_code = SharedMemory(CodeMemory(), code_memory_key)
shared_memory_conversation = SharedMemory(ConversationMemory(), conversation_memory_key)

# Initialize custom agents with shared memory
research_agent = ResearchAgent(shared_memory=shared_memory_conversation)
approach_agent = ApproachAgent(shared_memory=shared_memory_conversation)
pseudocode_agent = PseudoCodeAgent(shared_memory=shared_memory_code)
code_agent = CodeAgent(shared_memory=shared_memory_code)
reviewer_agent = ReviewerAgent(shared_memory=shared_memory_code)

# Initialize custom tools with shared memory
graphcodebert_tool = GraphCodeBERTTool(shared_memory=shared_memory_code)
unixcoder_tool = UniXcoderTool(shared_memory=shared_memory_code)
codereviewer_tool = CodeReviewerTool(shared_memory=shared_memory_code)

# Initialize custom chains with shared memory
llm_chain = LLMChain(shared_memory=shared_memory_conversation)
summary_chain = SummaryChain(shared_memory=shared_memory_conversation)
pseudogen_chain = PseudoGenChain(shared_memory=shared_memory_code)

# Initialize agent executor with agents and tools
agent_executor = AgentExecutor([research_agent, approach_agent, pseudocode_agent, code_agent, reviewer_agent], [graphcodebert_tool, unixcoder_tool, codereviewer_tool])

# Initialize tool executor with tools and chains
tool_executor = ToolExecutor([graphcodebert_tool, unixcoder_tool, codereviewer_tool], [llm_chain, summary_chain, pseudogen_chain])

# Initialize chain executor with chains and tools
chain_executor = ChainExecutor([llm_chain, summary_chain, pseudogen_chain], [graphcodebert_tool, unixcoder_tool, codereviewer_tool])

# Initialize memory executor with shared memory and agents
memory_executor = MemoryExecutor([shared_memory_code, shared_memory_conversation], [research_agent, approach_agent, pseudocode_agent, code_agent, reviewer_agent])

# Define a function to get user input from the console
def get_user_input():
    # Prompt the user to enter a query or type exit to quit
    user_input = input("Enter a query or type exit to quit: ")

    # Return the user input or None if exit is typed
    if user_input.lower() == "exit":
        return None
    else:
        return user_input

# Define a function to print the output to the console
def print_output(output):
    # Print the output with a separator line
    print("Output: " + output)
    print("-" * 80)

# Define the main function that controls the execution loop
def main():
    # Print a welcome message and instructions for using the system
    print("Welcome to our conversational AI system using LangChain framework.")
    print("You can interact with multiple agents and tools to get intelligent responses based on your input.")
    print("To use an agent or a tool, use the syntax: @agent_name: query or #tool_name: query")
    print("For example:")
    print("@research_agent: What is natural language processing?")
    print("#graphcodebert: #python: def fib(n):")
    print()

    # Get the first user input from the console
    user_input = get_user_input()

    # Loop until the user input is None
    while user_input is not None:
        # Execute the user input using the agent executor
        agent_output = agent_executor.execute(user_input)

        # Print the agent output to the console
        print_output(agent_output)

        # Execute the agent output using the tool executor
        tool_output = tool_executor.execute(agent_output)

        # Print the tool output to the console
        print_output(tool_output)

        # Execute the tool output using the chain executor
        chain_output = chain_executor.execute(tool_output)

        # Print the chain output to the console
        print_output(chain_output)

        # Execute the chain output using the memory executor
        memory_executor.execute(chain_output)

        # Get the next user input from the console
        user_input = get_user_input()

    # Print a goodbye message and exit
    print("Thank you for using our conversational AI system. Goodbye!")

# Call the main function to start the execution loop
if __name__ == "__main__":
    main()
