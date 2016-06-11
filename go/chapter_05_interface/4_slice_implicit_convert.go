package main

import "fmt"

/*

    会报错
    http://my.oschina.net/xlplbo/blog/199145

    # command-line-arguments
    ./4_slice_implicit_convert.go:10: cannot type switch on non-interface value i (type []interface {})
    ./4_slice_implicit_convert.go:27: cannot use int_i (type interface {}) as type []interface {} in argument to sort: need type assertion
    ./4_slice_implicit_convert.go:28: cannot use str_i (type interface {}) as type []interface {} in argument to sort: need type assertion

    http://studygolang.com/articles/2509
*/
func sort(i []interface{}) {
    // 应给写排序的算法 简单省略
    switch i.(type) {
        case string:
            println("in string")
            fmt.Printf("%#v\n", i)
        case int:
            println("in int")
            fmt.Printf("%#v\n", i)
    }
}

func main() {
    arr_int := [3]int{1, 2, 3}
    arr_str := [3]string{"qwe", "asd", "zxc"}

    var int_i interface{}
    var str_i interface{}

    sort(int_i)
    sort(str_i)
}
