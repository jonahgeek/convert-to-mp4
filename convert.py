import argparse
import ffmpeg

def convert_mov_to_mp4(input_file, output_file, video_bitrate="1M", audio_bitrate="128k", resolution=None):
    """
    Convert a .mov file to .mp4 with both video and audio, and reduce the size while maintaining quality.
    
    :param input_file: Path to the input .mov file
    :param output_file: Path to the output .mp4 file
    :param video_bitrate: Target video bitrate (default: 1M)
    :param audio_bitrate: Target audio bitrate (default: 128k)
    :param resolution: Output resolution, e.g., "1280x720" or None to keep the original resolution
    """
    # Build the ffmpeg command with necessary parameters
    input_stream = ffmpeg.input(input_file)

    # Apply resolution scaling if specified
    if resolution:
        input_stream = ffmpeg.filter(input_stream, 'scale', resolution.split('x')[0], resolution.split('x')[1])

    # Convert to mp4 format with specified video and audio bitrate
    stream = ffmpeg.output(
        input_stream, output_file, 
        vcodec='libx264', acodec='aac',
        video_bitrate=video_bitrate, audio_bitrate=audio_bitrate, 
        movflags='faststart'
    )

    # Ensure audio and video are included
    stream = stream.global_args('-map', '0:v', '-map', '0:a')

    # Run the ffmpeg command
    ffmpeg.run(stream)
    print(f"Conversion complete: {output_file}")

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Convert .mov to .mp4 and include audio.")
    
    parser.add_argument("input", help="Path to the input .mov video file")
    parser.add_argument("output", help="Path to the output .mp4 video file")
    parser.add_argument("--video_bitrate", default="1M", help="Set the video bitrate (default: 1M)")
    parser.add_argument("--audio_bitrate", default="128k", help="Set the audio bitrate (default: 128k)")
    parser.add_argument("--resolution", help="Set the output resolution, e.g., '1280x720' (optional)")
    
    args = parser.parse_args()

    # Call the function with parsed arguments
    convert_mov_to_mp4(args.input, args.output, args.video_bitrate, args.audio_bitrate, args.resolution)
