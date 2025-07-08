import whisper
import argparse
import os

parser = argparse.ArgumentParser(prog='ProgramName')
parser.add_argument('--recording_path', default='/BRAIN/neuromod-data/static00/narratives.stimuli/audio_files_filtered/')
parser.add_argument('--audio_file', default=None)
parser.add_argument('--transcription_save_path', default='../stimuli_transcriptions/')
parser.add_argument('--timesteps', default=True)
parser.add_argument('--language', default="en")
args = parser.parse_args()


if not os.path.exists(args.transcription_save_path):
    os.makedirs(args.transcription_save_path, exist_ok=True)
    print(f"Created directory: {args.transcription_save_path}")
else:
    print(f"Directory already exists: {args.transcription_save_path}")

if args.audio_file != None:
    recording_path = args.recording_path + args.audio_file
else:
    recording_path = args.recording_path

model = whisper.load_model("turbo")
transcription = model.transcribe(
    word_timestamps=True,
    audio=recording_path,
    language=args.language,
)

recording_name = recording_path.split("/")[-1].split(".")[-2]
print("Working on the recording...")
print(recording_name)

time_steps = ""
with open(args.transcription_save_path+recording_name+"_timestamps.txt", "w") as f: 
    for segment in transcription['segments']:
        #time_steps += ' '.join(f"{word['word']}[{word['start']}/{word['end']}]" for word in segment['words'])
        time_steps = ''.join(f"{word['word']}_{word['start']}_{word['end']}\n" for word in segment['words'])
        f.write(time_steps)

with open(args.transcription_save_path+recording_name+".txt", "w") as f:
    f.write(transcription["text"])

print("\n🔹 **Transcribed Speech:**\n", transcription["text"])
