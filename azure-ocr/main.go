package main

import (
	"bytes"
	"encoding/csv"
	"encoding/json"
	"fmt"
	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/canvas"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/widget"
	"github.com/fogleman/gg"
	"github.com/urfave/cli/v2"
	"image"
	_ "image/jpeg"
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
	r, err2 := getOcr(filename)
	if err2 != nil {
		return nil, err2
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

func getOcr(filename string) (*AiVisionResponse, error) {
	client := NewAiVisionClient("https://chinese-learning-jorjao81.cognitiveservices.azure.com/", os.Getenv("AZURE_VISION_API_KEY"))

	return client.Analyse(filename)
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
	app := &cli.App{
		Name:  "cyberpunk-ocr",
		Usage: "parse chinese text in Cyberpunk 2077 screenshots",
		Commands: []*cli.Command{
			{
				Name:    "generate-frame-training",
				Aliases: []string{""},
				Usage:   "generates frame training data",
				Action: func(cCtx *cli.Context) error {
					return generateFrameTrainingData(cCtx.Args().Slice())
				},
			},
			{
				Name:    "annotate",
				Aliases: []string{""},
				Usage:   "annotate data",
				Action: func(cCtx *cli.Context) error {
					return annotate(cCtx.Args().Slice())
				},
			},
		},
	}

	if err := app.Run(os.Args); err != nil {
		log.Fatal(err)
	}
}

func annotate(args []string) error {
	filename := args[0]

	a := app.New()
	w := a.NewWindow("Hello")

	var vBox *fyne.Container

	line := 0
	fileIndex := 0

	screenshot, lines := getScreenshot(filename)
	annotation, _ := os.Create(fmt.Sprintf("%v.annotation", filename))

	moveToNext := func() {
		if line >= len(lines) {
			fileIndex++
			line = 0
			if fileIndex >= len(args) {
				w.Close()
			} else {
				filename = args[fileIndex]
				screenshot, lines = getScreenshot(filename)
			}
		}
		marked2 := markImage(screenshot, lines[line].BoundingBox)
		img2 := canvas.NewImageFromImage(marked2)
		img2.FillMode = canvas.ImageFillContain
		img2.SetMinSize(fyne.NewSize(800, 600))
		vBox.Objects[0] = img2
		vBox.Refresh()
		line++

	}

	hBox := container.NewHBox(
		widget.NewButton("Subtitle", func() {
			fmt.Printf("%v\t%v\n", "subtitle", lines[line-1].Content)
			annotation.WriteString(fmt.Sprintf("%v\t%v\n", "subtitle", lines[line-1].Content))

			moveToNext()
		}),
		widget.NewButton("Mission goal", func() {
			fmt.Printf("%v\t%v\n", "mission", lines[line-1].Content)
			annotation.WriteString(fmt.Sprintf("%v\t%v\n", "mission", lines[line-1].Content))

			moveToNext()
		}),
		widget.NewButton("Other", func() {
			fmt.Printf("%v\t%v\n", "other", lines[line-1].Content)
			annotation.WriteString(fmt.Sprintf("%v\t%v\n", "other", lines[line-1].Content))

			moveToNext()
		}),
		widget.NewButton("Terminal", func() {
			fmt.Printf("%v\t%v\n", "terminal", lines[line-1].Content)
			annotation.WriteString(fmt.Sprintf("%v\t%v\n", "terminal", lines[line-1].Content))

			moveToNext()
		}),
		widget.NewButton("Information", func() {
			fmt.Printf("%v\t%v\n", "information", lines[line-1].Content)
			annotation.WriteString(fmt.Sprintf("%v\t%v\n", "information", lines[line-1].Content))

			moveToNext()
		}),
	)

	vBox = container.NewVBox(
		widget.NewLabel("bla"),
		hBox,
	)
	moveToNext()

	w.SetContent(vBox)

	w.ShowAndRun()

	return nil

}

func getScreenshot(filename string) (image.Image, []readResultLines) {
	reader, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}
	defer reader.Close()

	screenshot, err := gg.LoadImage(filename)

	f, err := getOcr(filename)
	lines := f.ReadResult.Pages[0].Lines

	return screenshot, lines
}

func markImage(screenshot image.Image, bbox BoundingBox) image.Image {
	dc := gg.NewContextForImage(screenshot)

	dc.SetRGB255(0, 255, 0)
	dc.SetLineWidth(5)

	dc.DrawLine(bbox[0], bbox[1], bbox[2], bbox[3])
	dc.DrawLine(bbox[4], bbox[5], bbox[6], bbox[7])
	dc.Stroke()

	marked := dc.Image()
	return marked
}

func generateFrameTrainingData(args []string) error {
	w := csv.NewWriter(os.Stdout)

	for _, filename := range args {
		f, err := parseScreenshot(filename)
		if err != nil {
			return err
		}

		t := "bla"
		if f.frameType == Normal {
			t = "normal"
		}

		w.Write([]string{filename, t})
	}
	w.Flush()
	return nil
}

func main_old() {
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
