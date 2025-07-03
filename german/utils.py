import os
import re

def merge_splits(folder_path, output_file):

    txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]

    # Sort the files if needed (important if you want them in correct order like clip_0, clip_1, etc.)
    def extract_clip_number(filename):
        match = re.search(r'clip_(\d+)_', filename)
        if match:
            return int(match.group(1))
        else:
            return -1  # In case the pattern is not found

    txt_files.sort(key=extract_clip_number)

    # Merge all files
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for filename in txt_files:
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as infile:
                content = infile.read()
                outfile.write(content)

def merge_timesteps(folder_path, output_file):
    txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    # Sort the files if needed (important if you want them in correct order like clip_0, clip_1, etc.)
    def extract_clip_number(filename):
        match = re.search(r'clip_(\d+)_', filename)
        if match:
            return int(match.group(1))
        else:
            return -1  # In case the pattern is not found

    txt_files.sort(key=extract_clip_number)
    whole_timestampes = ""

    with open(output_file, 'w', encoding='utf-8') as outfile:
        
        for i, filename in enumerate(txt_files):

            file_path = os.path.join(folder_path, filename)
            offset = 4 * 60 * i

            with open(file_path, 'r', encoding='utf-8') as infile:
                for line in infile:
                    line = line.strip()
                    
                    try:
                        # Split into parts: word, start, end
                        parts = line.rsplit('_', 2)  # Split from the right, maximum 2 splits
                        word = parts[0]
                        start = float(parts[1])
                        end = float(parts[2])

                        # Add 240 seconds to start and end
                        start += offset
                        end += offset

                        # Write back to output file
                        whole_timestampes += f"{word}_{start:.2f}_{end:.2f}\n"

                    except Exception as e:
                        print(f"Error processing line: {line}")
                        print(e)

        outfile.write(whole_timestampes)


def merge_timestamps(file_path, output_path):
    merged_lines = []

    with open(file_path, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    for line in lines:
        line = line.strip()
        if not line:
            continue  # skip empty lines

        if line.startswith('-'):
            # Merge with the previous line
            prev_line = merged_lines.pop()

            # Split previous and current lines
            prev_parts = prev_line.rsplit('_', 2)
            curr_parts = line.lstrip('-').rsplit('_', 2)

            # Extract word and timings
            prev_word, prev_start, _ = prev_parts
            curr_word, _, curr_end = curr_parts

            # Merge words and update timing
            merged_word = prev_word + '-' + curr_word
            merged_line = f"{merged_word}_{prev_start}_{curr_end}"

            # Push back the merged line
            merged_lines.append(merged_line)

        elif line.lstrip().startswith('.') and line.lstrip()[1].isdigit():
            # Special case: line starts with . followed by a digit
            prev_line = merged_lines.pop()

            prev_parts = prev_line.rsplit('_', 2)
            curr_parts = line.rsplit('_', 2)

            prev_word, prev_start, _ = prev_parts
            curr_word, _, curr_end = curr_parts

            # Merge without hyphen
            merged_word = prev_word + curr_word
            merged_line = f"{merged_word}_{prev_start}_{curr_end}"

            merged_lines.append(merged_line)

        elif line.lstrip().startswith(',') and line.lstrip()[1].isdigit():
            # Special case: line starts with , followed by digits
            prev_line = merged_lines.pop()

            prev_parts = prev_line.rsplit('_', 2)
            curr_parts = line.rsplit('_', 2)

            prev_word, prev_start, _ = prev_parts
            curr_word, _, curr_end = curr_parts

            merged_word = prev_word + curr_word
            merged_line = f"{merged_word}_{prev_start}_{curr_end}"

            merged_lines.append(merged_line)

        elif re.fullmatch(r'\.[a-zA-Z]\.', line.split('_')[0]):
            # Special case: fragment like .c. that contains at least one letter inside symbols
            print(f"Fragment detected: {line}")
            prev_line = merged_lines.pop()

            prev_parts = prev_line.rsplit('_', 2)
            curr_parts = line.rsplit('_', 2)

            prev_word, prev_start, _ = prev_parts
            curr_word, _, curr_end = curr_parts

            # Merge normally (no hyphen), just attach
            merged_word = prev_word + curr_word
            merged_line = f"{merged_word}_{prev_start}_{curr_end}"

            merged_lines.append(merged_line)

        else:
            # Normal line, just add it
            word, start, end = line.split('_')
            if re.fullmatch(r'[\W_]+', word, re.UNICODE):
                pass
            else:
                merged_lines.append(line)

    # Now write to output or print
    with open(output_path, 'w', encoding='utf-8') as outfile:
        for line in merged_lines:
            outfile.write(line + '\n')
                                


if __name__ == "__main__":

    num_chapter = 2
    
    merge_splits(
        folder_path = f"../german_chapters/transcriptions/splits/Kapitel_{num_chapter}/transcriptions/",
        output_file = f"../german_chapters/transcriptions/splits/Kapitel_{num_chapter}/merged_transcription_updated.txt"
    )

    merge_timesteps(
        folder_path = f"../german_chapters/transcriptions/splits/Kapitel_{num_chapter}/timestamps/",
        output_file = f"../german_chapters/transcriptions/splits/Kapitel_{num_chapter}/merged_transcription_timestamps_updated.txt"
    )