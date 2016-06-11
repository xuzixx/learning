package main

//import "fmt"

/*
    func (p mytype) funcname(q int) (r,s int) { return 0,0 }
    p mytype 接收者
    q int 输入
    r, s int 返回
*/

func test_multi_return() (string, int) {
    return "qwert", 1
}

func main() {
    str, i := test_multi_return()
    println(str)
    println(i)
}
