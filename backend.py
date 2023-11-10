from pydub import AudioSegment
from pydub.utils import mediainfo
from mutagen import File
import os
import subprocess
import shutil
import tempfile

def flac_to_opus(input_file, output_file):
    # Load FLAC file
    audio = AudioSegment.from_file(input_file, format="flac")

    # Export as temporary WAV file
    temp_wav_file = os.path.join(tempfile.gettempdir(), "temp.wav")
    audio.export(temp_wav_file, format="wav")

    # Load temporary WAV file
    wav_audio = AudioSegment.from_file(temp_wav_file, format="wav")

    # Export as OPUS file
    wav_audio.export(output_file, format="opus")

    # Remove temporary WAV file
    os.remove(temp_wav_file)

def copy_tags(input_file, output_file):
    # Load FLAC tags
    flac_tags = File(input_file)

    # Copy FLAC tags to OPUS file
    opus_tags = File(output_file, easy=True)
    opus_tags.update(flac_tags)

def copy_cover(input_file, output_file):
    # Load FLAC cover
    flac_tags = File(input_file)
    flac_cover = flac_tags.tags.get("APIC:")
    
    if flac_cover:
        # Save FLAC cover as a temporary image file
        temp_cover_file = os.path.join(tempfile.gettempdir(), "temp_cover.jpg")
        with open(temp_cover_file, "wb") as f:
            f.write(flac_cover.data)

        # Copy the temporary cover to the output directory
        shutil.copy(temp_cover_file, os.path.dirname(output_file))

        # Remove temporary cover file
        os.remove(temp_cover_file)

def batch_convert_folder(input_folder, output_folder):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through all FLAC files in the input folder
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(".flac"):
                input_file = os.path.join(root, file)
                output_file = os.path.join(output_folder, file.replace(".flac", ".opus"))

                # Convert and copy tags and cover
                flac_to_opus(input_file, output_file)
                copy_tags(input_file, output_file)
                copy_cover(input_file, output_file)

if __name__ == "__main__":
    # Replace 'input_folder' with the path to your folder containing FLAC files
    input_folder = "path/to/flac/folder"

    # Replace 'output_folder' with the desired path for the output OPUS files
    output_folder = "path/to/output/folder"

    batch_convert_folder(input_folder, output_folder)