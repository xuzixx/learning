package main

import "fmt"

type square struct{ r int }
type circle struct{ r int }

func (s square) area() int { return s.r * s.r }
func (c circle) area() int { return c.r * 3 }

func main() {
    s := square{1}
    c := circle{1}
    // a 是interface{} 空interface 类型的数组变量
    // 可以把任何类型的值放入其单元。
    // 此处我们分别放入单位方形和单位圆形变量s和c的值。
    a := [2]interface{}{s, c}

    fmt.Println(s, c, a)
    sum := 0
    for _, t := range a {
        switch v := t.(type) {
            case square:
                sum += v.area()
            case circle:
                sum += v.area()
        }
    }
    fmt.Println(sum)
}
