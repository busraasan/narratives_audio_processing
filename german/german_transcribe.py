import whisper
import argparse
import os
import librosa
import soundfile as sf
from utils import merge_splits

'''
    Code for transcribing audio files using the Whisper model.
    Default: turbo is used
    Optional: For enhancing accuracy and avoiding missed sentences during transcription, you may try to split then transcribe.
'''

parser = argparse.ArgumentParser(prog='German Transcription')
parser.add_argument('--recording_path', default='../german_chapters/single_chapters/splits/Kapitel_2/clip_4_Kapitel_2.wav')
parser.add_argument('--transcription_save_path', default='../german_chapters/transcriptions/clips/')
parser.add_argument('--split_and_transcribe', default=False, help="Split the audio into 4min segments and transcribe each segment")
parser.add_argument('--model', default='large')
parser.add_argument('--timesteps', default=True)
parser.add_argument('--language', default="de")
args = parser.parse_args()

def split_recordings(signal_data, duration=4):
    '''
        Splits the audio signal into chunks of specified duration (in minutes) and saves them as separate files.
    '''

    chunk_duration = duration * 60

    # Total number of samples in each chunk
    chunk_samples = int(chunk_duration * sr)

    # Total number of chunks
    total_chunks = (len(signal_data) + chunk_samples - 1) // chunk_samples

    base_path = os.path.dirname(args.recording_path)
    recording_name = args.recording_path.split("/")[-1].split(".")[-2]
    output_dir = os.path.join(base_path+'/splits', recording_name)
    os.makedirs(output_dir, exist_ok=True)

    for count in range(total_chunks):

        start_sample = count * chunk_samples
        end_sample = min((count + 1) * chunk_samples, len(signal_data))

        clip = signal_data[start_sample:end_sample]

        # Save the clip to a new file
        output_path = os.path.join(output_dir, f'clip_{count}_{recording_name}.wav')
        sf.write(output_path, clip, sr)

        print(f"Saved {output_path}")

    return output_dir


if not os.path.exists(args.transcription_save_path):
    os.makedirs(args.transcription_save_path, exist_ok=True)
    print(f"Created directory: {args.transcription_save_path}")
else:
    print(f"Directory already exists: {args.transcription_save_path}")


model = whisper.load_model(args.model)
transcription = model.transcribe(
    word_timestamps=True,
    audio=args.recording_path,
    language=args.language,
)

if args.split_and_transcribe:

    print("Splitting the audio into 4min segments...")
    signal_data, sr = librosa.load(args.recording_path, sr=None)
    splits_dir = split_recordings(signal_data, duration=4)
    
    kapitel_name = args.recording_path.split("/")[-1].split(".")[-2]
    save_path = args.transcription_save_path+'/splits/'+kapitel_name+"/"

    print("Transcribing each chunk...")
    for count, file in enumerate(os.listdir(splits_dir)):
        if file.endswith(".wav"):
            file_path = os.path.join(splits_dir, file)
            transcription = model.transcribe(
                word_timestamps=True,
                audio=file_path,
                language=args.language,
            )

            recording_name = file.split(".")[-2]
            print("Working on the recording chunk...")
            print(recording_name)

            time_steps = ""
            if not os.path.exists(save_path):
                os.makedirs(save_path, exist_ok=True)

            with open(save_path+recording_name+"_timestamps.txt", "w") as f: 
                for segment in transcription['segments']:
                    time_steps = ''.join(f"{word["word"]}_{word["start"]}_{word["end"]}\n" for word in segment['words'])
                    f.write(time_steps)

            with open(save_path+recording_name+".txt", "w") as f:
                f.write(transcription["text"])

    merge_splits(folder_path=save_path, output_file=save_path+"merged_transcription.txt")

else:
    recording_name = args.recording_path.split("/")[-1].split(".")[-2]
    print("Working on the recording...")
    print(recording_name)
    time_steps = ""
    with open(args.transcription_save_path+recording_name+"_timestamps.txt", "w") as f: 
        for segment in transcription['segments']:
            time_steps = ''.join(f"{word["word"]}_{word["start"]}_{word["end"]}\n" for word in segment['words'])
            f.write(time_steps)

    with open(args.transcription_save_path+recording_name+".txt", "w") as f:
        f.write(transcription["text"])

    print("\n🔹 **Transcribed Speech:**\n", transcription["text"])
