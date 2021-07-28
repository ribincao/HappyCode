build:
	# 指定编译生成目标系统程序
	GOOS=linux GOARCH=amd64 go build ./src/main/main.go
	# 执行 Dockerfile 的命令
	docker build -t webserve .
run:
	# 物理机端口:虚拟环境端口
	docker run -p 8080:8080 webserve