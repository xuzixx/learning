package main


func myfunc(arg ...int) {
    for _, v := range arg{
        println(v)
    }
}
func main() {
    //arr := []int{1,2,3,4}
    myfunc(1, 2, 3, 4)
    println("----------------")
    myfunc(1, 2)
}
