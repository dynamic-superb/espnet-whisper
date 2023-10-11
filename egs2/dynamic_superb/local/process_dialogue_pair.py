import glob
from os.path import join
import os
import json
from pydub import AudioSegment
import tqdm
data_dirs = glob.glob(join("/mnt/data/data-for-stan", "*DialogueActPairing*", "*"))
print(data_dirs)


def concatenate_with_silence(file1, file2, output_file, silence_duration_ms=1000):
    # Load the audio files
    audio1 = AudioSegment.from_file(file1)
    audio2 = AudioSegment.from_file(file2)

    # Add silence between the audios
    silence = AudioSegment.silent(duration=silence_duration_ms)
    combined_audio = audio1 + silence + audio2

    # Export the combined audio
    combined_audio.export(output_file, format="wav")

for data_dir in data_dirs:
    
    metadata = json.load(open(join(data_dir, "metadata_save.json"), 'r'))
    new_metadata = {}
    for file, info in tqdm.tqdm(metadata.items()):
        assert os.path.exists(join(data_dir, file.replace(".wav", "_pair.wav")))
        concatenate_with_silence(
            join(data_dir, file), 
            join(data_dir, file.replace(".wav", "_pair.wav")),
            join(data_dir, file.replace(".wav", "_concat.wav")),
        )
        new_metadata[file.replace(".wav", "_concat.wav")] = info
    json.dump(new_metadata, open(join(data_dir, "metadata.json"), 'w'))
# Example usage
# concatenate_with_silence("audio1.wav", "audio2.wav", "output.wav")