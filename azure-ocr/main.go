package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"math"
	"net/http"
	"os"
)

type StringType int64
type BoundingBox []float64

const (
	Dialog StringType = iota
	Mission
	Choice
	Other
)

type (
	readResultLines struct {
		Content     string      `json:"content"`
		BoundingBox BoundingBox `json:"boundingBox"`
	}
	//readResultWords struct {
	//	Content    string  `json:"content""`
	//	Confidence float32 `json:"confidence"`
	//}
	readResultPage struct {
		Lines []readResultLines `json:"lines"`
	}
	aiVisionReadResult struct {
		Pages []readResultPage `json:"pages"`
	}
	aiVisionResponse struct {
		ReadResult aiVisionReadResult `json:"readResult"`
	}
)

func abs(n int) int {
	if n < 0 {
		return -n
	}
	return n
}

func stringType(box BoundingBox) StringType {
	if math.Abs(box[0]-3044) < 100 && box[1] > 700 && box[7] < 1300 {
		return Mission
	}
	if math.Abs(box[1]-2000) < 200 && math.Abs(box[0]-1000) < 200 {
		return Dialog
	}
	if math.Abs(box[1]-1500) < 200 && box[0] > 1000 && box[2] < 3000 {
		return Choice
	}
	return Other
}

//[
//1823,
//1585,
//2028,
//1589,
//2027,
//1638,
//1822,
//1634
//]

func main() {
	client := &http.Client{}

	ENDPOINT := "https://learn-zh-jorjao81.cognitiveservices.azure.com"
	url := fmt.Sprintf("%s/computervision/imageanalysis:analyze?features=read&model-version=latest&language=zh-Hans&api-version=2023-02-01-preview", ENDPOINT)

	filename := os.Args[1]
	image, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}
	raw, _ := io.ReadAll(image)
	reqBody := bytes.NewReader(raw)

	request, _ := http.NewRequest("POST", url, reqBody)
	request.Header.Add("Ocp-Apim-Subscription-Key", os.Getenv("AZURE_VISION_API_KEY"))
	request.Header.Add("Content-Type", "application/octet-stream")

	resp, err := client.Do(request)
	if err != nil {
		log.Fatal(err)
	}
	defer resp.Body.Close()

	var r aiVisionResponse
	err = json.NewDecoder(resp.Body).Decode(&r)

	if err != nil {
		log.Fatal(err)
	}

	dialogs := make([]readResultLines, 0)
	mission := make([]readResultLines, 0)
	choices := make([]readResultLines, 0)

	for _, page := range r.ReadResult.Pages {
		for _, line := range page.Lines {
			switch stringType(line.BoundingBox) {
			case Dialog:
				dialogs = append(dialogs, line)
				fmt.Printf("DIALOG:  %s\n", line.Content)
				break
			case Mission:
				mission = append(mission, line)
				fmt.Printf("MISSION: %s\n", line.Content)
				break
			case Choice:
				choices = append(choices, line)
				fmt.Printf("CHOICE:  %s\n", line.Content)
				break
			case Other:
				//fmt.Printf("OTHER:   %s\n", line.Content)
				break
			}
		}
	}

	fmt.Println("\n\nMISSION")
	for _, line := range mission {
		fmt.Println(line.Content)
	}

	fmt.Println("\n\nDIALOG")
	for _, line := range dialogs {
		fmt.Println(line.Content)
	}

	fmt.Println("\n\nCHOICES")
	for _, line := range choices {
		fmt.Println(line.Content)
	}

}
