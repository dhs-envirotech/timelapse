package main

import (
	"fmt"
	"log"
	"os"

	"github.com/labstack/echo"
)

func initializeAPI(api *echo.Group) {
	// Other setup
	cwd, err := os.Getwd()
	if err != nil {
		log.Fatal(err)
	}

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
}
