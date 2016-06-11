package main

import "fmt"

/*
    pointer 初始化， 赋值
*/
func main() {
    var p *int
    fmt.Printf("%v\n", p)

    var i int
    p = &i
    fmt.Printf("%v\n", p)

    *p = 8
    fmt.Printf("%v\n", *p)
    fmt.Printf("%v\n", i)

}
