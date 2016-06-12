package main

import (
	"bufio"
	"io"
	"os"
)

func readLine(filename string) {
	f, _ := os.Open(filename)
	defer f.Close()

	r := bufio.NewReader(f)

	postfix := []byte{' ', '-', '\n'}
	w := bufio.NewWriter(os.Stdout)
	defer w.Flush()

	for {
		s, _, ok := r.ReadLine()
		if ok == io.EOF {
			break
		}
		w.Write(s)
		w.Write(postfix)
	}
}

func readBuf(filename string) {
	buf := make([]byte, 1024)
	f, _ := os.Open(filename)
	defer f.Close()

	r := bufio.NewReader(f)
	w := bufio.NewWriter(os.Stdout)
	defer w.Flush()

	for {
		n, _ := r.Read(buf)
		if n == 0 {
			break
		}
		w.Write(buf[:n])
	}
}

func main() {
	//filename := "/etc/password"
	filename := "one_line.txt"
	readBuf(filename)
	println("------------------------------")
	readLine(filename)
}
