package main

import "fmt"

/*
   在 switch 之外使用 (type) 是非法的。

   按照约定，只包含一个方法的, 接口的名字由方法名加 [e]r 后缀组成，
   例如Printer、Reader、Writer、Logger、Converter 等等。
   还有一些不常用的方式（当后缀 er 不合适时），
   比如Recoverable，此时接口名以 able 结尾，
   或者以 I 开头（像 .NET 或 Java 中那样）。

*/

type S struct{ i int }

func (p *S) Get() int  { return p.i }
func (p *S) Put(v int) { p.i = v }

type R struct{ i int }

func (p *R) Get() int  { return p.i }
func (p *R) Put(v int) { p.i = v }

type I interface {
	Get() int
	Put(int)
}

func f(p I) {
	switch t := p.(type) {
	case *S:
		println("in case S")
		fmt.Printf("%#v\n", t)
	case *R:
		println("in case R")
		fmt.Printf("%#v\n", t)
	}
	println(p.Get())
	p.Put(1)
}

func main() {
	var s S
	var r R

	fmt.Printf("%#v\n", s)
	fmt.Printf("%#v\n", r)
	println("----------------")
	f(&s)
	f(&r)
	println("----------------")
	fmt.Printf("%#v\n", s)
	fmt.Printf("%#v\n", r)
	println("----------------")

}
