chapter\_08\_project
-----------------------

从 chapter\_03\_pkg 迁移过来，做一下包规范的尝试

```
source gopath

go run src/project_main/main.go
```

### import

1. 包中不能有main方法。
2. 同文件夹中可以直接用方法名调用。
3. main函数建议放在package main里
4. main不能调用同个目录下的其它文件中的方法。

### unittest

`cd src/test`
##### 功能测试 执行全部
`go test`
##### 执行单个测试文件
`go test -v unit1_test.go`
##### 测试单个方法
`go test -v -test.run TestMain2`

##### 性能测试
`go test -v bench_test.go -test.bench=".*"`


http://www.cnblogs.com/yjf512/archive/2013/01/18/2865915.html
