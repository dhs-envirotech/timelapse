package main

import (
	"fmt"
	"os"
	"strings"
)

type Settings struct {
	Cron string `json:"cron"`
}

const cronFilePath = "/Users/humanfriend22/Downloads/raspberry-pi-timelapse"

func readCron() string {
	bytes, err := os.ReadFile(cronFilePath)
	if err != nil {
		panic(err)
	}

	str := strings.Split(string(bytes), " ")[0]

	return str
}

func writeCron(cronExpression string, cwd string) {
	// Open the file for writing
	f, err := os.Create(cronFilePath)
	if err != nil {
		panic(err)
	}

	// Write the contents to the file
	_, err = f.Write([]byte(
		fmt.Sprintf("%s bash %s/scripts/picture.sh %s/media/pictures", cronExpression, cwd, cwd) +
			"\n" +
			"",
	))
	if err != nil {
		panic(err)
	}

	// Close the file
	err = f.Close()
	if err != nil {
		panic(err)
	}
}
