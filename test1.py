# Download IMDB datasets from here - https://datasets.imdbws.com/
# Documentation  - https://datasets.imdbws.com/
import os
import pandas as pd
import difflib
import re
import shutil
import datetime

pd.set_option('display.max_colwidth', -1)

# IMDB Datasets Path - contains info related to Movie titles
imdb_data_files_tbasics = 'C:\\Users\\NEO\\Desktop\\New folder\\imdb\\title.basics.tsv.gz'
# IMDB Datasets Path - contains info related to Ratings
imdb_data_files_tratings = 'C:\\Users\\NEO\\Desktop\\New folder\\imdb\\title.ratings.tsv.gz'
movie_file_path = "C:\\NEO\\Movies"  # Path where movies are stored

# Garbage words which are present in the movie Names
replace_words = ["720p", "Bluray", "\.", "x264", "YTS AG", "YIFY", "www UsaBit com", "\[", "\]", "_", "anoXmous",
                 "BrRip", "sujaidr", "-", "\(", "\)", "Ganool", "TMRG", "1080p", "480p", "10th Anniversary Edition", "DVDScr"
                 "XVID", "AC3", "EtMovies", "YTS"]
Movie_or_Serial = 'movie'
delim = "___"

all_extension_list = []
all_file_list_with_path = []
video_file_list_with_path = []
name_of_movie_list = []
imdb_matched_movie_list = []
year_of_movie_list = []
name_of_movie_folder_list = []

# Extracting the list of video files for which IMDB information would be extracted
for roots, directories, filename in os.walk(movie_file_path):
    for files in filename:
        filepath = os.path.join(roots, files)
        extension = os.path.splitext(filepath)[1]
        all_extension_list.append(extension)
        all_file_list_with_path.append(filepath)

unq_ext = set(all_extension_list)
# print(unq_ext)

for files in all_file_list_with_path:
    if os.stat(files).st_size > 104857600:  # 00 MB , filtering files which are greater than 500 MB in size
        video_file_list_with_path.append(files)

# Searching for 4 digits to extract YEAR
for x in range(len(video_file_list_with_path)):
    with open(os.path.join(movie_file_path, "all_folder_names.txt"), 'a') as fh:
        fh.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M') + " -- " + video_file_list_with_path[x] + "\n")
        if x == len(video_file_list_with_path) - 1:
            fh.write("_________________________________________________________________________________________________________________" + "\n")
    name_of_movie_list.append(video_file_list_with_path[x].split("\\")[-1])
    name_of_movie_folder_list.append(video_file_list_with_path[x].split("\\")[-2])
    year = re.findall(r'\d\d\d\d', ''.join(re.findall(r'\(\d\d\d\d\)', video_file_list_with_path[x].split("\\")[-2])))
    if not year:
        year = re.findall(r'\d\d\d\d', video_file_list_with_path[x].split("\\")[-2])
    if not year:
        year = re.findall(r'\d\d\d\d', ''.join(re.findall(r'\(\d\d\d\d\)', video_file_list_with_path[x].split("\\")[-1])))
    if not year:
        year = re.findall(r'\d\d\d\d', video_file_list_with_path[x].split("\\")[-1])
    year = ''.join(year)
    year_of_movie_list.append(year)
    if movie_file_path == video_file_list_with_path[x].rsplit("\\", 1)[0]:
        print("This movie is not in its own folder -- ", video_file_list_with_path[x].split("\\")[-1])
        if not os.path.isdir(os.path.join(movie_file_path, video_file_list_with_path[x].split("\\")[-1].rsplit(".", 1)[0])):
            os.makedirs(os.path.join(movie_file_path, video_file_list_with_path[x].split("\\")[-1].rsplit(".", 1)[0]))
        shutil.move(video_file_list_with_path[x], os.path.join(movie_file_path, video_file_list_with_path[x].split("\\")[-1].rsplit(".", 1)[0]))
    with open(os.path.join(video_file_list_with_path[x].rsplit("\\", 1)[0], "Previous_folder_names.txt"), "a") as fh:
        fh.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M') + " -- Previous Folder Name - " + "'" + video_file_list_with_path[x].split("\\")[-2] + "'" + "\n")


for x in range(len(name_of_movie_list)):
    print(name_of_movie_folder_list[x], "-----", name_of_movie_list[x], "-----", year_of_movie_list[x])

