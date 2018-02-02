import requests
from bs4 import BeautifulSoup
import os
import shutil
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# driver = webdriver.Firefox(executable_path='C:\\Users\\NEO\\Desktop\\geckodriver-v0.19.0-win64\\geckodriver.exe')
driver = webdriver.Chrome(executable_path='C:\\Users\\NEO\\Desktop\\chromedriver_win32\\chromedriver.exe')

movie_file_path = "C:\\Users\\NEO\\Downloads\\Star Wars"

all_extension_list = []
all_file_list = []
video_file_list = []
name_of_folder_list = []


# SCraping unofficial IMDB API
def scrape_theimdbapi(movieid):
    page = requests.get("http://www.theimdbapi.org/api/movie?movie_id=" + movieid)

    page_str = page.text.splitlines()
    relevant_info = ['"rating"', '"description"', '"title"', '"year"', '"content_rating"', '"url": "', '"rating_count"',
                     '"genre"', '"imdb_id"', '"length"', '"director"']
    relevant_info_list = []

    count_flag = 0
    myline = ""

    for counter, line in enumerate(page_str):
        if ("genre" in line) or count_flag == 1:
            count_flag = 1
            myline = myline + line.strip()
            if "]" in line:
                count_flag = 0
                page_str[counter] = myline

    for counter, line in enumerate(page_str):
        if any(x in line for x in relevant_info):
            temp = line.replace('"', "")
            if (line.strip()[-1:]) == ",":
                temp = line.strip()[:-1].replace('"', "")
                relevant_info_list.append(temp.strip())
                continue
            relevant_info_list.append(temp.strip())

    # for counter,line in enumerate(relevant_info_list):
    # 	print(relevant_info_list[counter].strip())

    name_of_folder = ""

    for attr in relevant_info_list:
        if 'title:' in attr:
            name_of_folder = name_of_folder + "".join(attr.split(":")[1:]) + "/"
        if 'rating:' in attr:
            name_of_folder = name_of_folder + "".join(attr.split(":")[1:]) + "/"
        if 'genre:' in attr and len(attr) > 12:
            name_of_folder = name_of_folder + "".join(attr.split(":")[1:])
        if 'year:' in attr:
            name_of_folder = name_of_folder + "".join(attr.split(":")[1:]) + "/"

    print("name_of_folder = ", name_of_folder)
    name_of_folder_list.append(name_of_folder)


# Finding out the IMDB title page from the movie name
def find_imdb_movie_title(movie):
    print(movie)
    page = requests.get('https://www.google.co.in/search?q=' + movie + "+imdb.com=" + movie)
    soup = BeautifulSoup(page.content, 'html.parser')
    for cite in soup.findAll('cite'):
        if 'imdb.com/title/tt' in cite.text:
            print(cite.text)
            movieid = cite.text.split("/")[2]
            scrape_theimdbapi(movieid)
            break


# find_imdb_movie_title("House.of.Cards.S05E01.720p.WEBRiP.x265.ShAaNiG")


# Extracting the list of video files for which IMDB information would be scraped

for roots, directories, filenames in os.walk(movie_file_path):
    for files in filenames:
        filepath = os.path.join(roots, files)
        extension = os.path.splitext(filepath)[1]
        all_extension_list.append(extension)
        all_file_list.append(filepath)

unq_ext = set(all_extension_list)
print(unq_ext)

for files in all_file_list:
    if os.stat(files).st_size > 52352252:
        video_file_list.append(files)

for counter, files in enumerate(video_file_list):
    movie_name = os.path.split(files)[-1]
    find_imdb_movie_title(movie_name)

for x in range(len(video_file_list)):
    print("Movie Path -->", video_file_list[x], "Extracted Information -->", name_of_folder_list[x])
