from langchain.agents import initialize_agent, load_tools
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from rich import print
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table

import openai_balance
import plugins
from config import config_instance
from prompt_buffer import buffer
import readline # 有用，别删！！

telepath = '''
$$$$$$$$\        $$\                                $$\     $$\       
\__$$  __|       $$ |                               $$ |    $$ |      
   $$ | $$$$$$\  $$ | $$$$$$\   $$$$$$\   $$$$$$\ $$$$$$\   $$$$$$$\  
   $$ |$$  __$$\ $$ |$$  __$$\ $$  __$$\  \____$$\\_$$  _|  $$  __$$\ 
   $$ |$$$$$$$$ |$$ |$$$$$$$$ |$$ /  $$ | $$$$$$$ | $$ |    $$ |  $$ |
   $$ |$$   ____|$$ |$$   ____|$$ |  $$ |$$  __$$ | $$ |$$\ $$ |  $$ |
   $$ |\$$$$$$$\ $$ |\$$$$$$$\ $$$$$$$  |\$$$$$$$ | \$$$$  |$$ |  $$ |
   \__| \_______|\__| \_______|$$  ____/  \_______|  \____/ \__|  \__|
                               $$ |                                   
                               $$ |                                   
                               \__|   
'''

print(telepath)
console = Console()
console.print("[bold green]Telepath Insider Alpha")
console.print("By FantWu")

chat = ChatOpenAI(
    temperature=0.5,
    openai_api_key=config_instance.openai_api_key
)

tools = [
    # load_tools(["human"])[0],
    plugins.CurrentTimeTool(),
    # plugins.todolist(),
    plugins.PyInterpreter(),
    plugins.WolframAlpha(),
    plugins.WebSearch(),
    plugins.CommandShell(),
    # plugins.UrlSummary(),
    plugins.PyPackageInstaller(),
    plugins.BrainMemoryCreator(),
    plugins.BrainMemoryRetriever()
]

table = Table(show_header=True, header_style="bold magenta")
table.add_column("Enabled Apps")
for i in tools:
    table.add_row(i.name)

console.print(table)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

agent = initialize_agent(
    tools,
    chat,
    agent="conversational-react-description",
    verbose=False,
    memory=memory,
)


def translate(prompt, input_language: str, output_language: str):
    # print(f"[translate] {input_language}-{output_language} {prompt}", end="")
    # console.log(f"[translate] {input_language}-{output_language} {prompt}")
    if config_instance.language_mode != "c":
        return prompt
    translator = ChatOpenAI(
        temperature=0.1,
        openai_api_key=config_instance.openai_api_key
    )
    template = "You are a helpful assistant that translates {input_language} to {output_language}."
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template = '''
    Please rewrite the following content in {output_language}, 
    with the requirement that the rewritten content is closer to the language habits of {output_language}, 
    and accurately preserves all key points.
    
    {text}
    '''
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    message = chat_prompt.format_prompt(input_language=input_language, output_language=output_language,
                                        text=prompt).to_messages()
    c = translator(message).content
    # print(f" -> {c}")
    # console.log(f" -> {c}")
    return c


with console.status("[bold green]Initializing...") as status:
    max_retry = 3
    while max_retry > 0:
        try:
            str = '''You are an artificial intelligence assistant named Telepath, developed using GPT-3.5.

Your language skills are strong, and you can solve any questions that users ask you.

You have the ability to call external tools. When you call an external tool, it will provide you with some information, which you can use when answering.

Please remember: your answer should be as detailed as possible. If you are going to cite information from the internet, please add the corresponding URL at the appropriate location.
                '''

            console.log(agent.run(str))
        except Exception as e:
            max_retry -= 1
            if max_retry == 0:
                console.log("Failed to start Telepath")
                exit(1)
        else:
            break

while True:
    prompt = ""
    print()
    if config_instance.show_balance == "true":
        try:
            prompt = input(f"[Total used: USD {openai_balance.get_balance()}][{config_instance.your_name}] ")
            if prompt == "":
                continue
            elif prompt == "!exit":
                exit(0)
            else:
                buffer.set_buffer(prompt)
        except Exception as e:
            prompt = input(f"[{config_instance.your_name}] ")
            buffer.set_buffer(prompt)
    else:
        prompt = input(f"[{config_instance.your_name}] ")
        buffer.set_buffer(prompt)
    max_retry = 3
    while max_retry > 0:
        try:
            prompt = translate(prompt, input_language="Chinese", output_language="English")
            re = agent.run(prompt)
            re = translate(re, input_language="English", output_language="Chinese")
            markdown = Markdown(re)
            print()
            print()
            console.print(markdown)
        except Exception as e:
            console.log(f"Error: {e} ...Retrying")
            max_retry -= 1
            if max_retry == 0:
                console.log("Maximum number of retries exceeded")
                break
        else:
            break
