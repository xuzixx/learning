package main

import (
	"fmt"
	"myconfig"
)

func main() {
	config.LoadConfig()
	fmt.Println("hello, go\n")
}
