package main

import (
	"fmt"
	"log"
	"os"
	"strings"

	"github.com/shakeel/pdf2txt/pdf"
)

func calmDown() {
	err := recover()
	if err != nil {
		log.Fatal(err)
	}
}

func main() {
	defer calmDown()
	if len(os.Args) != 2 {
		log.Fatal("Incorrect usage.")
	}
	file := os.Args[1]
	reader, err := pdf.Open(file)
	if err != nil {
		log.Fatal("err opening sample.pdf")
	}
	out := strings.Replace(file, ".pdf", ".txt", 1)
	writer, err := os.Create(out)
	if err != nil {
		log.Fatal("err creating sample.txt")
	}

	var b strings.Builder
	for i := 1; i <= reader.NumPage(); i++ {
		// y coordinate of page
		y := 0.0
		for _, t := range reader.Page(i).Content().Text {
			// check if we are on new line
			if t.Y != y {
				y = t.Y
				b.WriteString("\n")
			}
			b.WriteString(t.S)
		}
	}
	fmt.Fprintf(writer, "%v\n", b.String())
	writer.Close()
}
