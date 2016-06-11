package main


import (
    "fmt"
    "reflect"
)

type TagType struct { // tags
    field1 bool   "An important answer"
    field2 string "The name of the thing"
    field3 int    "How much there are"
}

func refTag(tt TagType, ix int) {
    // reflect.TypeOf() 可以获取变量的正确类型
    ttType := reflect.TypeOf(tt)
    ixField := ttType.Field(ix)
    fmt.Printf("%#v\n", ttType)
    fmt.Printf("%#v\n", ixField)
    fmt.Printf("%#v\n", ixField.Tag)
}

func main() {
    tt := TagType{true, "Barak Obama", 1}
    for i := 0; i < 3; i++ {
        refTag(tt, i)
    }
}
