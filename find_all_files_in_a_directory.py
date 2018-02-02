import os

mypath = "C:\\NEO\\Movies"

all_files_with_path = []
for root, directories, files in os.walk(mypath):
    for filename in files:
        filepath = os.path.join(root, filename)
        all_files_with_path.append(filepath)

# for i in range(len(all_files_with_path)):
#     print(all_files_with_path[i])

all_files_extension = []
for files in all_files_with_path:
    extension = os.path.splitext(files)[1]
    all_files_extension.append(extension)

unq_extensions = set(all_files_extension)
# print(unq_extensions)

all_video_files = []
# {'.ini', '.png', '.avi', '.zip', '.jpg', '.mkv', '.txt', '.mp4', '.mp3', '.sub', '.srt'}
for i in range(len(all_files_extension)):
    if all_files_extension[i] in ['.avi', '.mkv', '.mp4']:
        all_video_files.append(all_files_with_path[i])

for all_files in all_video_files:
    print(all_files)
