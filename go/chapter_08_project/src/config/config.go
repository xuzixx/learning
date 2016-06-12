package config

func WrapFunc() {
	println("in wrap")
	configToolFunc()
}

func LoadConfig() {
	println("LoadConfig")
}

var CONFIG_INT []int
