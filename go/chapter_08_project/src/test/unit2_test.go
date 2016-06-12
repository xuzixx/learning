package test

import (
	"config"
	"fmt"
	"testing"
)

func TestMain3(t *testing.T) {
	fmt.Println("<<<<<test 3 main <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
	config.LoadConfig()
	fmt.Println("--------hello, go in main")
	config.WrapFunc()
	fmt.Println("--------config variable")
	fmt.Printf("%#v\n", config.CONFIG_INT)
	config.CONFIG_INT = make([]int, 10)
	config.CONFIG_INT[0] = 10000
	fmt.Printf("%#v\n", config.CONFIG_INT)
}
