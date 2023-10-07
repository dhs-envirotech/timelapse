package main

import (
	"log"
	"os"

	"github.com/labstack/echo"
	"github.com/labstack/echo/middleware"
)

const explorerName = "media"

func readMedia(folderName string) []string {
	folder, err := os.Open(explorerName + "/" + folderName)
	if err != nil {
		log.Fatal(err)
	}

	files, err := folder.Readdir(0)
	if err != nil {
		log.Fatal(err)
	}

	names := []string{}
	for _, file := range files {
		names = append(names, file.Name())
	}

	return names
}
func main() {

	// HTTP Server
	e := echo.New()
	e.Use(middleware.Logger())

	// HTML File Explorer
	explorerRoute := e.Group("/" + explorerName)
	explorerRoute.Use(middleware.StaticWithConfig(middleware.StaticConfig{
		Root:   explorerName,
		Browse: true,
	}))

	// Patch pictures trailing slash bug - default functions don't work
	const redirectUrl = "/" + explorerName + "/"
	e.GET("/"+explorerName, func(c echo.Context) error {
		return c.Redirect(301, redirectUrl)
	})

	// Website
	e.Static("/", "web")

	e.Logger.Fatal(e.Start(":3000"))
}
