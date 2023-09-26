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
	"strings"
	"unicode"
)

type StringType int64
type FrameType int64
type BoundingBox []float64

const (
	Dialog StringType = iota
	Mission
	Choice
	Other
)
const (
	Console FrameType = iota
	Normal
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
	AiVisionResponse struct {
		ReadResult aiVisionReadResult `json:"readResult"`
	}
)

func abs(n int) int {
	if n < 0 {
		return -n
	}
	return n
}

func isCommonName(s string) bool {
	commonNames := map[string]bool{
		"哈里": true,
		"杰克": true,
	}
	return commonNames[s]
}

func containsChinese(s string) bool {
	for _, runeValue := range s {
		if unicode.Is(unicode.Han, runeValue) {
			return true
		}
	}
	return false
}

func commonConfusion(s string) bool {
	if strings.Contains(s, "口") { // confusion with PS5 square button
		return true
	}
	return false
}

func stringType(line readResultLines) StringType {
	box := line.BoundingBox
	if math.Abs(box[0]-3044) < 100 && box[1] > 700 && box[7] < 1300 {
		return Mission
	}
	if math.Abs(box[1]-1500) < 200 && box[0] > 1000 && box[2] < 3000 {
		if !isCommonName(line.Content) && containsChinese(line.Content) && !commonConfusion(line.Content) {
			return Choice
		}
	}
	if inside(box, 900, 1700, 2100, 400) {
		return Dialog
	}
	return Other
}

type Frame struct {
	dialogs   []readResultLines
	mission   []readResultLines
	choices   []readResultLines
	other     []readResultLines
	frameType FrameType
}

func (f Frame) GetDialogs() []string {
	dialogs := make([]string, len(f.dialogs))

	for i, d := range f.dialogs {
		dialogs[i] = d.Content
	}
	return dialogs
}

func (f Frame) GetChoices() []string {
	choices := make([]string, len(f.choices))

	for i, d := range f.choices {
		choices[i] = d.Content
	}
	return choices
}

func NewFrame() *Frame {
	return &Frame{
		dialogs: make([]readResultLines, 0),
		mission: make([]readResultLines, 0),
		choices: make([]readResultLines, 0),
		other:   make([]readResultLines, 0),
	}
}

func insideCoordinates(box BoundingBox, xTopLeft float64, yTopLeft float64,
	xBottomRight float64, yBottomRight float64) bool {
	return box[0] > xTopLeft && box[6] > xTopLeft &&
		box[2] < xBottomRight && box[4] < xBottomRight &&
		box[1] > yTopLeft && box[3] > yTopLeft &&
		box[5] < yBottomRight && box[7] < yBottomRight
}
func inside(box BoundingBox, xTopLeft float64, yTopLeft float64,
	xDelta float64, yDelta float64) bool {
	return insideCoordinates(box, xTopLeft, yTopLeft, xTopLeft+xDelta, yTopLeft+yDelta)
}

func findFrameType(r *AiVisionResponse) FrameType {
	for _, page := range r.ReadResult.Pages {
		for _, line := range page.Lines {
			if line.Content == "消息" {
				if inside(line.BoundingBox, 693, 435, 150, 78) {
					return Console
				}
			}
		}
	}
	return Normal
}

// [716.0,450.0,801.0,447.0,804.0,497.0,720.0,499.0]
func parseScreenshot(filename string) (*Frame, error) {
	client := NewAiVisionClient("https://chinese-learning-jorjao81.cognitiveservices.azure.com/", os.Getenv("AZURE_VISION_API_KEY"))

	r, err := client.Analyse(filename)
	if err != nil {
		return nil, err
	}

	f := NewFrame()
	f.frameType = findFrameType(r)

	for _, page := range r.ReadResult.Pages {
		for _, line := range page.Lines {
			switch stringType(line) {
			case Dialog:
				f.dialogs = append(f.dialogs, line)
				break
			case Mission:
				f.mission = append(f.mission, line)
				break
			case Choice:
				f.choices = append(f.choices, line)
				break
			case Other:
				if containsChinese(line.Content) {
					f.other = append(f.other, line)
				}
				break
			}
		}
	}

	return f, nil
}

