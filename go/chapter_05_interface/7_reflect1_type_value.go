// blog: Laws of Reflection
package main

import (
    "fmt"
    "reflect"
)

/*
    http://www.kancloud.cn/kancloud/the-way-to-go/72529
*/
func main() {
    var x float64 = 3.4
    fmt.Println("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    fmt.Println(" var x float64 = 3.4")
    fmt.Println("x type:", reflect.TypeOf(x))
    v := reflect.ValueOf(x)
    fmt.Println("v type:", reflect.TypeOf(v))
    fmt.Printf("v value: %#v\n", v)
    fmt.Println("v.Type() type:", v.Type())
    fmt.Println("v.Kind() kind:", v.Kind())
    fmt.Println("v.Float() value:", v.Float())
    fmt.Println("v.Interface():", v.Interface())
    fmt.Printf("value is %5.2e\n", v.Interface())
    y := v.Interface().(float64)
    fmt.Printf("y %#v\n", y)

    if v.Kind() == reflect.Float64 {
        fmt.Println("v.Kind() == reflect.Float64")
    }
}

/* output:

<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
 var x float64 = 3.4
x type: float64
v type: reflect.Value
v value: 3.4
v.Type() type: float64
v.Kind() kind: float64
v.Float() value: 3.4
v.Interface(): 3.4
value is 3.40e+00
y 3.4
v.Kind() == reflect.Float64

*/
