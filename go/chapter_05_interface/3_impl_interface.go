package main

import "fmt"


// interface
type Shaper interface {
    Area() float32
}

// struct Square 和 Rectangle, Area 绑定的内容不同
// 所以 value_pointer_test 传入不同
type Square struct {
    side float32
}
func (sq *Square) Area() float32 {
    return sq.side * sq.side
}

type Rectangle struct {
    length, width float32
}
func (r Rectangle) Area() float32 {
    return r.length * r.width
}

// print func
func PrintTestShaper(i interface{}){
    // 判断是否实现了 Shaper 接口
    println("---- in PrintTestShaper ----")
    fmt.Printf("%#v\n", i)
    if t, ok := i.(Shaper); ok {
        println("ok")
        println(t)
    }else{
        println("not ok")
    }
    println("---- end PrintTestShaper ----")
}

func print_test() {
    fmt.Printf("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
    // 它本质上是一个指针，虽然不完全是一回事。
    // 指向接口值的指针是非法的，它们不仅一点用也没有，还会导致代码错误。
    var i Shaper
    PrintTestShaper(i)

    // 同样效果的三种方式, case 1 是最简便的方式
    sq1 := new(Square)
    sq1.side = 5
    // case 1
    areaI := sq1
    PrintTestShaper(areaI)
    // case 2
    var areaI2 Shaper
    areaI2 = sq1
    PrintTestShaper(areaI2)
    // case 3
    areaI3 := Shaper(sq1)
    PrintTestShaper(areaI3)
}

func value_pointer_test() {
    fmt.Printf("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
    // Area() of Rectangle needs a value
    r := Rectangle{5, 3}
    // Area() of Square needs a pointer
    q := &Square{5}
    shapes := []Shaper{r, q}
    for _, v := range shapes {
        fmt.Printf("---------%#v\n", v)
        fmt.Println("Shape details: ", v)
        fmt.Println("Area of this shape is: ", v.Area())
    }
}

func main() {
    print_test()
    value_pointer_test()
}