print("___________________________________________________________________________________________")
print("___________________________________________________________________________________________")
# Creating Pandas Data frame from the list of movie names
df_movie = pd.DataFrame({"primaryTitle": name_of_movie_list})
# Cleaning up the movie Names - removing extension from the name
df_movie['MovieName'] = df_movie['primaryTitle'].str.rsplit('.', 1).str[0]

# Replacing garbage words with blank
for i in range(len(replace_words)):
    df_movie['MovieName'] = df_movie['MovieName'].apply(lambda x: re.sub(replace_words[i], " ", x, flags=re.IGNORECASE))
    df_movie['MovieName'] = df_movie['MovieName'].str.strip()


df_movie['year'] = pd.Series(year_of_movie_list)
df_movie['complete_path'] = pd.Series(video_file_list_with_path)
# Removing year from the name
for i in range(len(df_movie)):
    df_movie.loc[i]['MovieName'] = df_movie.loc[i]['MovieName'].replace(str(df_movie.loc[i]['year']), "")
# Removing Garbage words which represents size - 900MB etc
df_movie['MovieName'] = df_movie['MovieName'].str.replace(r'\d+MB', "")
# Reducing multiple spaces to one
df_movie['MovieName'] = df_movie['MovieName'].str.replace(r' +', " ")
df_movie['MovieName'] = df_movie['MovieName'].str.strip()

################################################

# Reading IMDB datasets in Pandas Data frame
df_tbasics = pd.read_csv(imdb_data_files_tbasics, sep="\t", encoding="utf-8", dtype="unicode")
df_tratings = pd.read_csv(imdb_data_files_tratings, sep="\t", encoding="utf-8", dtype="unicode")

# Merging Title info and ratings into one Data frame
df_ratings_basics = pd.merge(df_tratings, df_tbasics, on=['tconst'], how='inner')
df_ratings_basics['runtimeMinutes'] = df_ratings_basics['runtimeMinutes'].str.replace(r'\\N', "0")
imdb_matched_movie_list = []
for i in range(len(df_movie)):
    if len(df_movie.loc[i]['year']) == 0:
        temp = difflib.get_close_matches(df_movie.loc[i]['MovieName'], df_ratings_basics['primaryTitle'], 1, cutoff=0.6)
        imdb_matched_movie_list.append(temp)
#         print("year missing")
    else:
        try:
            df_ratings_basics_filtered = df_ratings_basics[(df_ratings_basics['startYear'] == df_movie['year'].loc[i])]
#                                                     & (pd.to_numeric(df_ratings_basics['runtimeMinutes']) > 60)]
            temp = difflib.get_close_matches(df_movie.loc[i]['MovieName'], df_ratings_basics_filtered['primaryTitle'], 1,
                                             cutoff=0.6)
            imdb_matched_movie_list.append(''.join(temp))
            print(df_movie.loc[i]['MovieName'], "------", temp, "-----", df_movie['year'].loc[i])
        except ValueError:
            print("Character values found in RuntimeMinutes")

print("___________________________________________________________________________________________")
print("___________________________________________________________________________________________")

df_movie['imdb_matched_name'] = pd.Series(imdb_matched_movie_list)

print(df_movie)

print("___________________________________________________________________________________________")
print("___________________________________________________________________________________________")

df_movie_imdb = pd.merge(df_movie, df_ratings_basics, left_on=['imdb_matched_name'], right_on=['primaryTitle'], how='inner')

# pd.set_option('display.max_colwidth', -1)
# # pd.set_option('display.height', 1000)
# pd.set_option('display.max_rows', 500)
# pd.set_option('display.max_columns', 10)
# pd.set_option('display.width', 5000)
# pd.set_option('display.expand_frame_repr', False)

df_movie_new = pd.merge(df_movie, df_ratings_basics[df_ratings_basics['titleType'] == Movie_or_Serial], left_on=['imdb_matched_name', 'year'], right_on=['primaryTitle', 'startYear'], how='inner')
df_movie_new['to_rename'] = df_movie_new['imdb_matched_name'] + delim + df_movie_new['year'] + delim + df_movie_new['averageRating'] + delim + df_movie_new['runtimeMinutes'] + delim + df_movie_new['genres']
print(df_movie_new)

print("___________________________________________________________________________________________")
print("___________________________________________________________________________________________")

for x in range(len(video_file_list_with_path)):
    os.rename(video_file_list_with_path[x].rsplit("\\", 1)[0], os.path.join(video_file_list_with_path[x].rsplit("\\", 1)[0], df_movie_new.loc[x]['to_rename']))
