package webserver

import (
	"net/http"
	"fmt"
)

func SayHello(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Hello Golang")
}