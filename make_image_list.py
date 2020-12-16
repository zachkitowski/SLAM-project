import os

print "hello"

video_folder = "/home/zach/dev_code/JM_Videos/cam1V2_lowlight"
output_txt_name = 'JM_Videos/cam1V2_lowlight.txt'

image_list =[]
for filename in os.listdir(video_folder):

	filename = filename.replace('frame','')
	filename = filename.replace('.jpg','')
	image_list.append(int(filename))
	# print filename
image_list.sort()
# sort(image_list)
# print(image_list)

writeFile = open(output_txt_name, 'w')

for image_id in image_list:
	writeFile.write(str(image_id)+'\n')
writeFile.close()