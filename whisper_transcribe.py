import whisper
import argparse
import os

parser = argparse.ArgumentParser(prog='ProgramName')
parser.add_argument('--recording_path', default='../recordings_download/recordings_cleaned/sub_003/ses_005/sub-03_ses-005_20230517-131445_task-ForgotRecall_run-01_audio_DeepFilterNet3.wav')
parser.add_argument('--transcription_save_path', default='../recordings_download/recordings_transcriptions/sub_003/ses_005/')
parser.add_argument('--timesteps', default=True)
parser.add_argument('--language', default="en")
args = parser.parse_args()


if not os.path.exists(args.transcription_save_path):
    os.makedirs(args.transcription_save_path, exist_ok=True)
    print(f"Created directory: {args.transcription_save_path}")
else:
    print(f"Directory already exists: {args.transcription_save_path}")


model = whisper.load_model("turbo")
transcription = model.transcribe(
    word_timestamps=True,
    audio=args.recording_path,
    language=args.language,
)

recording_name = args.recording_path.split("/")[-1].split(".")[-2]
print("Working on the recording...")
print(recording_name)

time_steps = ""
with open(args.transcription_save_path+recording_name+"_timestamps.txt", "w") as f: 
    for segment in transcription['segments']:
        #time_steps += ' '.join(f"{word['word']}[{word['start']}/{word['end']}]" for word in segment['words'])
        time_steps = ''.join(f"{word["word"]}_{word["start"]}_{word["end"]}\n" for word in segment['words'])
        f.write(time_steps)

with open(args.transcription_save_path+recording_name+".txt", "w") as f:
    f.write(transcription["text"])

print("\n🔹 **Transcribed Speech:**\n", transcription["text"])
