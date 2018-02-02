# this code renames list of subtitles as per the video files

import os
import shutil

###############################################Parameters Setting ###################################################################
video_file_path = "C:\\NEO\\The Big Bang Theory\\The Big Bang Theory Season 9"
# subtitles_library="C:\\NEO\\The Big Bang Theory\\The Big Bang Theory Season 1\\the-big-bang-theory-first-season_HI_english-1175854"
video_file_extension = ['.avi', '.mkv', '.mp4']
want_to_rename_subtitles = 'yes'
######################################################################################################################################

video_file_list = []
subtitles_list = []
all_extension_list = []

for roots, directories, filenames in os.walk(video_file_path):
    for files in filenames:
        filepath = os.path.join(roots, files)
        extension = os.path.splitext(filepath)[1]
        all_extension_list.append(extension)
        if extension in video_file_extension:
            video_file_list.append(filepath)
        if extension in [".srt", ".sub"]:
            subtitles_list.append(filepath)

unq_extension = list(set(all_extension_list))
print("Extension of all the files in the folder - ", unq_extension)

video_file_list.sort()
subtitles_list.sort()

for video_files in video_file_list:
    print(video_files)

for ext in unq_extension:
    if ext not in video_file_extension:
        print("Check for the files with extension ----> ", ext,
              " --might need to add them in the list - video_file_extension")

if len(video_file_list) > len(subtitles_list):
    print("Cant RENAME subtitles  -- Number of video files are more than the number of subtitles")
if len(subtitles_list) > len(video_file_list):
    print("Cant RENAME subtitles -- Number of subtitles are more than the number of video files")

if want_to_rename_subtitles != "yes":
    print("If you want to rename the subtitles files, change want_to_rename_subtitles to 'yes'")

if (len(subtitles_list) == len(video_file_list) and want_to_rename_subtitles == "yes"):
    for serial in range(len(subtitles_list)):
        # shutil.move(subtitles_list[serial],os.path.join(video_file_path,(os.path.split(video_file_list[serial])[1])).split('.')[0]+".srt")
        shutil.move(subtitles_list[serial], os.path.join(video_file_path, video_file_list[serial].replace(
            video_file_list[serial].split('.')[-1], "") + "srt"))
