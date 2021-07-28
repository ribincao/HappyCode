# 拉取镜像
FROM alpine:latest
# 虚拟环境创建一个 webapp 目录
RUN mkdir /webapp
# 将 webapp 目录设置为工作目录
WORKDIR /webapp
# 将我们将要编译生成的 main 执行文件添加到工作目录并命名为 webserve
ADD main /webapp/webserve
# 启动 webserve
CMD ["./webserve"]