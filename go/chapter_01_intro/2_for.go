package main

import "fmt"

/*
    break 跳出指定循环
    range -- slice, string
*/

func main() {
    println("<<<< part 1 <<<<<<<<<<<<<<<<<<<<<<<<")
    for j:=0; j<3; j++ {
        println("-----j: ", j)
        for i:=0; i<10; i++ {
            if i>5 {
                break
            }
            println("-------i: ", i)
        }
    }
    println("=====================")
    // break 指定循环
    J: for j:=0; j<3; j++ {
        println("-----j: ", j)
        for i:=0; i<10; i++ {
            if i>5 {
                break J
            }
            println("-------i: ", i)
        }
    }
    println("<<<< part 2 <<<<<<<<<<<<<<<<<<<<<<<<")
    list := []string {"a", "b", "c", "d", "e", "f"}
    for k, v := range list{
        println(k, v)
    }
    for pos, char := range "aΦx" {
        fmt.Printf("character '%c' starts at byte position %d\n", char, pos)
    }

}
