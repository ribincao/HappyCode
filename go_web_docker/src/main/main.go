package main

import (
	"log"
	"net/http"
	web "webserver"//	引用 github.com/webserver 相当于应用了我们编写的 webserver
)

func main() {
	http.HandleFunc("/test", web.SayHello)

	err := http.ListenAndServe(":8080", nil)
	if err != nil {
		log.Fatal("ListenAndServer:", err)
	}
}

