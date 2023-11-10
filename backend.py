from pydub import AudioSegment
import os
import io
import shutil
import mutagen
import tempfile
import threading
import time

# Global variable to store progress
progress = [0]
time_spent = [0]

def flac_to_opus(input_file, output_file, bitrate_mode, bitrate, tune):
    # Load FLAC file
    audio = AudioSegment.from_file(input_file, format="flac")
    # Set Opus encoder options
    encoder_options = [
        "-c:a", "libopus",
        "-b:a", f"{bitrate}k",  # Convert bitrate from kilobits to bits
    ]
    if tune == "Music":
        encoder_options.extend(["-application", "audio"])
    elif tune == "Speech":
        encoder_options.extend(["-application", "voip"])
    if bitrate_mode == "hard-cbr":
        encoder_options.extend(["-compression_level", "10"])
    elif bitrate_mode == "vbr":
        encoder_options.extend(["-vbr", "on"])
    elif bitrate_mode == "cvbr":
        encoder_options.extend(["-vbr", "constrained"])

    # Export as OPUS file in memory
    output_stream = io.BytesIO()
    audio.export(output_stream, format="opus", parameters=encoder_options) 
    # Set the stream position to the beginning
    output_stream.seek(0)
    # Write the OPUS data to the output file
    with open(output_file, "wb") as f:
        f.write(output_stream.read())

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

def batch_convert_folder(input_folder, output_folder, encoder_settings):
    # Extract Opus encoder settings
    bitrate_mode = encoder_settings.get("bitrate_mode")
    bitrate = int(encoder_settings.get("bitrate"))
    tune = encoder_settings.get("tune")
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through all FLAC files in the input folder
    flac_files = []
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(".flac"):
                flac_files.append(os.path.join(root, file))
                
    # Track progress and measure conversion time
    completed_tasks = 0
    total_tasks = len(flac_files)
    start_time = time.time()
                
    # Define a function to convert a single FLAC file to OPUS
    def convert_file(input_file, output_folder):
        output_file = os.path.join(output_folder, os.path.basename(input_file).replace(".flac", ".opus"))
        flac_to_opus(input_file, output_file, bitrate_mode, bitrate, tune)     
        copy_tags(input_file, output_file)
        copy_cover(input_file, output_file)
        progress_callback()
        
        def update_time_spent():
            nonlocal completed_tasks
            elapsed_time = time.time() - start_time
            time_spent[0] = elapsed_time
            if completed_tasks < total_tasks:
                time.sleep(0.1)  # Update every 1 second
                update_time_spent()

        update_time_spent()
    
    def progress_callback():
        nonlocal completed_tasks
        completed_tasks += 1
        progress[0] = completed_tasks / total_tasks * 100
        
    # Convert each file using a separate thread
    threads = []
    for file in flac_files:
        thread = threading.Thread(target=convert_file, args=(file, output_folder))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
def get_progress():
    return progress[0], time_spent[0]