import os
import time
from pdf2image import convert_from_path
from exif import Image
from datetime import datetime, timedelta

# Usage
pdf_path = "D:\\meta data\\Bobby Fischer Teaches Chess.pdf" # Path to your PDF file
output_folder = "D:\\output pic"  # Folder to save the JPEG images
start_time = datetime(2023, 8, 23, 12, 30, 0)  # Set the start time

def convert_pdf_to_jpegs(pdf_path, output_folder):
    # Convert PDF to JPEG images
    images = convert_from_path(pdf_path)
    print("pdf to jpeg conversion succesful")
    
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Save each image with a sequential name (e.g., 001.jpg, 002.jpg)
    print("creating image names....")
    image_paths = []
    for i, image in enumerate(images, start=1):
        filename = f"{output_folder}/{i:03}.jpg"
        image.save(filename, 'JPEG')
        image_paths.append(filename)
    
    return image_paths
# Convert PDF to JPEG images
image_paths = convert_pdf_to_jpegs(pdf_path, output_folder)

def modify_metadata(image_paths, start_time):
    # Initialize the current time with the provided start time
    current_time = start_time

    # Iterate over each image in the list
    for image_path in image_paths:
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

        # Increment the time by 1 minute for the next image
        current_time += timedelta(minutes=1)

# Modify the metadata and file modification time of the JPEG images
modify_metadata(image_paths, start_time)
