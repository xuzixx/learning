package main

import "fmt"

/*
   长字符串变量 命名
   rune, str 替换

   a = []rune(str)
   str = string(a)
*/
const (
	a = iota
	b
)

func main() {
	long_s := "AAAAAAAAAAAAAAAAAA" +
		"BBBBBBBBBBBBBBB"

	long_s2 := `AAAAAAAAAAAAAAAAA
    BBBBBBBBBBBB`

	fmt.Printf("<<<<<<<<<<<每次调用自增的常量 <\n")
	fmt.Printf("const a:%v\n", a)
	fmt.Printf("const b:%v\n", b)
	fmt.Printf("const a:%v\n", a)
	fmt.Printf("const b:%v\n", b)
	fmt.Printf("<<<<<<<<<<<Long str <<<<<<<<<<<\n")
	fmt.Printf("long_s: %v\n", long_s)
	fmt.Printf("long_s2: %v\n", long_s2)

	fmt.Printf("<<<<<<<<<<< s -> s2  <<<<<<<<<<\n")
	s := "hello"
	c := []rune(s)
	c[0] = 'c'
	s2 := string(c)
	fmt.Printf("%s\n", s2)

}
