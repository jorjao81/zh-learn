package main

import (
	"github.com/stretchr/testify/mock"
	"io"
	"net/http"
	"strings"
	"testing"
)
import "github.com/stretchr/testify/assert"

func normalize(s []string) []string {
	normalized := make([]string, len(s))
	for i, v := range s {
		normalized[i] = strings.TrimRight(strings.ReplaceAll(v, " ", ""), "。")
	}
	return normalized
}

func TestDialog(t *testing.T) {
	filename := "./tests/SHARE_20230617_0742151.jpeg"
	f, err := parseScreenshot(filename)

	assert.Nil(t, err)

	assert.Equal(t, []string{"T-Bug:不错,我就说这你不在话下"}, normalize(f.GetDialogs()))
}

type MockHttp struct {
	mock.Mock
}

func TestChoices(t *testing.T) {
	filename := "./tests/SHARE_20230617_0727300.jpeg"

	f, err := parseScreenshot(filename)

	assert.Nil(t, err)

	assert.Equal(t, []string{"是法兰克福的事吗?", "我没时间弄这个"}, f.GetChoices())
}

func TestChoices2(t *testing.T) {
	filename := "./tests/SHARE_20230617_0728521.jpeg"
	f, err := parseScreenshot(filename)

	assert.Nil(t, err)

	assert.Equal(t, []string{"[坐下]见到你我也很高兴"}, normalize(f.GetChoices()))
}

func TestChoices3(t *testing.T) {
	filename := "./tests/SHARE_20230617_0729232.jpeg"
	f, err := parseScreenshot(filename)

	assert.Nil(t, err)

	assert.Equal(t, normalize([]string{"[递过数据芯]你瞅一眼。", "这件事你知我知"}), normalize(f.GetChoices()))
}

func (m *MockHttp) Do(req *http.Request) (*http.Response, error) {
	args := m.Called(req)
	return args.Get(0).(*http.Response), args.Error(1)
}

func TestError(t *testing.T) {
	mockedHttp := new(MockHttp)
	response := &http.Response{
		StatusCode: 429,
		Body:       io.NopCloser(strings.NewReader("{\"error\": {\"code\": \"429\",\"message\": \"some error msg\"}}")),
	}
	mockedHttp.On("Do", mock.Anything).Return(response, nil)

	client := AiVisionClient{
		httpClient: mockedHttp,
	}

	r, err := client.Analyse("tests/error.jpeg")
	assert.Nil(t, r)
	assert.EqualError(t, err, "some error msg")
}
