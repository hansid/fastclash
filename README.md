# fastclash

用wxpython写的clash程序管理界面，可以额外运行naive，实现clash分流后的流量传到naive。

# 界面介绍

![image](https://github.com/hansid/fastclash/blob/main/Snipaste_2025-09-12_19-55-56.png)\
## config.yaml可以参考项目中的文件
**主程序**\
选择clash的exe文件\
**配置文件夹**\
选择存放config.yaml的文件夹，这里建议把clash.exe和config.yaml放在一起\
**输入网址**\
可选可不选，功能是下载文件服务器上的config.yaml到本地，替换原来的config.yaml\
**打开代理**\
指将代理设置http://127.0.0.1:7892 \
**面板密码**\
指config.yaml中设置的密码\
**测试url**\
用来测试各个节点的延迟（http://www.google-analytics.com/generate_204）\
**次程序**\
用来运行clash官方不支持的协议，例如naiveproxy，次程序暴露一个socks5端口，主程序clash分流后将流量给到次程序的sock5端口
**次程序运行命令**\
比如有些协议的运行命令是程序名 -c 配置文件名，此时可以将 -c 填入运行命令中
**怎样切换节点**\
双击右下角表格中的节点名称，注意每次切换节点会杀死原有节点的所有链接
