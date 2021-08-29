from types import MethodDescriptorType
import zipfile # imports the zipfile module so you can make use of it
import shutil # imports the shutil module 
import os # for manipulating directories
from os.path import basename # for deleting any prefix up to the last slash character of a pathname

def zip_files(destination_file, list_of_files, compress=zipfile.ZIP_DEFLATED): # it will now compresses by default
  # create ZipFile object in "w"ritemode, storing the reference in the new_zip object
  with zipfile.ZipFile(destination_file, mode="w", compression=compress) as new_zip: 
      # the function parameter destination_file is passed as an argument to the constructor
      # the end result is that destination_file is the filename of the destination zip file
      # compress will dictate the compression used when creating the ZipFile object
      for file in list_of_files:
        # goes through every file in the list_of_files - received as a function parameter
        new_zip.write(file) # the file you want add to the zip file

def list_zip_file_contents(source_file): # the function receives the name of an existing file
  # Read source_file which is an already existing zip file
  with zipfile.ZipFile(source_file, mode="r") as source:
    # prints the name of the existing zip file
    print(source_file)
    # Get list of files names in zip
    file_names = source.namelist()
    # Iterate over the list of file names print them
    for file_name in file_names:
        # prints the name of files within, with a tab for better readability
        print("\t", file_name)

def add_files_to_zip_file(destination_file, list_of_files):
  # create ZipFile object in "a"ppend mode in order to add content to the file
  with zipfile.ZipFile(destination_file, mode="a") as new_zip: 
      # the files will be added to the destination_file
      for file in list_of_files:
        # goes through every file in the list_of_files 
        new_zip.write(file) # the file you want add to the zip file

def unzip_files_with_zipfile(source_file, destination_folder, files_to_extract):
  with zipfile.ZipFile(source_file, mode="r") as source:
    if files_to_extract:
      for file in files_to_extract:
        source.extract(file, path=destination_folder)
    else:
      source.extractall(path=destination_folder)

def unzip_files_with_shutil(source_file, destination_folder):
  shutil.unpack_archive(source_file, destination_folder)

def filter_and_zip_files(destination_file, list_of_files, filter): 
  print ("hello")

# zip the files from given directory that matches the filter
def filter_and_zip_files (destination_file, source_foulder, filter):
   with zipfile.ZipFile(destination_file, mode="w", compression=zipfile.ZIP_DEFLATED) as new_zip:
       # Iterate over all the files in the folder
       test = os.walk(source_foulder)
       for folder, subfolders, filenames in os.walk(source_foulder):
           for filename in filenames:
               if filter(filename):
                   # create complete filepath of file in directory
                   file_path = os.path.join(folder, filename)
                   # Add file to zip
                   new_zip.write(file_path, basename(file_path))

# unzip only files withtin the zip file that match the filter 
def unzip_filtered_files (source_file, destination_folder, filter):
		with zipfile.ZipFile(source_file, "r") as source:
		   list_of_file_names = source.namelist() # you'll get an iterable object
		   for file_name in list_of_file_names:
		       # checks if the file matches the filter ls

		       if  filter(file_name):
		           # Extract the files to destination_folder
		           source.extract(file_name,path=destination_folder )
  
# zipping a single file
zip_files("single_file.zip", ["all_black.bmp"])

# zipping multiple files
zip_files("multiple_files.zip", ["all_blue.bmp","all_green.bmp", "all_red.bmp"])

# zipping and compressing multiple files
zip_files("multiple_files_uncompressed.zip", ["all_blue.bmp","all_green.bmp", "all_red.bmp"], zipfile.ZIP_STORED)

# listing the contents of existing zip file
list_zip_file_contents("multiple_files.zip")

print("adding all_black.bmp to multiple_files.zip")
# adding all_black.bmp to the multiple_files.zip
add_files_to_zip_file("multiple_files.zip", ["all_black.bmp"])

# listing the contents of existing zip file
list_zip_file_contents("multiple_files.zip")

# unzipping all files to the folder all_colors
unzip_files_with_zipfile("multiple_files.zip", "all_colors", [])

# unzipping only colors that start with b to only_b_colors 
unzip_files_with_zipfile("multiple_files.zip", "only_b_colors", ["all_black.bmp", "all_blue.bmp"])

# unzipping all colors with shutil
unzip_files_with_shutil("multiple_files.zip", "shutil_extraction")

# zipping only colors that start with b to only_b_colors by using_filters
filter_and_zip_files("only_b_colors.zip", ".", lambda name : name.startswith("all_b"))
list_zip_file_contents("only_b_colors.zip")

# unzipping only colors that start with b to only_b_colors by using_filters
unzip_filtered_files("multiple_files.zip", "not_b_colors", lambda name : not name.startswith("all_b"))