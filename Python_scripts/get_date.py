import os
from glob import glob
from datetime import datetime
import json
import sys

videos_dir_path = 'F:\\Videos\\'
videos_extension = '.mp4'
datetime_format = '%Y-%m-%d %H:%M:%S'
json_file_name = 'F:\\Users\\User\\Desktop\\video_app\\videos_array.js'

videos_path = glob(f'{videos_dir_path}*{videos_extension}')

videos_array = []

# print(len(videos_path))

for x in videos_path:
	video_title = x.replace(videos_dir_path, '').replace(videos_extension, '')

	# print(video_title)
	c_file_time = os.path.getctime(x)
	human_time = datetime.fromtimestamp(c_file_time).strftime(datetime_format)

	# print(f'{human_time}\n')
	videos_array.append([video_title, 'music', '', human_time])

ready_to_json = [{'title': x[0], 'category': x[1], 'hashtags': x[2], 'resolution': '360p30', 'extension': 'mp4', 'date_created': x[3]} for x in videos_array]

# https://stackoverflow.com/questions/18337407/saving-utf-8-texts-in-json-dumps-as-utf8-not-as-u-escape-sequence
# \/ PRETTY json print WITH SPECIAL CHARACTERS (decoded) \/ 
new_array = json.dumps(ready_to_json, indent=4, ensure_ascii=False).encode('utf8')
print(new_array.decode())

with open(json_file_name, 'a', encoding='utf-8') as f:
	f.write(f'// last backup: {datetime.now().strftime(datetime_format)}\n// videos directory\nvar videos_file = "F:/Videos/";\n\nvar videos_array = ')

