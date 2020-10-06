import os
from glob import glob
import sys

videos_dir_path = 'F:\\Videos\\'
videos_extension = '.mp4'

videos_path = glob(f'{videos_dir_path}*{videos_extension}')

videos_array = []

for x in videos_path:
	print(x)
	# try:
	# 	os.mkdir(x.replace(videos_extension, ''))

	# 	os.rename(x, videos_dir_path + x.replace(videos_dir_path, '').replace(videos_extension, '') + "\\" + x.replace(videos_dir_path, ''))
	# 	os.rename(x.replace(videos_extension, '.jpg'), videos_dir_path + x.replace(videos_dir_path, '').replace(videos_extension, '') + "\\thumbnail.jpg")

	# 	os.remove(x)
	# 	os.remove(x.replace(videos_extension, '.jpg'))
	# except Exception as e:
	# 	print(e)

