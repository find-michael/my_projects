# https://youtube-dl.org/

from __future__ import unicode_literals
import youtube_dl
import os.path
from shutil import copyfile
from PIL import Image
from datetime import datetime
import json

from pydub import AudioSegment
from matplotlib import pyplot as plot
from PIL import Image, ImageDraw
import numpy as np
import os
from statistics import mean, median

#-----------------------------------------------------------------------------------
video_url = '' # <<--------- CHANGE URL HERE
#-----------------------------------------------------------------------------------
video_category = 'music'



videos_dir_path = 'F:/Videos/'
website_directory = 'F:/Users/User/Desktop/video_app/'
video_array_path = f'{website_directory}videos_array.js'
video_resolution = '360p30'
video_extension = 'mp4'
s = '        ' # 2 tabs (8 spaces)
datetime_format = '%Y-%m-%d %H:%M:%S'

def CreateBackupIfPossible(x):
	try:
		x = x[16:len(x)-1]
		x = datetime.strptime(x, datetime_format)
		time_difference = datetime.now() - x
		if time_difference.days >= 1:
			copyfile(video_array_path, f'{website_directory}Backups/videos_array-copy.js')
			print('\nVideos array file: COPY HAS BEEN CREATED\n')
			content[0] = f'// last backup: {datetime.now().strftime(datetime_format)}\n'
	except:
		print('\n!!! SOMETHING IS WRONG WITH BACKUP FILE !!!\n')

def CheckForDuplikates(x):
	for y in range(6, len(x), 8):
		new_x = x[y]
		new_x = new_x[18:len(new_x)-3]
		if new_x == video_title:
			print('\n'+video_title)
			print('new video: THIS VIDEO TITLE IS ALREADY IN VIDEO ARRAY\n')
			return False
	return True

ydl_opts = {
	# in order to check awailable resolutions: uncomment "listformats" and run code, after compilation choose format code and type it in "format" below and run again (keep it in string) 
	# 'listformats': True,
	'format': 'best', # best = 360p30 (video + audio merged)
	'outtmpl': f'{videos_dir_path}%(title)s.%(ext)s',
	'writethumbnail': f'{videos_dir_path}%(title)s.%(ext)s',
	'noplaylist': True,
}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
	info_dict = ydl.extract_info(video_url)
	video_title = info_dict.get('title', None)


#change invalid windows folder name characters to "_"
invalid_filename_characters = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
for ch in invalid_filename_characters:
	if ch in video_title:
		video_title = video_title.replace(ch, '_')

thumbnail_webp_path = f'{videos_dir_path}{video_title}.webp'


#convert thumbnail extension from webp to jpeg
if(os.path.exists(thumbnail_webp_path)):
	im = Image.open(thumbnail_webp_path).convert('RGB')
	im.save(f'{videos_dir_path}{video_title}.jpg', 'jpeg')
	os.remove(thumbnail_webp_path)

#thumbnail and video paths
thumbnail_jpg_path = f'{videos_dir_path}{video_title}.jpg'
video_path = f'{videos_dir_path}{video_title}.mp4'


#adding new video to playlist array
if(os.path.exists(video_path) & os.path.exists(thumbnail_jpg_path)):
	with open(video_array_path, "r", encoding="utf-8") as f:
		content = f.readlines()

	if CheckForDuplikates(content):
		CreateBackupIfPossible(content[0])
		content.insert(
		5, 
		f'''\t{{\n{s}"title": "{video_title}",\n{s}"category": "{video_category}",\n{s}"hashtags": ["undefined"],\n{s}"resolution": "{video_resolution}",\n{s}"extension": "{video_extension}",\n{s}"date_created": "{datetime.now().strftime(datetime_format)}"\n\t}},\n'''
		)
		with open(video_array_path, 'w', encoding="utf-8") as f:
			content = ''.join(content)
			f.write(content)

		print(f'\nnew video:	{video_title}	HAS BEEN ADDED TO PLAYLIST\n')





# move video and thumbnail to newly created folder 
if not os.path.isdir(videos_dir_path + video_title):
	os.mkdir(videos_dir_path + video_title)
if not os.path.isfile(f'{videos_dir_path}{video_title}/{video_title}.{video_extension}'):
	os.rename(video_path, f'{videos_dir_path}{video_title}/{video_title}.{video_extension}')
if not os.path.isfile(f'{videos_dir_path}{video_title}/thumbnail.jpg'):
	os.rename(thumbnail_jpg_path, f'{videos_dir_path}{video_title}/thumbnail.jpg')


# CREATE SOUND WAVE / CREATE SOUND WAVE / CREATE SOUND WAVE / CREATE SOUND WAVE / CREATE SOUND WAVE / CREATE SOUND WAVE / CREATE SOUND WAVE / CREATE SOUND WAVE / CREATE SOUND WAVE

# https://gist.github.com/moeseth/130cd92dc47c56c47030

src = f'{videos_dir_path}{video_title}/{video_title}.{video_extension}'

audio = AudioSegment.from_file(src)
data = np.frombuffer(audio._data, np.int16)
fs = audio.frame_rate

BARS = 150
BAR_HEIGHT = 80
LINE_WIDTH = 5

length = len(data)
RATIO = length/BARS

count = 0
maximum_item = 0
max_array = []
highest_line = 0
average_array = []

for d in data:
	if count < RATIO:
		count = count + 1
		if count % 10 == 0:
			average_array.append(abs(d))
		if abs(d) > maximum_item:
			maximum_item = abs(d)
	else:
		avg = mean(average_array)
		average_array = []
		max_array.append(avg)

		if maximum_item > highest_line:
			highest_line = maximum_item

		maximum_item = 0
		count = 1

line_ratio = highest_line/BAR_HEIGHT

im = Image.new('RGBA', (BARS * LINE_WIDTH, BAR_HEIGHT), (255, 255, 255, 1))
draw = ImageDraw.Draw(im)
current_x = 1
for item in max_array:
	item_height = item/line_ratio
	item_height = item_height*2

	current_y = (BAR_HEIGHT - item_height)/2
	draw.line((current_x, current_y, current_x, current_y + item_height), fill=(169, 171, 172), width=3)

	current_x = current_x + LINE_WIDTH

im.save(f'{videos_dir_path}{video_title}/sound_wave.png')
print('new video: SOUND WAVE Image CREATED\n')
