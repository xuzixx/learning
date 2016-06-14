package main

//import "fmt"
/*
   u开头的类型就是无符号 uint8 uint16 ...

   byte类型，这个类型和uint8是一样的，表示字节类型。
   另外一个是rune类型，这个类型和int32是一样的，
   用来表示unicode的代码点，就是unicode字符所对应的整数。

   string(a) <-> []byte(s)
   string(a) <-> []int(s)
   string(a) <-> []rune(s)

   float32(i) <-> int(f)
*/

func main() {
	/*
	   hello
	   āЀA
	*/
	b := []byte{'h', 'e', 'l', 'l', 'o'} // 复合声明
	s := string(b)
	println(s)
	i := []rune{257, 1024, 65}
	r := string(i)
	println(r)
	println("--------------")
	for _, i := range []rune(r) {
		println(i)
		println(string(i))
	}
	println("--------------")
	u := uint8('C')
	println(u)
}
