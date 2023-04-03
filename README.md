# Telepath
基于Langchain开发的，集成各种外部工具的ChatGPT命令行聊天界面。
（还没写完，别急）

## 目录

- [亮点](#亮点)
- [安装和使用](#安装和使用)

## 亮点

Telepath可以借助外部工具来充分利用GPT-3.5的语言能力。有了外部工具，ChatGPT现在可以感知世界、查询信息，甚至帮用户完成一些操作。

Telepath不需要你自己指定工具。他会分析你的问题，并在已经加载的工具中选择最优方案来解决问题。理论上，Telepath可以让ChatGPT实现任意一个功能。

目前版本的Telepath中内置了以下插件，在之后的版本中会开放扩展插件的接口，任何人都可以为Telepath开发插件并投入使用。

- CurrentTimeTool：获取当前时间
- PyInterpreter：Python代码解释器
- WolframAlpha：Wolfram Alpha接口
- WebSearch：New Bing网页搜索器
- PyPackageInstaller：Python包管理器
- BrainMemory：键值对存储

以下是一些演示：

查询在线信息（调用new bing）：

![](https://github.com/FantWu/Telepath/blob/main/images/websearch1.png)

求解数学问题（调用Wolfram Alpha）：

![](https://github.com/FantWu/Telepath/blob/main/images/math1.png)

感知当前时间：

![](https://github.com/FantWu/Telepath/blob/main/images/time.png)

读写本地文件：

![](https://github.com/FantWu/Telepath/blob/main/images/file1.png)

![](https://github.com/FantWu/Telepath/blob/main/images/file2.png)

运行Python代码：

![](https://github.com/FantWu/Telepath/blob/main/images/python1.png)

![](https://github.com/FantWu/Telepath/blob/main/images/python2.png)

安装Python库：

![](https://github.com/FantWu/Telepath/blob/main/images/python3.png)

## 安装和使用

### 准备工作：

为了获得完整的体验，在使用Telepath前，请先取得OpenAI和Wolfram Alpha的API key，以及授权使用new bing的cookies。

- OpenAI [官网](https://openai.com/)    

- Walfram Alpha [API获取页面](https://products.wolframalpha.com/api/)

- new bing获取方法如下：

1、安装浏览器插件：[Cookies Editor](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm)

2、访问[Bing首页](https://www.bing.com)，确保此时你可以使用new Bing

3、启用插件




