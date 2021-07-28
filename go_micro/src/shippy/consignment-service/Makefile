build:
	# protoc -I. --go_out=plugins=grpc:$(GOPATH)/src/shippy/consignment-service proto/consignment/consignment.proto
	protoc -I. --go_out=plugins=grpc:$(GOPATH)/src/shippy/consignment-service proto/consignment/consignment.proto

	#	指定 go 编译的目标系统和架构
	GOOS=linux GOARCH=amd64 go build
	#	根据当前目录下的 Dockerfile 生成名为 consignment-service 的镜像
	docker build -t consignment-service .

run:
	#	在 Docker 容器的50051端口上运行 consignment-service 服务
	#	可添加 -d 参数指定后台运行
	docker run -p 50051:50051 \
			   consignment-service