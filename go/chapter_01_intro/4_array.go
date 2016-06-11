package main

import "fmt"

/*
    Array:

    var a [3]
    a := [3]int{1, 2, 3}
    a := [...]int{1, 2, 3}

    a := [3][2]int { [2]int {1,2}, [2]int {3,4}, [2]int {5,6} }
    a := [3][2]int { [...]int {1,2}, [...]int {3,4}, [...]int {5,6} }
    a := [3][2]int { {1,2}, {3,4}, {5,6} }

*/
/*
    Slice
    // append
    s0 := []int {0, 0}
    s1 := append(s0, 2)
    s2 := append(s1, 3, 5, 7) 
    s3 := append(s2, s0...) // 需要三个点
*/

func main() {
    println("<<<< part 1 <<<<<<<<<<<<<<<<<<<<<<<<")
    // make a slice from a array
    arr := [...]int {1, 2, 3, 4, 5}
    s2 := arr[1:5]

    for i:=0 ; i<len(s2); i++ {
        println(s2[i])
    }

    println("---- change slice s2[0]")
    s2[0] = 1000
    println("print arr", arr[1])
    println("---- also change the array")

    println("<<<< part 2 <<<<<<<<<<<<<<<<<<<<<<<<")
    // test copy
    var arr2 = [...]int{0,1,2,3,4,5,6,7}
    var s = make([]int, 6)
    for i:=0 ; i<len(s); i++ {
        print(s[i],",")
    }
    println()
    println("slice init end")
    n1 := copy(s, arr2[0:])
    //n1 == 6, s == []int{0, 1, 2, 3, 4, 5}
    println(n1)

    println("---- change slice s[0]")
    s[0] = 1000
    println("s[0]", s[0])
    println("arr2[0]", arr2[0])
    println("---- copy a new array to the slice")

    n2 := copy(s, s[2:])
    //n2 == 4, s == []int{2, 3, 4, 5, 4, 5}
    println(n2)
    println("fmt print")
    fmt.Printf("%v\n", s)

    println("<<<< part 3 <<<<<<<<<<<<<<<<<<<<<<<<")
    m := map[string] int {
        "key": 123,
    }
    v, ok := m["Jan"]
    println(ok)
    println(v)
    v2, ok2 := m["key"]
    println(ok2)
    println(v2)

}
