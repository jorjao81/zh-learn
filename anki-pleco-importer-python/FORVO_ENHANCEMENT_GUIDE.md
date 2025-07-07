# 🎵 Enhanced Forvo Integration Guide

## Overview

The Forvo integration has been significantly enhanced to provide intelligent pronunciation selection based on user preferences and quality metrics.

## Key Features

### 🎯 **Smart User Selection**
- **Preferred Users**: Define an ordered list of trusted Forvo users
- **Auto-Selection**: Automatically picks the best pronunciation from preferred users
- **Fallback Logic**: If no preferred users found, intelligently selects or prompts for choice

### 🔍 **Interactive Selection**
- **Detailed User Info**: Shows username, gender, country, vote counts, and ratings
- **Quality Indicators**: Star ratings and vote counts help you choose the best pronunciation
- **Skip Option**: Option to skip if no pronunciation meets your standards

### 📁 **Enhanced Caching**
- **Username-Based Filenames**: Cache files include username for easy identification
- **Smart Cache Lookup**: Finds existing pronunciations regardless of username
- **Organized Storage**: Better file organization in the audio cache

## Configuration

### Basic Configuration
```json
{
  "audio": {
    "forvo": {
      "api_key": "your_forvo_api_key",
      "preferred_users": [
        "liufeimagic",
        "mouyao", 
        "darren8221",
        "learnxuexi",
        "Vincent930209"
      ],
      "download_all_when_no_preferred": true,
      "interactive_selection": true
    }
  }
}
```

### Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| `preferred_users` | `[]` | Ordered list of preferred Forvo usernames |
| `download_all_when_no_preferred` | `true` | Download all options when no preferred users found |
| `interactive_selection` | `true` | Enable interactive selection prompt |

## Usage Examples

### 1. Preferred User Auto-Selection
```bash
# With preferred users configured, best pronunciation is auto-selected
FORVO_API_KEY="your_key" anki-pleco-importer input.tsv --audio --audio-config config.json
```

**Result:**
```
Found preferred user 'liufeimagic' for '你好'
Selected pronunciation by: liufeimagic
```

### 2. Interactive Selection
When no preferred users are found:

```
🎵 学习 - Found 5 pronunciations:

 1. wtj232010 (♂, United States) - 3 votes, rating: 3.0 ⭐⭐⭐
 2. witenglish (♂, China) - 3 votes, rating: -3.0 
 3. g03524taiwan (♀, Taiwan) - 0 votes, rating: 0.0 
 4. hellolovey (♀, China) - 0 votes, rating: 0.0 
 5. wangdream (♀, China) - 3 votes, rating: 3.0 ⭐⭐⭐ [PREFERRED]

Select pronunciation (1-5, or 's' to skip): 5
```

### 3. Non-Interactive Mode
```json
{
  "forvo": {
    "interactive_selection": false,
    "download_all_when_no_preferred": false
  }
}
```
Falls back to highest-rated pronunciation automatically.

## Recommended Preferred Users

Based on quality and consistency for Chinese pronunciations:

### Top Tier (Native Speakers, High Quality)
- **liufeimagic** - Female, China - Consistently high quality
- **mouyao** - Female, China - Clear pronunciation  
- **darren8221** - Male, Taiwan - Good for traditional variants
- **learnxuexi** - Male, China - Educational focus

### Second Tier (Good Quality)
- **Vincent930209** - Male, China - Frequent contributor
- **milk1127** - Female, Taiwan - Good for regional variants
- **sundayright** - Male, Taiwan - Clear pronunciation

## File Organization

### Cache File Format
```
audio_cache/
├── forvo_liufeimagic_7eca689f0d3389d9dea66ae112e5cfd7.mp3
├── forvo_mouyao_b213aa8f17e867c7548e8544d9652d85.mp3
└── forvo_darren8221_dda9e0a0a0bf74efee003346144f740d.mp3
```

### Benefits
- **Easy Identification**: Quickly see which user provided each pronunciation
- **Quality Tracking**: Monitor which users provide the best audio
- **Backup Options**: Multiple pronunciations available for comparison

## Advanced Usage

### Quality Assessment
The system considers multiple factors when selecting pronunciations:

1. **Preferred User Priority**: Your configured user list takes precedence
2. **Vote Counts**: Higher positive votes indicate better quality
3. **Rating Scores**: Star ratings show community approval
4. **User Demographics**: Native speakers often preferred

### Interactive Selection Tips
- **Check User Info**: Look for native speakers (China, Taiwan)
- **Consider Ratings**: 3+ stars usually indicate good quality
- **Vote Counts**: Higher vote counts suggest more community validation
- **Skip Low Quality**: Don't hesitate to skip poor pronunciations

### Batch Processing
For large vocabulary lists:
```bash
# Process with automatic selection (faster)
anki-pleco-importer large_list.tsv --audio --audio-config non_interactive_config.json

# Process with manual quality control (slower but higher quality)
anki-pleco-importer large_list.tsv --audio --audio-config interactive_config.json
```

## Troubleshooting

### No Preferred Users Found
```
No preferred users found for '罕见词汇', using highest-rated: random_user
```
**Solution**: Add more diverse users to your preferred list or enable interactive selection.

### Interactive Selection Not Working
**Check**: Ensure `interactive_selection: true` in your configuration.

### Cache Not Using Usernames
**Check**: Verify you're using the latest version with enhanced caching.

## Best Practices

1. **Curate Your Preferred Users**: Regularly review and update your preferred user list
2. **Quality Over Quantity**: Better to have fewer high-quality preferred users
3. **Regional Preferences**: Include users from different regions for variant pronunciations
4. **Regular Review**: Periodically check new pronunciations and update preferences

## Migration from Old System

If you have existing Forvo cache files, they will continue to work. New pronunciations will use the enhanced username-based format automatically.

The system will automatically detect and use existing cache files while generating new ones with improved naming.