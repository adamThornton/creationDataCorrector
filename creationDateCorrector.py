from datetime import datetime
import os
import re
import piexif

def exifDateFixer(directory, is_test = False):
    errors = []
    for dirpath,_,filenames in os.walk(directory):
        print((f'##### Checking in {dirpath}'))
        for f in filenames:
            fullPath = os.path.abspath(os.path.join(dirpath, f))
            if re.match(r"^(\d\d\d\d)(\d\d)(\d\d)_(\d\d)(\d\d)(\d\d)\S*jpg", f):
                # print(f+" Matched")
                try:
                    exif_dict = piexif.load(fullPath)
                except Exception as e:
                    message = f'Failed opening {fullPath}: {e}'
                    print(message)
                    errors.append(message)
                match = re.search("^(\d\d\d\d)(\d\d)(\d\d)_(\d\d)(\d\d)(\d\d)\S*jpg", f)
                if not is_test:
                    year = match.group(1)
                    month= match.group(2)
                    day = match.group(3)
                    hour = match.group(4)
                    minute = match.group(5)
                    second = match.group(6)
                    #Update DateTimeOriginal
                    if not exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal]:
                        exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second)).strftime("%Y:%m:%d %H:%M:%S")
                    #Update DateTimeDigitized
                    if not exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized]:
                        exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second)).strftime("%Y:%m:%d %H:%M:%S")
                    #Update DateTime
                    if not exif_dict['0th'][piexif.ImageIFD.DateTime]:
                        exif_dict['0th'][piexif.ImageIFD.DateTime] = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second)).strftime("%Y:%m:%d %H:%M:%S")
                    exif_bytes = piexif.dump(exif_dict)
                    piexif.insert(exif_bytes, fullPath)
    print(errors)


if __name__ == '__main__':
    dir = ""
    if not os.path.isdir(dir):
        print(f'Path not found: {dir}')
        exit()
    is_test = True
    for root, dirs, file_names in os.walk(dir):
        exifDateFixer(root, is_test)
