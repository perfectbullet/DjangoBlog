# 笔记本

## 工作日志记录
### 20230720
- 联调
- pywebview
- Flask swagger

## Flask 方案
《 Flask 方案 》 中介绍了一些常用的解决方案。
https://dormousehole.readthedocs.io/en/2.1.2/patterns/index.html
- flask 文件上传
https://dormousehole.readthedocs.io/en/latest/patterns/fileuploads.html
- flask 数据库
- 进程中使用flask
https://stackoverflow.com/questions/71024343/how-to-run-flask-in-another-process

- genvent 作为 wsgi  
https://blog.csdn.net/cdknight_happy/article/details/112981031
- 在子进程中运行 genvent 

## 数据接口

### 打包 sofa 接口
```json
{
  "sofaFile": "sofa-master1.zip",
  "sofaFilePath": "D:\\zjpython_work\\PPX_GX\\upload_datas\\sofa-master1\\sofa-master1.zip",
  "sofaName": "sofa-master1",
  "nginxFile": "nginx_dysy.conf",
  "nginxFilePath": "D:\\zjpython_work\\PPX_GX\\upload_datas\\sofa-master1\\nginx_dysy.conf",
  "pluginList": [
    {
      "sofaPluginFile": "sofa-node-plugin2.zip",
      "sofaPluginFilePath": "D:\\zjpython_work\\PPX_GX\\upload_datas\\sofa-master1\\sofa-node-plugin2.zip",
      "htmlFile": "sofa-node-plugin2对应的前端.zip",
      "htmlFilePath": "D:\\zjpython_work\\PPX_GX\\upload_datas\\sofa-master1\\sofa-node-plugin2对应的前端.zip",
      "router": "sofa-master1/sofa-node-plugin2/",
      "module": "sofa-node-plugin2"
    },
    {
      "sofaPluginFile": "sofa-node-plugin3.zip",
      "sofaPluginFilePath": "D:\\zjpython_work\\PPX_GX\\upload_datas\\sofa-master1\\sofa-node-plugin3.zip",
      "htmlFile": "sofa-node-plugin3对应的前端.zip",
      "htmlFilePath": "D:\\zjpython_work\\PPX_GX\\upload_datas\\sofa-master1\\sofa-node-plugin3对应的前端.zip",
      "router": "sofa-master1/sofa-node-plugin3/",
      "module": "sofa-node-plugin3"
    }
  ]
}
```

### 文件上传数据表示
- pluginFlag="sofa-node-plugin"  表示插件
- pluginFlag="sofa-master-container"  表示sofa容器

