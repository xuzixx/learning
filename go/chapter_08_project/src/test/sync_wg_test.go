package test

import (
	"fmt"
	"sync"
	"testing"
)

var wg sync.WaitGroup

func TestMain1(t *testing.T) {
	/*
		init == loop

		init > loop
		fatal error: all goroutines are asleep - deadlock!

		init < loop
		panic: sync: negative WaitGroup counter
	*/
	fmt.Println("<<<<<test 1 main <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
	init := 20
	loop := 20

	wg.Add(init)

	go func() {
		for i := 0; i < loop; i++ {
			go func(i int, n *sync.WaitGroup) {
				defer n.Done()

				line := fmt.Sprintf("line_%v", i)
				fmt.Println(line)
			}(i, &wg)
		}
	}()

	wg.Wait()
	fmt.Println(string("Done"))
}
