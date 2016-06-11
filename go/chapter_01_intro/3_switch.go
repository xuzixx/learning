package main

/*
    switch, default, fallthrough

    https://play.golang.org/p/LySjbnt53q
*/

func unhex(c byte) byte {
    // switch 不接变量
    switch {
        case '0'<=c && c<='9':
            return c - '0'
        case 'a'<=c && c<='f':
            return c - 'a' + 10
        case 'A'<=c && c<='F':
            return c - 'A' + 10
    }
    return 0
}

func switch_default(i int) {
    // switch + i
    switch i {
        case 1:
            println("in 1")
        case 2:
            println("in 2")
        case 3:
            println("in 3")
        default:
            println("not in 1,2,3")
    }
}

func switch_fallthrough(i int){
    // switch + i
    switch i {
        case 1:
            println("in 1")
        case 2:
            println("in 2")
            fallthrough
        case 3:
            println("in 3")
            fallthrough
        case 4:
            println("in 4")
        default:
            println("not in 1,2,3")
    }

}

func main() {
    println("<<<< part 1 <<<<<<<<<<<<<<<<<<<<<<<<")
    println(unhex('a'))
    println(unhex('>'))

    println("<<<< part 2 <<<<<<<<<<<<<<<<<<<<<<<<")
    switch_default(1)
    switch_default(4)

    println("<<<< part 3 <<<<<<<<<<<<<<<<<<<<<<<<")
    /*
        <<<< part 3 <<<<<<<<<<<<<<<<<<<<<<<<
        in 1
        not in 1,2,3
        in 3
        in 4
    */
    switch_fallthrough(1)
    switch_fallthrough(5)
    switch_fallthrough(3)

}
