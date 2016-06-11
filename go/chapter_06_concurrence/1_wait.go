package main

import (
    "fmt"
    "time"
)

/*
    main waiting
    Coffee Done
    Tea Done
    main end
    
    如果 主函数 不sleep
    main waiting
    main end
*/
func ready(w string, sec int) {
    time.Sleep(time.Duration(sec) * time.Second)
    fmt.Println(w, "Done")
}

func main() {
    go ready("Tea", 2)
    go ready("Coffee", 1)

    fmt.Println("main waiting")
    time.Sleep(5 * time.Second)
    fmt.Println("main end")
}

