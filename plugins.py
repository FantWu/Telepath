import asyncio
import datetime
import os

import requests
from duckduckgo_search import ddg_answers
from langchain import OpenAI
from langchain.agents.agent_toolkits import create_python_agent
from langchain.python import PythonREPL
from langchain.tools import BaseTool
from langchain.utilities.wolfram_alpha import WolframAlphaAPIWrapper
from pydantic import Field
from rich.console import Console
from rich.table import Table

import urlsummary
from bing import Bing
from brain import Brain
from config import config_instance
from prompt_buffer import buffer

os.environ["WOLFRAM_ALPHA_APPID"] = config_instance.wolfram_alpha_api_key

console = Console()
bing = Bing()


def _get_default_python_repl() -> PythonREPL:
    return PythonREPL(_globals=globals(), _locals=None)


class PythonREPLTool(BaseTool):
    """A tool for running python code in a REPL."""

    name = "Python REPL"
    description = (
        "A Python shell. Use this to execute python commands. "
        "Input should be a valid python command. "
        "If you want to see the output of a value, you should print it out "
        "with `print(...)`."
    )
    python_repl: PythonREPL = Field(default_factory=_get_default_python_repl)

    def _run(self, query: str) -> str:
        """Use the tool."""
        console.log(f"[bold green]call {self.name}[/]: {query}")
        r = self.python_repl.run(query)
        console.log(f"[bold green]return:[/]\n {r}")
        return r

    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("PythonReplTool does not support async")


py_agent = create_python_agent(
    llm=OpenAI(
        temperature=0.5,
        max_tokens=1000,
        openai_api_key=config_instance.openai_api_key,
    ),
    tool=PythonREPLTool(),
    verbose=False
)


class CurrentTimeTool(BaseTool):
    name = "Time"
    description = '''
    Return the current time
    '''

    def _run(self, tool_input: str) -> str:
        console.log(f"[bold green]call {self.name}[/]: {tool_input}")
        r = f"The current time is：{str(datetime.datetime.now())}"
        console.log(f"[bold green]return:[/]\n {r}")
        return r

    async def _arun(self, tool_input: str) -> str:
        raise NotImplementedError("CurrentTimeTool does not support async")


class PyInterpreter(BaseTool):
    name = "Python Execute"
    description = '''
    Function: Using Python to solve complex problems or assist users in performing operations such as modifying files and drawing graph
    '''

    def _run(self, tool_input: str) -> str:
        console.log(f"[bold green]call {self.name}[/]: {tool_input}")
        r = py_agent.run(buffer.get_buffer())
        console.log(f"[bold green]return:[/]\n {r}")
        return r

    async def _arun(self, tool_input: str) -> str:
        raise NotImplementedError("PyInterpreter does not support async")


class PyPackageInstaller(BaseTool):
    name = "Python Package Installer"
    description = '''
    A Python Package Installer that can help you install a required Python package on the system
    
    Input: Package name
    '''

    def _run(self, tool_input: str) -> str:
        console.log(f"[bold green]call {self.name}[/]: {tool_input}")
        f = os.popen(f"pip3 install {tool_input}")
        r = f.read()
        console.log(f"[bold green]return:[/]\n {r}")
        return r

    async def _arun(self, tool_input: str) -> str:
        raise NotImplementedError("PyPackageInstaller does not support async")


class todolist(BaseTool):
    name = "TODO List"
    description = '''
    A simple TODO list.

    input "READ" to read the TODO list;
    '''

    def _run(self, tool_input: str) -> str:
        console.log(f"[bold green]call {self.name}[/]: {tool_input}")
        r = "TODO list: To have a dinner on 6:00 PM"
        console.log(f"[bold green]return:[/]\n {r}")
        return r

    async def _arun(self, tool_input: str) -> str:
        raise NotImplementedError("todolist does not support async")


class WolframAlpha(BaseTool):
    name = "Wolfram Alpha"
    description = '''
    Function: Use wolfram alpha API to solve mathematical questions, or to calculate a math problem.
    
    Input: mathematical question in single line
    '''

    def _run(self, tool_input: str) -> str:
        console.log(f"[bold green]call {self.name}[/]: {tool_input}")
        wolfram = WolframAlphaAPIWrapper()
        r = wolfram.run(tool_input)
        console.log(f"[bold green]return:[/]\n {r}")
        return r

    async def _arun(self, tool_input: str) -> str:
        raise NotImplementedError("WolframAlpha does not support async")


