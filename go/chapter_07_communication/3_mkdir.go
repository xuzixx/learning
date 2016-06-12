package main

import (
	"fmt"
	"os"
)

func mkdir(dir string) {
	if _, e := os.Stat(dir); e != nil {
		os.Mkdir(dir, 0755)
	} else {
		fmt.Printf("%#v", e)
	}
}

func main() {
	mkdir("test_dir")
}
