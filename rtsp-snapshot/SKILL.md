---
name: rtsp-snapshot
description: Captures a still frame from an RTSP camera stream using ffmpeg. Use when asked to get a snapshot, still image, or single frame from an RTSP source.
---

# RTSP Snapshot

This skill uses `ffmpeg` to capture a single, high-quality still frame from a network RTSP stream.

## Usage

Execute the following shell command. Replace `<RTSP_URL>` with the full RTSP connection string for your camera and `<OUTPUT_FILE>` with the desired output path (e.g., `~/.openclaw/media/rtsp-snapshots/living-room.jpg`).

### Recommended Command

```bash
ffmpeg -y -rtsp_transport tcp -i "<RTSP_URL>" -ss 00:00:01 -vframes 1 -q:v 8 -colorspace smpte170m -color_primaries smpte170m -color_trc smpte170m "<OUTPUT_FILE>"
```

### Command Breakdown

-   `-y`: Overwrite the output file without asking.
-   `-rtsp_transport tcp`: Forces the stream to use TCP instead of UDP. This is more reliable and prevents corrupted or incomplete images, especially over Wi-Fi or congested networks.
-   `-i "<RTSP_URL>"`: Specifies the input RTSP stream URL.
-   `-ss 00:00:01`: Seeks 1 second into the stream before capturing the frame. This gives the stream time to stabilize and avoids capturing a black or garbled initial frame.
-   `-vframes 1`: Captures exactly one video frame and then stops.
-   `-update 1`: Overwrites the single output file, which is the correct way to handle single-frame grabs.
-   `-q:v 8`: Sets the JPEG quality level. The scale is 2 (best) to 31 (worst). A value of 8 is a good balance of quality and file size.
-   `"<OUTPUT_FILE>"`: The path where the snapshot image will be saved.
