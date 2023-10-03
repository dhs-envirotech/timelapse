package main

import (
	"fmt"
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
	// Other setup
	cwd, err := os.Getwd()
	if err != nil {
		log.Fatal(err)
	}

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

	// API
	api := e.Group("/api")

	// Media
	// api.GET("/pictures", func(c echo.Context) error {
	// 	names := readMedia("pictures")
	// 	return c.JSON(200, names)
	// })

	// api.GET("/videos", func(c echo.Context) error {
	// 	names := readMedia("videos")
	// 	return c.JSON(200, names)
	// })

	// Settings
	api.GET("/settings", func(c echo.Context) error {
		var settings Settings

		settings.Cron = readCron()

		return c.JSON(200, settings)
	})

	api.POST("/settings", func(c echo.Context) error {
		fmt.Println(c.Request().Header.Get("Content-Type"))
		var settings Settings
		if err := c.Bind(&settings); err != nil {
			return err
		}

		if settings.Cron != "" {
			writeCron(settings.Cron, cwd)
		}

		return c.JSON(200, settings)
	})

	e.Logger.Fatal(e.Start(":3000"))
}
