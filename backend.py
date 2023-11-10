from pydub import AudioSegment
import os
import shutil
import mutagen
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
    flac_tags = mutagen.File(input_file)
    if flac_tags is None:
        return
    
    # Copy FLAC tags to OPUS file
    opus_tags = mutagen.File(output_file, easy=True)
    if opus_tags is None:
        return
    
    # Exclude the "LYRICS" tag
    if "LYRICS" in flac_tags:
        del flac_tags["LYRICS"]
    elif "lyrics" in flac_tags:
        del flac_tags["lyrics"]
    
    opus_tags.clear()
    opus_tags.update(flac_tags)
    opus_tags.save()

def copy_cover(input_file, output_file):
    # Load FLAC cover
    flac_tags = mutagen.File(input_file)
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
    
    # Check if there is a cover file with any case variation in the input directory
    input_dir = os.path.dirname(input_file)
    for file in os.listdir(input_dir):
        if file.lower() == "cover.jpg":
            cover_file = os.path.join(input_dir, file)
            # Copy the cover file to the output directory
            shutil.copy(cover_file, os.path.dirname(output_file))
            return
        
def convert_file(input_file, output_folder):
    output_file = os.path.join(output_folder, os.path.basename(input_file).replace(".flac", ".opus"))
    flac_to_opus(input_file, output_file)
    copy_tags(input_file, output_file)
    copy_cover(input_file, output_file)

def batch_convert_folder(input_folder, output_folder):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through all FLAC files in the input folder
    flac_files = []
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(".flac"):
                flac_files.append(os.path.join(root, file))

    # Convert each FLAC file to OPUS
    for file in flac_files:
        convert_file(file, output_folder)
    print("Batch conversion completed.")