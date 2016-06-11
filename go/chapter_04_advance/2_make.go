package main

/*
    make slice

    http://www.tuicool.com/articles/QrymYz
*/

import "fmt"

func main() {
    a := make([]int, 5)
    printSlice("a", a)
    println(a)
    b := make([]int, 0, 5)
    printSlice("b", b)
    println(b)
    c := b[:2]
    printSlice("c", c)
    println(c)
    d := c[2:5]
    printSlice("d", d)
    println(d)

    println("------------------")
    // b c d 低层还是同一个array
    b = append(b, 0, 1, 2, 3)
    printSlice("b", b)
    println(b)
    printSlice("c", c)
    println(c)
    printSlice("d", d)
    println(d)
}

func printSlice(s string, x []int) {
    fmt.Printf("%s len=%d cap=%d %v\n", s, len(x), cap(x), x)
}
