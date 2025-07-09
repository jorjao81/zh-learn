#!/usr/bin/env python3
"""
Chinese Gameplay Processor

Extracts Chinese dialogue segments from gameplay videos by:
1. Detecting voice activity in audio
2. Transcribing speech with Whisper
3. Filtering for Chinese content
4. Creating edited video with only story segments
"""

import whisper
import ffmpeg
import numpy as np
from moviepy.editor import VideoFileClip, concatenate_videoclips
import webrtcvad
import wave
import contextlib
import os
import sys
from typing import List, Dict, Tuple
import argparse
import tempfile


class ChineseGameplayProcessor:
    def __init__(self, whisper_model="base", vad_aggressiveness=3):
        """
        Initialize the processor
        
        Args:
            whisper_model: Whisper model size (tiny, base, small, medium, large)
            vad_aggressiveness: Voice activity detection sensitivity (0-3)
        """
        print(f"Loading Whisper model: {whisper_model}")
        self.whisper_model = whisper.load_model(whisper_model)
        self.vad = webrtcvad.Vad(vad_aggressiveness)
        
    def extract_audio(self, video_path: str, audio_path: str) -> None:
        """Extract audio from video file"""
        print("Extracting audio from video...")
        (
            ffmpeg
            .input(video_path)
            .output(audio_path, acodec='pcm_s16le', ac=1, ar='16000')
            .run(overwrite_output=True, quiet=True)
        )
    
    def detect_speech_segments(self, audio_path: str) -> List[Tuple[float, bool]]:
        """Detect segments with speech using VAD"""
        print("Analyzing voice activity...")
        with contextlib.closing(wave.open(audio_path, 'rb')) as wf:
            sample_rate = wf.getframerate()
            frames = wf.getnframes()
            audio_data = wf.readframes(frames)
            
        # Process in 30ms chunks
        chunk_size = int(sample_rate * 0.03)  # 30ms
        speech_segments = []
        
        for i in range(0, len(audio_data), chunk_size * 2):
            chunk = audio_data[i:i + chunk_size * 2]
            if len(chunk) >= chunk_size * 2:
                is_speech = self.vad.is_speech(chunk, sample_rate)
                timestamp = i / (sample_rate * 2)
                speech_segments.append((timestamp, is_speech))
                
        return speech_segments
    
    def transcribe_and_detect_chinese(self, audio_path: str) -> List[Dict]:
        """Transcribe audio and detect Chinese segments"""
        print("Transcribing audio and detecting Chinese...")
        result = self.whisper_model.transcribe(audio_path, language='zh')
        
        chinese_segments = []
        for segment in result['segments']:
            # Check if segment contains Chinese characters
            if self.contains_chinese(segment['text']):
                chinese_segments.append({
                    'start': segment['start'],
                    'end': segment['end'],
                    'text': segment['text'].strip(),
                    'confidence': segment.get('confidence', 0.5)
                })
        
        return chinese_segments
    
    def contains_chinese(self, text: str) -> bool:
        """Check if text contains Chinese characters"""
        for char in text:
            if '\u4e00' <= char <= '\u9fff':
                return True
        return False
    
    def merge_segments(self, segments: List[Dict], min_gap: float = 2.0) -> List[Dict]:
        """Merge nearby segments to avoid choppy cuts"""
        if not segments:
            return []
            
        merged = [segments[0].copy()]
        
        for segment in segments[1:]:
            last_segment = merged[-1]
            if segment['start'] - last_segment['end'] <= min_gap:
                # Merge segments
                merged[-1]['end'] = segment['end']
                merged[-1]['text'] += ' ' + segment['text']
            else:
                merged.append(segment.copy())
                
        return merged
    
    def extract_video_segments(self, video_path: str, segments: List[Dict], output_path: str) -> None:
        """Extract and concatenate video segments"""
        print(f"Extracting {len(segments)} video segments...")
        clips = []
        
        for i, segment in enumerate(segments):
            print(f"  Processing segment {i+1}/{len(segments)}: {segment['start']:.1f}s-{segment['end']:.1f}s")
            clip = VideoFileClip(video_path).subclip(
                segment['start'], 
                segment['end']
            )
            clips.append(clip)
        
        if clips:
            print("Concatenating segments...")
            final_clip = concatenate_videoclips(clips)
            final_clip.write_videofile(output_path, codec='libx264')
            final_clip.close()
            
            # Clean up clips
            for clip in clips:
                clip.close()
        else:
            print("No segments to process!")
    
    def process_video(self, video_path: str, output_path: str, min_gap: float = 2.0) -> None:
        """Main processing function"""
        if not os.path.exists(video_path):
            print(f"Error: Video file '{video_path}' not found!")
            return
            
        # Use temporary file for audio
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
            audio_path = temp_audio.name
        
        try:
            # Extract audio
            self.extract_audio(video_path, audio_path)
            
            # Detect Chinese speech
            chinese_segments = self.transcribe_and_detect_chinese(audio_path)
            
            if not chinese_segments:
                print("No Chinese speech detected in video!")
                return
            
            print(f"\nFound {len(chinese_segments)} Chinese segments:")
            total_duration = 0
            for i, seg in enumerate(chinese_segments):
                duration = seg['end'] - seg['start']
                total_duration += duration
                print(f"  {i+1:2d}. {seg['start']:6.1f}s-{seg['end']:6.1f}s ({duration:4.1f}s): {seg['text']}")
            
            print(f"\nTotal Chinese content: {total_duration:.1f} seconds")
            
            # Merge nearby segments
            print(f"\nMerging segments with gaps < {min_gap}s...")
            merged_segments = self.merge_segments(chinese_segments, min_gap)
            
            merged_duration = sum(seg['end'] - seg['start'] for seg in merged_segments)
            print(f"After merging: {len(merged_segments)} segments, {merged_duration:.1f} seconds")
            
            # Extract video segments
            self.extract_video_segments(video_path, merged_segments, output_path)
            
            print(f"\nProcessed video saved to: {output_path}")
            
        finally:
            # Clean up temporary audio file
            if os.path.exists(audio_path):
                os.unlink(audio_path)


def main():
    parser = argparse.ArgumentParser(description='Extract Chinese dialogue from gameplay videos')
    parser.add_argument('input_video', help='Input video file path')
    parser.add_argument('output_video', help='Output video file path')
    parser.add_argument('--model', default='base', 
                       choices=['tiny', 'base', 'small', 'medium', 'large'],
                       help='Whisper model size (default: base)')
    parser.add_argument('--min-gap', type=float, default=2.0,
                       help='Minimum gap between segments before merging (seconds)')
    parser.add_argument('--vad-aggressiveness', type=int, default=3, choices=[0, 1, 2, 3],
                       help='Voice activity detection aggressiveness (0-3)')
    
    args = parser.parse_args()
    
    processor = ChineseGameplayProcessor(
        whisper_model=args.model,
        vad_aggressiveness=args.vad_aggressiveness
    )
    
    processor.process_video(args.input_video, args.output_video, args.min_gap)


if __name__ == "__main__":
    main()