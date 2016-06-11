package main

import "fmt"

/*
    %T
    %v
*/
func main() {
    println("<< str <<<<<<<<<<<<<<<<<<<<<")
    str := "qwer"
    fmt.Printf("%T\n", str)

    println("<< arr <<<<<<<<<<<<<<<<<<<<<")
    arr := []int{1, 2, 3, 4}
    fmt.Printf("%T\n", arr)
    fmt.Printf("%+v\n", arr)
    fmt.Printf("%v\n", arr)
    fmt.Printf("%#v\n", arr)

    println("<< func <<<<<<<<<<<<<<<<<<<<")
    f := func(){
        println("this is a func")
    }
    fmt.Printf("%T\n", f)

    println("<< slice <<<<<<<<<<<<<<<<<<<")
    var s = make([]int, 6)
    fmt.Printf("%T\n", s)
    fmt.Printf("%v\n", s)
}
