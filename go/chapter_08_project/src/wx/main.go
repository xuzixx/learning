package main

import (
	"config"
	"fmt"
)

func main() {
	config.LoadConfig()
	fmt.Println("--------hello, go in main")
	config.WrapFunc()
	fmt.Println("--------config variable")
	fmt.Printf("%#v\n", config.CONFIG_INT)
	config.CONFIG_INT = make([]int, 10)
	fmt.Printf("%#v\n", config.CONFIG_INT)
}
