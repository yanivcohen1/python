import os
import shutil

DOWNLOAD_DIR =r"C:\Temp\Adi\adi\secend_year\proj2\download\\"
ZIP_DIR = "C:\\Temp\\Adi\\adi\\secend_year\\proj2\\users\\"

def create_zip_file_from_folder(zipFileName):
    """  Creating the user pics ZIP file
    """
    path = ZIP_DIR + zipFileName
    archived = shutil.make_archive(path, 'zip', DOWNLOAD_DIR)

    if os.path.exists(path+".zip"):
        print(archived)
        # delete all files in folder
        for (dirpath, dirnames, filenames) in os.walk(DOWNLOAD_DIR):
            for filename in filenames:
                os.remove(dirpath + "\\" + filename)
    else:
        print("ZIP file not created")


if __name__ == '__main__':
    create_zip_file_from_folder("yaniv")
