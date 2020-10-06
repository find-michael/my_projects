import os
from pydub import AudioSegment
from matplotlib import pyplot as plot
from PIL import Image, ImageDraw
import numpy as np
import os
from statistics import mean, median


rootdir = 'F:\\Videos'
go = None

for subdir, dirs, files in os.walk(rootdir):
	for file in files:
		if os.path.join(subdir, file).find('.mp4') != -1:
			video_path = os.path.join(subdir, file)
			file_path = video_path[:video_path.rfind('\\')]
			# print(video_path)
			# print(file_path)

			if file_path.replace('F:\\Videos\\', '') == 'DEAF KEV - Safe & Sound with Sendi Hoxha [NCS Release]':
				go = True

			if go:

				print(file_path.replace('F:\\Videos\\', ''))
				src = video_path

				audio = AudioSegment.from_file(src)
				data = np.frombuffer(audio._data, np.int16)
				fs = audio.frame_rate

				BARS = 150
				BAR_HEIGHT = 80
				LINE_WIDTH = 5

				length = len(data)
				RATIO = length/BARS
				print(length)

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
				# print(max_array)
				current_x = 1
				for item in max_array:
					item_height = item/line_ratio
					item_height = item_height*2
					# print(item_height)

					current_y = (BAR_HEIGHT - item_height)/2  # without /2 image is not mirrored
					draw.line((current_x, current_y, current_x, current_y + item_height), fill=(169, 171, 172), width=3)

					current_x = current_x + LINE_WIDTH

				im.save(file_path + '\\sound_wave.png')
