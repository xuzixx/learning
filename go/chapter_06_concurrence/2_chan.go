package main

import (
	"fmt"
	"time"
)

/*
   ci := make(chan int)
   cs := make(chan string)
   cf := make(chan interface{})
*/

// 全局的 chan
var c chan int

func ready(w string, sec int) {
	time.Sleep(time.Duration(sec) * time.Second)
	fmt.Println(w, "Done")
	c <- 1
}

func main() {
	c = make(chan int)
	go ready("Tea", 2)
	go ready("Coffee", 1)

	fmt.Println("main waiting")
	// 丢弃 接受到的值
	<-c
	<-c
	fmt.Println("main end")
}
