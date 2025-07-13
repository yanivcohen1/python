import wget
filename = wget.download('https://github.com/AlexMa123/BIU_Computational_physics_2023/raw/main/data.zip')

import zipfile
with zipfile.ZipFile(filename, 'r') as zip_ref:
    # Extract the files to a specified directory (e.g., 'extracted_files')
    zip_ref.extractall()

import os
os.remove(filename)

## optional
# import urllib.request
# url = 'https://github.com/AlexMa123/BIU_Computational_physics_2023/raw/main/data.zip'
# filename = url.split("/")[-1]
# urllib.request.urlretrieve(url, filename)
