import os
import re
import piexif

def absoluteFilePaths(directory):
	for dirpath,_,filenames in os.walk(directory):
		for f in filenames:
			fullPath = os.path.abspath(os.path.join(dirpath, f))
			if re.match(r"^(\d\d\d\d)(\d\d)(\d\d)_(\d\d)(\d\d)(\d\d)\S*jpg", f) or :
				print(f+" Matched")
				match = re.search("^(\d\d\d\d)(\d\d)(\d\d)_(\d\d)(\d\d)(\d\d)\S*jpg", f)
				year = match.group(1)
				month= match.group(2)
				day = match.group(3)
                hour = match.group(4)
                minute = match.group(5)
                second = match.group(6)
				exif_dict = piexif.load(fullPath)
				#Update DateTimeOriginal
				exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second)).strftime("%Y:%m:%d %H:%M:%S")
				#Update DateTimeDigitized				
				exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second)).strftime("%Y:%m:%d %H:%M:%S")
				#Update DateTime
				exif_dict['0th'][piexif.ImageIFD.DateTime] = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second)).strftime("%Y:%m:%d %H:%M:%S")
				exif_bytes = piexif.dump(exif_dict)
				piexif.insert(exif_bytes, fullPath)
				print("############################")


absoluteFilePaths("__DIRECTORY_WITH_PHOTOS__")