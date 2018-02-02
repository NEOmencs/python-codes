# this code puts video files and .srt files out of subfolders and put it in main folders, also deletes unwanted files like .txt files etc, also deletes empty folder,
# check messages printed

import os
import shutil

#####################Parameters setting###########################################################################
mainfolder = "C:\\NEO"
list_of_extensions_to_move = ['.avi', '.mkv', '.mp4', '.srt']
list_of_extensions_to_delete = ['.txt', '.ini', '.sub', '.mp3']
need_to_move_files = "no"
need_to_delete_files = "no"
need_to_delete_empty_directories = "no"
##################################################################################################################

if (os.path.exists(mainfolder)) == 0:
    print("Folder does not exist")

if (os.path.exists(mainfolder)) == 1:

    all_files_with_path = []
    all_files_to_retain = []
    all_list_of_extension = []
    counter_for_printing_not_moving_files_message = 0
    counter_for_file_deletions_message = 0
    counter_for_directory_deletion_message = 0

    for root, directories, files in os.walk(mainfolder):
        for filename in files:
            filepath = os.path.join(root, filename)  # Joining path with filename
            all_files_with_path.append(filepath)  # List of all files with complete path
            extension = os.path.splitext(filename)[1]  # Extracting Extension
            all_list_of_extension.append(extension)  # List of all extensions

        for dir in directories:
            directory_path = os.path.join(root, dir)
            if os.listdir(directory_path) == []:
                if need_to_delete_empty_directories == "yes":
                    print("Following empty directory is empty and will be deleted- ", directory_path)
                    os.rmdir(directory_path)
                if need_to_delete_empty_directories != "yes":
                    if counter_for_directory_deletion_message == 0:
                        print(
                            "Following directory are empty, if you need to delete these, change the variable -need_to_delete_empty_directories to 'yes' ")
                        counter_for_directory_deletion_message = counter_for_directory_deletion_message + 1
                    print(directory_path)

    # for eachfile in all_files_with_path:
    # 	extension = os.path.splitext(eachfile)[1]
    # 	if extension in list_of_extensions_to_move:             #If extension is in the list of extension which are to be moved
    # 		all_files_to_retain.append(eachfile)                #List of files based on the extension to be retained
    # 		if os.path.split(eachfile)[0] != mainfolder:
    # 			if need_to_move_files == "yes":
    # 				print(eachfile,"--will be moved to--",mainfolder)
    # 				shutil.move(eachfile,os.path.join(mainfolder,os.path.split(eachfile)[1]))	#Moving the files from subfolders to the main folder
    # 			if need_to_move_files != "yes":
    # 				if counter_for_printing_not_moving_files_message==0:
    # 					print("---------------------------------")
    # 					print("")
    # 					print("Following files are not MOVED, change the variable - need_to_move_files to 'yes' to move the files to mainfolder --")
    # 					print("")
    # 					counter_for_printing_not_moving_files_message=counter_for_printing_not_moving_files_message+1
    # 				print(eachfile)

    for eachfile in all_files_with_path:
        extension = os.path.splitext(eachfile)[1]
        if extension in list_of_extensions_to_delete:  # If extension is in the list of extension which are to be moved
            if need_to_delete_files == "yes":
                print(eachfile, "--will be deleted--")
                os.remove(eachfile)
            if need_to_delete_files != "yes":
                if counter_for_file_deletions_message == 0:
                    print("---------------------------------")
                    print("")
                    print(
                        "Following files are not DELETED, change the variable - need_to_delete_files to 'yes' to delete the files ---,")
                    print("")
                    counter_for_file_deletions_message = counter_for_file_deletions_message + 1
                print(eachfile)

    print("---------------------")
    unq_extensions = set(all_list_of_extension)
    print("Unique Extensions in the containing folder", unq_extensions)
