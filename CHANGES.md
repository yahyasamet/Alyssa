# TTS Service Migration: OpenAI → Google Gemini

## Summary of Changes

This document outlines the migration from OpenAI's TTS service to Google Gemini's TTS service.

## Files Modified

### 1. `backend/requirements.txt`
- **Removed**: `openai`
- **Added**: `google-genai`

### 2. `backend/app/audio/tts.py`
- **Complete rewrite** of the `TTSService` class
- **New imports**: 
  - `from google import genai`
  - `from google.genai import types`
  - `import mimetypes`
  - `import struct`
- **New methods**:
  - `_convert_to_wav()`: Converts audio data to WAV format
  - `_parse_audio_mime_type()`: Parses audio MIME type parameters
- **Updated methods**:
  - `generate_speech()`: Now uses Google Gemini streaming TTS
  - `save_audio_file()`: Now handles WAV files instead of MP3
- **Voice changes**: Default voice changed from "achernar" to "Fenrir"

### 3. `backend/app/routes/api.py`
- **Updated**: File extensions from `.mp3` to `.wav`
- **Updated**: Media type from `audio/mpeg` to `audio/wav`
- **Updated**: Default voice in `TTSRequest` model from "achernar" to "Fenrir"

### 4. `README.md`
- **Updated**: Tech stack section to reflect Google Gemini TTS
- **Updated**: Environment variables section
- **Updated**: Setup instructions

### 5. New Files Created
- `backend/.env.example`: Template for environment variables
- `backend/test_tts.py`: Test script for the new TTS service
- `CHANGES.md`: This documentation file

## Environment Variables

### Required Changes
- **Remove**: `OPENAI_API_KEY`
- **Add**: `GOOGLE_API_KEY` (or use existing `GOOGLE_API_KEY`)

### Example .env file
```bash
GOOGLE_API_KEY=your_google_GOOGLE_API_KEY
GOOGLE_API_KEY=your_google_GOOGLE_API_KEY
CORS_ORIGINS=http://localhost:5173
```

## API Changes

### Voice Options
- **Old**: "achernar", "alloy", "echo", "fable", "onyx", "shimmer" 
- **New**: "Fenrir" (and other Google Gemini voices)

### Audio Format
- **Old**: MP3 format
- **New**: WAV format (with automatic conversion from Gemini's native format)

## Features Retained

1. **Async audio generation**: Still fully asynchronous
2. **Language detection**: Arabic/Tunisian text detection still works
3. **File saving**: Audio files are still saved to `static/audio/`
4. **Streaming support**: Both file-based and streaming endpoints work
5. **Error handling**: Comprehensive error handling maintained

## Testing

To test the new TTS service:

1. Set up your environment variables
2. Run the test script: `python test_tts.py`
3. Check the generated audio file in `static/audio/`

## Migration Benefits

1. **Unified API**: Using Google Gemini for both chat and TTS
2. **Better multilingual support**: Improved handling of different languages
3. **Cost efficiency**: Potentially better pricing with single provider
4. **Voice quality**: High-quality voice synthesis from Google

## Potential Issues

1. **Voice consistency**: Different voice names and characteristics
2. **Audio format**: Changed from MP3 to WAV (larger file sizes)
3. **API limits**: Different rate limits and quotas
4. **Environment setup**: Requires new API key configuration

## Next Steps

1. Configure `GOOGLE_API_KEY` in your environment
2. Test the TTS functionality with sample text
3. Update any frontend code that depends on MP3 format
4. Monitor audio quality and adjust voice settings as needed
