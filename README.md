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

### 准备工作

为了获得完整的体验，在使用Telepath前，请先取得OpenAI和Wolfram Alpha的API key，以及授权使用new bing的cookies。

- OpenAI [官网](https://openai.com/)    

- Walfram Alpha [API获取页面](https://products.wolframalpha.com/api/)

- new bing Cookies

### new bing Cookies获取方法

1、安装浏览器插件：[Cookies Editor](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm)

2、访问[Bing首页](https://www.bing.com)，确保此时你可以使用new Bing

3、启用插件，点击插件界面右下角的Export，然后点击Export as JSON，此时cookies已经复制到剪贴板上了。

![](https://github.com/FantWu/Telepath/blob/main/images/exportcookies.png)

4、在主程序的目录下新建一个文件，名字叫bing_cookie.txt，然后把cookies粘贴进去即可。

### 安装程序

1、在你的系统上安装`Python 3.9+`

2、Clone整个源码，或者下载源码压缩包并解压到合适的位置

3、在源码文件夹中打开终端，安装依赖

```
pip3 install -r requirements.txt
```

4、把bing_cookie.txt放到和主程序main.py相同的文件夹中

5、编辑config.ini

```
[keys]
openai_api_key=<在这里填你的OpenAI API Key>
wolfram_alpha_api_key=<在这里填你的Wolfram Alpha API Key>
[settings]
language_mode=<语言模式，c表示中文模式，若不需要中文模式可改为任何一个其他字母，默认为c>
your_name=<你的用户名>
bing_cookie=<bing cookies文件名，默认为bing_cookie.txt>
show_balance=<是否开启显示余额功能，true为开启，false为关闭，默认为true>
```

6、运行程序

```
python3 main.py
```









