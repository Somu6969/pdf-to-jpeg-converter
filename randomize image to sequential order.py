import os
import time
from exif import Image
from datetime import datetime, timedelta

def modify_metadata_by_filename(folder_path, start_time):
    # Get a sorted list of all image files in the folder that match the pattern
    image_paths = sorted([os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.jpg') or f.endswith('.jpeg')])

    # Iterate over each image in the list
    for image_path in image_paths:
        # Extract the sequence number from the filename (e.g., 001 from 001.jpg)
        sequence_number = int(os.path.splitext(os.path.basename(image_path))[0])

        # Calculate the timestamp based on the start time and sequence number
        current_time = start_time + timedelta(minutes=(sequence_number - 1))

        # Open the image and read metadata
        with open(image_path, 'rb') as image_file:
            img = Image(image_file)

        # Check if the image has EXIF data
        if img.has_exif:
            # Format the current time as a string for EXIF data
            time_str = current_time.strftime('%Y:%m:%d %H:%M:%S')

            # Update the EXIF timestamps
            img.datetime_original = time_str
            img.datetime_digitized = time_str
            img.datetime = time_str

            # Write the updated metadata back to the image file
            with open(image_path, 'wb') as image_file:
                image_file.write(img.get_file())

        # Update the file modification and access times
        mod_time = time.mktime(current_time.timetuple())
        os.utime(image_path, (mod_time, mod_time))

# Usage
folder_path = "D:\\output pic"  # Path to your folder containing the images
start_time = datetime(2023, 8, 23, 12, 30, 0)  # Set the start time

modify_metadata_by_filename(folder_path, start_time)
  