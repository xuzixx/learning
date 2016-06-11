package main

import "fmt"

/*
    4_slice_implicit_convert 改编版本, 不报错
*/
type Base interface {}

type IntTest []int
type StringTest []string

func sort(i Base) {
    // 应给写排序的算法 简单省略
    switch i.(type) {
        case IntTest:
            println("---- in IntTest")
            fmt.Printf("%#v\n", i)
        case StringTest:
            println("---- in StringTest")
            fmt.Printf("%#v\n", i)
    }
}

func main() {
    int_i := IntTest{2, 2, 3, 3, 5, 7, 6, 8, 100, 12, 34}
    str_i := StringTest{"qwe", "asd", "zxc"}

    sort(int_i)
    sort(str_i)
}
