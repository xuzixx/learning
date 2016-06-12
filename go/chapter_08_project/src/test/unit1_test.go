package test

import (
	"config"
	"fmt"
	"testing"
)

func TestMain1(t *testing.T) {
	fmt.Println("<<<<<test 1 main <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
	config.LoadConfig()
	fmt.Println("--------hello, go in main")
	config.WrapFunc()
	fmt.Println("--------config variable")
	fmt.Printf("%#v\n", config.CONFIG_INT)
	config.CONFIG_INT = make([]int, 10)
	config.CONFIG_INT[0] = 10000
	fmt.Printf("%#v\n", config.CONFIG_INT)
}

func TestMain2(t *testing.T) {
	fmt.Println("<<<<<test 2 main <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
	config.LoadConfig()
	fmt.Println("--------hello, go in main")
	config.WrapFunc()
	fmt.Println("--------config variable")
	fmt.Printf("%#v\n", config.CONFIG_INT)
	config.CONFIG_INT = make([]int, 10)
	fmt.Printf("%#v\n", config.CONFIG_INT)
}
