package main

import (
	"fmt"
	"time"
)

/*
   ci := make(chan int)
   cs := make(chan string)
   cf := make(chan interface{})

   ch := make(chan type, value)
   value == 0 无缓冲
   value > 0 缓冲value 个元素

   判断channel 是否关闭
   x, ok = <-ch
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
	i := 0
L:
	for {
		select {
		case <-c:
			i++
			println("--- main one done")
			if i == 2 {
				break L
			}
		}
	}
	fmt.Println("main end")
}