class WebSearch2(BaseTool):
    name = "Web Search"
    description = '''
    A web searcher that return the search result on the Internet. Use this tool if you need to search something on the Internet.

    Input: search query
    '''

    def _run(self, tool_input: str) -> str:
        console.log(f"[bold green]call {self.name}[/]: {tool_input}")
        results = ddg_answers(keywords=tool_input, related=True)
        table = Table(title=f"Instant Answers Results: {tool_input}")
        table.add_column("text")
        table.add_column("topic")
        table.add_column("url")

        for i in results:
            table.add_row(i["text"], i["topic"], i["url"])

        console.print(table)

        url = f"https://ddg-webapp-aagd.vercel.app/search?q={tool_input}&max_results=7&region=en-us&timePeriod=m"
        response = requests.get(url)

        if response.status_code == 200:
            r = response.json()
            table = Table(title=f"Search Results: {tool_input}")
            table.add_column("title")
            table.add_column("url")
            table.add_column("body")
            for i in r:
                table.add_row(i["title"], i["href"], i["body"])
            console.print(table)
        else:
            r = "Search failed"
            console.log(f"[bold green]return:[/]\n {r}")

        results = results + r
        return results

    async def _arun(self, tool_input: str) -> str:
        raise NotImplementedError("WebSearch does not support async")


class WebSearch(BaseTool):
    name = "Web Search by new Bing"
    description = '''
    A web searcher that return the search result on the Internet. Use this tool if you need to search something on the Internet.

    Input: search query
    
    Note: If you need to reference the results in your answer, please include the corresponding URL in your answer as well.
    '''

    def _run(self, tool_input: str) -> str:
        console.log(f"[bold green]call {self.name}[/]: {tool_input}")
        global bing
        r = asyncio.run(bing.get(question=tool_input))
        console.log(f"[bold green]return:[/]\n {r}")
        return r

    async def _arun(self, tool_input: str) -> str:
        console.log(f"[bold green]call {self.name}[/]: {tool_input}")
        global bing
        r = await bing.get(question=tool_input)
        console.log(f"[bold green]return:[/]\n {r}")
        return r


class CommandShell(BaseTool):
    name = "Terminal"
    description = '''
    System terminal that can execute commands.
    
    Input: command to be executed.
    '''

    def _run(self, tool_input: str) -> str:
        console.log(f"[bold green]call {self.name}[/]: {tool_input}")
        f = os.popen(tool_input)
        r = f.read()
        console.log(f"[bold green]return:[/]\n {r}")
        return r

    async def _arun(self, tool_input: str) -> str:
        raise NotImplementedError("CommandShell does not support async")


class UrlSummary(BaseTool):
    name = "Get URL Summary"
    description = '''
    A tool that can get a brief summary of a URL
    
    Input: URL
    '''

    def _run(self, tool_input: str) -> str:
        console.log(f"[bold green]call {self.name}[/]: {tool_input}")
        try:
            '''
            a = Article(tool_input)
            a.download()
            a.parse()
            a.nlp()
            return a.summary
            '''
            r = urlsummary.get_webpage_summary(tool_input)
            console.log(f"[bold green]return:[/]\n {r}")
            return r
        except Exception as e:
            return "Summary failed"

    async def _arun(self, tool_input: str) -> str:
        raise NotImplementedError("UrlSummary does not support async")


class BrainMemoryCreator(BaseTool):
    name = "Brain Memory Creator"
    description = '''
    You have a brain that can remember things and retrieve when needed. This tool is for you to create a memory.
    
    Your memory will be storage as a key-value pair. 
    
    The input to this tool should be a comma separated list of key and value, like "key, value"
    
    For example, "Birthday, 2023/1/1" means to remember birthday is 2023/1/1
    '''

    def _run(self, tool_input: str) -> str:
        console.log(f"[bold green]call {self.name}[/]: {tool_input}")
        key, value = tool_input.split(",")
        try:
            brain = Brain()
            brain.read()
            brain.append(key, value)
            brain.save()
            r = "Memory Success"
        except Exception as e:
            r = f"Error: {e}"
        console.log(f"[bold green]return:[/]\n {r}")
        return r

    async def _arun(self, tool_input: str) -> str:
        raise NotImplementedError("BrainMemoryCreator does not support async")


class BrainMemoryRetriever(BaseTool):
    name = "Brain Memory Retriever"
    description = '''
    You have a brain that can remember things and retrieve when needed. This tool is for you to retrieve from memory.
    
    Your memory will be storage as a key-value pair. Input a key so that you can get the value.
    
    The input to this tool should be the key as a string
    
    For example, "Birthday"
    '''

    def _run(self, tool_input: str) -> str:
        console.log(f"[bold green]call {self.name}[/]: {tool_input}")
        try:
            brain = Brain()
            brain.read()
            r = brain.get(tool_input)
        except Exception as e:
            r = f"Error: {e}"
        console.log(f"[bold green]return:[/]\n {r}")
        return r

    async def _arun(self, tool_input: str) -> str:
        raise NotImplementedError("BrainMemoryRetriever does not support async")
