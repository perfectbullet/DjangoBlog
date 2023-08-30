# Nexus Maven Migration

This project is a simple tool written in Python to upload Maven local repository to Sonatype Nexus Repository Manage through the [Nexus API](https://help.sonatype.com/repomanager3/rest-and-integration-api).
The script will find dependencies in local repository with a deep search and will upload do Nexus server.

This tool can be useful to migrate different Repository Managers.

# Getting start

You need Python 3 with requests module installed. To install the module use this pip command:

```console
    pip install requests
```

Then, run de main.py Python script:

```console
    python main.py
```


# 打包
1. 拷贝代码到 myapp 目录
2. 进入 myapp, 修改 程序入口代码文件为 main.py
3. 记得激活虚拟环境
4. 执行命令
    pyinstaller -w -D  main.py --clean

5. 打包后的文件在 myapp/dist/main 下