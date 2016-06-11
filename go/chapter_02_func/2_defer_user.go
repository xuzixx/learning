package main

import "fmt"
import "time"

/*
    当函数执行到最后时，这些defer语句会按照**逆序**执行，最后该函数返回
    Done !
    lily Closed !!!
    jack Closed !!!

    u := new(User) 
    u.username = "xxxx"
    和
    &User{"xxxx"} 等价
*/

type User struct {
        username string
}

func (this *User) Close() {
        fmt.Println(this.username, "Closed !!!")
}

func main() {
        u1 := &User{"jack"}
        defer u1.Close()
        u2 := &User{"lily"}
        defer u2.Close()

        var u3 User
        println("init u3")
        println(u3.username)
        u3.username = "u3 test"
        u3.Close()

        u4 := new(User)
        println("init u4")
        u4.username = "u4 test"
        u4.Close()

        time.Sleep(2 * time.Second)

        fmt.Println("Done !")

}
