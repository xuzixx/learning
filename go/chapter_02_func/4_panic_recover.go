package main

import "log"

/*
    panic recover

    panicFunc 异常，defer 1st会执行
*/

func panicFunc(i int){
    println("panicFunc begin")
    defer println("1st i=", i)
    println(100/i)
    defer println("2nd i=", i)
}

func throwsPanic(f func(int), i int) (b bool) {
    defer func(){
        if x := recover(); x != nil {
            log.Println("[E]", x)
            b = true
        }
    }()
    f(i)
    return
}

func main() {
    //panicFunc begin
    //100
    //2nd i= 1
    //1st i= 1
    //throwsPanic result
    //false
    r := throwsPanic(panicFunc, 1)
    println("throwsPanic result")
    println(r)

    println("----------------")
    //panicFunc begin
    //1st i= 0
    //2016/06/11 11:11:27 [E] runtime error: integer divide by zero
    //throwsPanic result
    //true
    r2 := throwsPanic(panicFunc, 0)
    println("throwsPanic result")
    println(r2)
}
