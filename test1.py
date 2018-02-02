# Download IMDB datasets from here - https://datasets.imdbws.com/
import os
import pandas as pd
import difflib
import re

# IMDB Datasets Path - contains info related to Movie titles
imdb_data_files_tbasics = 'C:\\Users\\NEO\\Desktop\\New folder\\imdb\\title.basics.tsv.gz'
# IMDB Datasets Path - contains info related to Ratings
imdb_data_files_tratings = 'C:\\Users\\NEO\\Desktop\\New folder\\imdb\\title.ratings.tsv.gz'
movie_file_path = "C:\\NEO\\Movies"  # Path where movies are stored

# Garbage words which are present in the movie Names
replace_words = ["720p", "Bluray", "\.", "x264", "YTS AG", "YIFY", "www UsaBit com", "\[", "\]", "_", "anoXmous",
                 "BrRip","sujaidr", "-", "\(", "\)", "Ganool", "TMRG", "1080p", "480p","10th Anniversary Edition"]

all_extension_list = []
all_file_list_with_path = []
video_file_list_with_path = []
name_of_movie_list = []
imdb_matched_movie_list = []

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
    if os.stat(files).st_size > 524288000:  # 500 MB , filtering files which are greater than 500 MB in size
        video_file_list_with_path.append(files)

for x in range(len(video_file_list_with_path)):
    name_of_movie_list.append(video_file_list_with_path[x].split("\\")[-1])

# Creating Pandas Data frame from the list of movie names
df_movie = pd.DataFrame({"primaryTitle": name_of_movie_list})
# Cleaning up the movie Names - removing extension from the name
df_movie['MovieName'] = df_movie['primaryTitle'].str.rsplit('.', 1).str[0]

# Replacing garbage words with blank
for i in range(len(replace_words)):
    df_movie['MovieName'] = df_movie['MovieName'].apply(lambda x: re.sub(replace_words[i], " ", x, flags=re.IGNORECASE))
    df_movie['MovieName'] = df_movie['MovieName'].str.strip()

# Searching for 4 digits to extract YEAR
df_movie['year'] = df_movie['MovieName'].str.findall('\d{4}')
# Removing year from the name
df_movie['MovieName'] = df_movie['MovieName'].str.replace(r'\d{4}', "")
# Removing Garbage words which represents size - 900MB etc
df_movie['MovieName'] = df_movie['MovieName'].str.replace(r'\d+MB', "")
# Reducing multiple spaces to one
df_movie['MovieName'] = df_movie['MovieName'].str.replace(r' +', " ")
df_movie['MovieName'] = df_movie['MovieName'].str.strip()

print(df_movie)
################################################

# Reading IMDB datasets in Pandas Data frame
df_tbasics = pd.read_csv(imdb_data_files_tbasics, sep="\t", encoding="utf-8", dtype="unicode")
df_tratings = pd.read_csv(imdb_data_files_tratings, sep="\t", encoding="utf-8", dtype="unicode")

# Merging Title info and ratings into one Data frame
df_ratings_basics = pd.merge(df_tratings, df_tbasics, on=['tconst'], how='inner')
df_ratings_basics['runtimeMinutes'] = df_ratings_basics['runtimeMinutes'].str.replace(r'\\N',"0")

for i in range(len(df_movie)):
    if len(df_movie.loc[i]['year']) == 0:
        temp = difflib.get_close_matches(df_movie.loc[i]['MovieName'], df_ratings_basics['primaryTitle'], 1, cutoff=0.6)
        imdb_matched_movie_list.append(temp)
    else:
        for j in range(len(df_movie.loc[i]['year'])):
            df_ratings_basics_filtered = df_ratings_basics[(df_ratings_basics['startYear'] == df_movie['year'].loc[i][j])
                                                    & (pd.to_numeric(df_ratings_basics['runtimeMinutes']) > 60)]
            temp = difflib.get_close_matches(df_movie.loc[i]['MovieName'], df_ratings_basics_filtered['primaryTitle'], 1,
                                             cutoff=0.6)
            print(df_movie.loc[i]['MovieName'], "------", temp, "-----", df_movie['year'].loc[i][j])
            if len(temp) > 0:
                imdb_matched_movie_list.append(temp)
                continue

df_movie['imdb_matched_name'] = pd.DataFrame({'imdb_matched_name' : imdb_matched_movie_list})

df_movie_imdb = pd.merge(df_movie , df_ratings_basics, left_on = ['imdb_matched_name'], right_on = ['primaryTitle'],how='inner')

