---
name: ffmpeg-assembly
description: Generate FFmpeg commands for assembling images, video clips, and audio into final episode MP4
---

Generate and execute FFmpeg command chains for final episode assembly. Handles image-to-video conversion with Ken Burns effects, video concatenation, audio mixing (voice at 0dB, music at -18dB, effects at -12dB), loudness normalization to -14 LUFS, subtitle embedding, and H.264/AAC export at 1920x1080 for YouTube.
