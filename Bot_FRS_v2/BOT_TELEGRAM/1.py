
import subprocess

# Замените YOUTUBE_VIDEO_URL на URL видео с YouTube
youtube_video_url = "https://www.youtube.com/watch?v=EQkCiCIcwx0"

# Задайте имя выходного аудиофайла (например, output.mp3)
output_audio_file = "output.mp3"

# Команда для извлечения аудио из видео с YouTube с использованием ffmpeg
ffmpeg_command = [
    "ffmpeg",
    "-i", youtube_video_url,
    "-q:a", "0",
    "-map", "a",
    output_audio_file
]

try:
    # Выполните команду ffmpeg
    subprocess.run(ffmpeg_command, check=True)
    print(f"Аудио успешно извлечено и сохранено в {output_audio_file}")
except subprocess.CalledProcessError as e:
    print(f"Произошла ошибка: {e}")
