# https://gist.github.com/moeseth/130cd92dc47c56c47030

from pydub import AudioSegment
from matplotlib import pyplot as plot
from PIL import Image, ImageDraw
import numpy as np
import os
from statistics import mean, median

src = "C:/Users/MaJK/Desktop/test2.mp4"

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

		if abs(d) > maximum_item:
			maximum_item = abs(d)
	else:
		max_array.append(maximum_item)

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
	item_height = item_height
	# print(item_height)

	current_y = (BAR_HEIGHT - item_height)/2  # without /2 image is not mirrored
	draw.line((current_x, current_y, current_x, current_y + item_height), fill=(169, 171, 172), width=3)

	current_x = current_x + LINE_WIDTH

# draw.line((0, BAR_HEIGHT/2, current_x-LINE_WIDTH+1, BAR_HEIGHT/2), fill=(50, 50, 50), width=1)
im.show()
# im.save("C:/Users/MaJK/Desktop/geeks.png")