type errorJson struct {
	Code    string `json:"code"`
	Message string `json:"message"`
}

type azureError struct {
	Error errorJson `json:"error"`
}

type HttpClientInterface interface {
	Do(req *http.Request) (*http.Response, error)
}

type AiVisionClient struct {
	httpClient      HttpClientInterface
	endpoint        string
	subscriptionKey string
}

func NewAiVisionClient(endpoint string, subscriptionKey string) *AiVisionClient {
	client := AiVisionClient{
		httpClient:      &http.Client{},
		endpoint:        endpoint,
		subscriptionKey: subscriptionKey,
	}

	return &client
}

func (c *AiVisionClient) Analyse(filename string) (*AiVisionResponse, error) {
	url := fmt.Sprintf("%s/computervision/imageanalysis:analyze?features=read&model-version=latest&language=zh-Hans&api-version=2023-02-01-preview", c.endpoint)

	jsonFilename := fmt.Sprintf("%s.json", filename)
	var responseBytes []byte
	if _, err := os.Stat(jsonFilename); err != nil {

		image, err := os.Open(filename)
		if err != nil {
			log.Fatal(err)
		}
		raw, _ := io.ReadAll(image)
		reqBody := bytes.NewReader(raw)

		request, _ := http.NewRequest("POST", url, reqBody)
		request.Header.Add("Ocp-Apim-Subscription-Key", c.subscriptionKey)
		request.Header.Add("Content-Type", "application/octet-stream")

		resp, err := c.httpClient.Do(request)
		if err != nil {
			return nil, err
		}
		defer resp.Body.Close()

		responseBytes, _ = io.ReadAll(resp.Body)

		if resp.StatusCode != 200 {
			var errorMessage azureError
			err := json.NewDecoder(bytes.NewReader(responseBytes)).Decode(&errorMessage)
			if err != nil {
				return nil, err
			}
			return nil, fmt.Errorf(errorMessage.Error.Message)
		}

		err = os.WriteFile(jsonFilename, responseBytes, 0644)
		if err != nil {
			return nil, err
		}
	} else {
		responseBytes, err = os.ReadFile(jsonFilename)
		if err != nil {
			log.Fatal(err)
		}
	}

	var r AiVisionResponse
	err := json.NewDecoder(bytes.NewReader(responseBytes)).Decode(&r)
	if err != nil {
		return nil, err
	}
	return &r, nil
}

func main() {
	dialogSeen := make(map[string]bool)
	//choicesSeen := make(map[string]bool)
	//missionSeen := make(map[string]bool)
	//otherSeen := make(map[string]bool)

	os.Getenv("AZURE_VISION_API_KEY")

	for _, filename := range os.Args[1:] {
		if filename == "--" {
			continue
		}

		f, err := parseScreenshot(filename)
		if err != nil {
			panic(err)
		}

		if f.frameType == Normal {
			for _, line := range f.dialogs {
				if !dialogSeen[line.Content] {
					dialogSeen[line.Content] = true
					fmt.Println(line.Content)
				}
			}

			//fmt.Println("\n\nMISSION")
			//for _, line := range f.mission {
			//	fmt.Println(line.Content)
			//}
			//
			//for _, line := range f.choices {
			//	if !choicesSeen[line.Content] {
			//		choicesSeen[line.Content] = true
			//		fmt.Printf("CHOICE: %s\n", line.Content)
			//	}
			//}
			//
			//for _, line := range f.other {
			//	if !otherSeen[line.Content] {
			//		otherSeen[line.Content] = true
			//		fmt.Printf("CHOICE: %s\n", line.Content)
			//	}
			//}
		}

	}

}
