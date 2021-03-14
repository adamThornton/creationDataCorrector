from datetime import datetime
import os
import re
import piexif

log_enabled = False
dir_count: int = 0
file_count: int = 0

def log(message: str):
    if log_enabled:
        print(message)

class ExifDateFixer:

    def __init__(self, is_test):
        self.is_test = is_test
        self.current_file_number: int = 0

    def update_progress(self):
        self.current_file_number = self.current_file_number + 1
        print(f'##### {(self.current_file_number/file_count)*100}% #####', end='\r')

    def exifDateFixer(self, directory):
        errors = []
        for dirpath,_,filenames in os.walk(directory):
            log((f'##### Checking in {dirpath}'))
            for f in filenames:
                fullPath = os.path.abspath(os.path.join(dirpath, f))
                self.update_progress()
                if re.match(r"^(\d\d\d\d)(\d\d)(\d\d)_(\d\d)(\d\d)(\d\d)\S*jpg", f):
                    # print(f+" Matched")
                    try:
                        exif_dict = piexif.load(fullPath)
                    except Exception as e:
                        message = f'Failed opening {fullPath}: {e}'
                        log(message)
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
    dir = "\\\\SYNOLOGYNAS\photo\sylvia"
    if not os.path.isdir(dir):
        print(f'Path not found: {dir}')
        exit()
    is_test = True

    start = datetime.now()
    for root, dirs, file_names in os.walk(dir):
        log(f"{root}")
        dir_count = dir_count + 1
        for f in file_names:
            file_count = file_count + 1
    print(f'Total dirs: {dir_count}')
    print(f'Total files: {file_count}')

    fixer = ExifDateFixer(is_test)
    for root, dirs, file_names in os.walk(dir):
        fixer.exifDateFixer(root)
    print(f'Elapsed time: {datetime.now() - start}')
