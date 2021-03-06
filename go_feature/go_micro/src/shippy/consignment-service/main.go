package main

import (
	pb "shippy/consignment-service/proto/consignment"
	"context"
	"net"
	"log"
	"google.golang.org/grpc"
)

const (
	PORT = ":50051"
)

type IRepository interface {
	Create(consignment *pb.Consignment) (*pb.Consignment, error)
	GetAll() []*pb.Consignment
}

type Repository struct {
	consignments []*pb.Consignment
}

func (repo *Repository) Create(consignment *pb.Consignment) (*pb.Consignment, error) {
	repo.consignments = append(repo.consignments, consignment)
	return consignment, nil
}

func (repo *Repository) GetAll() []*pb.Consignment {
	return repo.consignments
}
//	定义微服务
type service struct {
	repo Repository
}
func (s *service) CreateConsignment(ctx context.Context, req *pb.Consignment) (*pb.Response, error) {
	consignment, err := s.repo.Create(req)
	if err != nil {
		return nil, err
	}
	resp := &pb.Response{
				Created:	true, 
				Consignment:	consignment}
	return resp, nil
}

func (s *service) GetConsignments(ctx context.Context, req *pb.GetRequest) (*pb.Response, error) {
	allConsignments := s.repo.GetAll()
	resp := &pb.Response{
		Consignments: allConsignments}
	return resp, nil
}

// func main()  {
// 	server := micro.NewService(
// 		micro.Name("go.micro.srv.consignment"),
// 		micro.Version("latest"),
// 	)

// 	server.Init()
// 	repo := Repository{}
// 	pb.RegisterShippingServiceHandler(server.Server(), &service{repo})
// 	if err := server.Run(); err != nil {
// 		log.Fatalf("failed to server: %v",)
// 	}
// }




func main() {
	listener, err := net.Listen("tcp", PORT)
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	log.Printf("listen on: %s\n", PORT)

	server := grpc.NewServer()
	repo := Repository{}

	pb.RegisterShippingServiceServer(server, &service{repo})
	if err := server.Serve(listener); err != nil {
		log.Fatalf("failed to server: %v", err)
	} 
}