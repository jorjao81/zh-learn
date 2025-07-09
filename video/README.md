# Chinese Gameplay Processor

Extract Chinese dialogue segments from gameplay videos automatically. This tool identifies Chinese speech in your recordings and creates a cleaned-up video containing only the story/dialogue portions.

## Features

- **Automatic Chinese Speech Detection**: Uses OpenAI Whisper to identify Chinese dialogue
- **Voice Activity Detection**: Filters out silent periods and background noise
- **Smart Segment Merging**: Combines nearby dialogue segments to avoid choppy cuts
- **Local Processing**: Everything runs on your machine (no cloud services required)
- **Multiple Quality Options**: Choose between speed and accuracy with different Whisper models

## Installation

### Prerequisites

1. **Python 3.8+** - Check with `python --version`
2. **FFmpeg** - Required for video processing
   - **macOS**: `brew install ffmpeg`
   - **Windows**: Download from https://ffmpeg.org/download.html
   - **Linux**: `sudo apt install ffmpeg` (Ubuntu/Debian)

### Install Dependencies

```bash
pip install -r requirements.txt
```

Note: First run will download the Whisper model (can take a few minutes).

## Usage

### Basic Usage

```bash
python chinese_gameplay_processor.py input_video.mp4 output_story.mp4
```

### Advanced Options

```bash
python chinese_gameplay_processor.py input_video.mp4 output_story.mp4 \
  --model small \
  --min-gap 3.0 \
  --vad-aggressiveness 2
```

### Parameters

- `--model`: Whisper model size
  - `tiny`: Fastest, least accurate
  - `base`: Good balance (default)
  - `small`: Better accuracy
  - `medium`: High accuracy
  - `large`: Best accuracy, slowest

- `--min-gap`: Minimum gap between segments before merging (seconds)
  - Default: 2.0 seconds
  - Higher values = fewer, longer segments

- `--vad-aggressiveness`: Voice activity detection sensitivity (0-3)
  - 0: Least aggressive (keeps more audio)
  - 3: Most aggressive (default, filters more background noise)

## Example Output

```
Loading Whisper model: base
Extracting audio from video...
Analyzing voice activity...
Transcribing audio and detecting Chinese...

Found 15 Chinese segments:
   1.   45.3s-  48.7s ( 3.4s): 你好，欢迎来到这个世界
   2.   52.1s-  55.8s ( 3.7s): 这是你的第一个任务
   3.   98.2s- 102.5s ( 4.3s): 恭喜你完成了任务
   ...

Total Chinese content: 67.3 seconds

Merging segments with gaps < 2.0s...
After merging: 8 segments, 67.3 seconds

Extracting 8 video segments...
Concatenating segments...
Processed video saved to: output_story.mp4
```

## Performance Tips

### Speed vs Quality

- **Fast Processing**: Use `--model tiny` for quick results
- **Best Quality**: Use `--model large` for highest accuracy
- **Balanced**: Default `base` model works well for most cases

### Hardware Requirements

- **CPU**: Any modern processor works
- **RAM**: 4GB+ recommended for larger models
- **GPU**: CUDA GPU will significantly speed up processing (optional)
- **Storage**: ~1GB for Whisper models

### Processing Times (Approximate)

For 1 hour of video:
- `tiny` model: ~5 minutes
- `base` model: ~10 minutes  
- `large` model: ~30 minutes

## Troubleshooting

### Common Issues

**"No Chinese speech detected"**
- Try a different Whisper model (`--model small` or `--model medium`)
- Reduce VAD aggressiveness (`--vad-aggressiveness 1`)
- Check if audio quality is clear

**"FFmpeg not found"**
- Install FFmpeg (see Prerequisites)
- Ensure FFmpeg is in your system PATH

**Out of memory errors**
- Use a smaller model (`--model tiny` or `--model base`)
- Process shorter video segments

**Choppy output video**
- Increase `--min-gap` to merge more segments
- Try `--min-gap 5.0` for longer continuous segments

### File Format Support

**Supported Input Formats**: MP4, AVI, MOV, MKV, WMV, FLV
**Output Format**: MP4 (H.264 codec)

## Examples

### Process a 2-hour gameplay session
```bash
python chinese_gameplay_processor.py "Long RPG Session.mp4" "Story Only.mp4" --model medium --min-gap 3.0
```

### Quick processing for testing
```bash
python chinese_gameplay_processor.py gameplay.mp4 test_output.mp4 --model tiny
```

### High-quality processing
```bash
python chinese_gameplay_processor.py gameplay.mp4 final_output.mp4 --model large --min-gap 1.0
```

## How It Works

1. **Audio Extraction**: Extracts audio track from video
2. **Voice Activity Detection**: Identifies speech segments using WebRTC VAD
3. **Speech Recognition**: Transcribes audio using OpenAI Whisper
4. **Chinese Detection**: Filters segments containing Chinese characters
5. **Segment Merging**: Combines nearby segments to avoid choppy cuts
6. **Video Assembly**: Extracts and concatenates matching video segments

## License

MIT License - Feel free to modify and use for personal projects.