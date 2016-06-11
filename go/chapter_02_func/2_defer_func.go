package main

/*
    defer func () 必须
*/
func f1() (ret int){
    // return 1
    defer func(){
        ret += 1
    }()
    return 0
}

func f2() (ret int){
    // return 100
    defer func(x int){
        ret += x
    }(100)
    return 0
}

func main() {
    f1 := f1()
    println(f1)

    f2 := f2()
    println(f2)
}

