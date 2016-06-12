package test

import (
	"fmt"
	"testing"
	"time"
)

/*
	b.StopTimer() //调用该函数停止压力测试的时间计数
	b.StartTimer() //重新开始时间
	https://github.com/astaxie/build-web-application-with-golang/blob/master/zh/11.3.md
*/
func BenchmarkMain(b *testing.B) {
	fmt.Println("<<<<<benchmark main <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
	time.Sleep(1 * time.Second)
	for i := 0; i < b.N; i++ {
		// TODO 测试性能的函数
	}
}
