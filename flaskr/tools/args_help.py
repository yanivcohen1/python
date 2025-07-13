import argparse

file_path = r"C:\pyProj\adi\third_year\proj3\files\tmp\login_data.gzip.aes"
key_path = r".\adi\third_year\proj3\keys.key"
decrypt = True
# for args_help.py -h
parser = argparse.ArgumentParser(description="A simple command line tool that encrypts and decrypts files using AES encryption and stores the key in a separate file.")
parser.add_argument('file_path', type=str, nargs='?', default=file_path, help="File path to encrypt or decyrpt")
parser.add_argument('key_path', type=str, nargs='?', default=key_path, help="File path to save the key or read the key")
parser.add_argument('-d', '--decrypt', default=decrypt, help="Option that switchs to decyrpt mode, default is encyrpt")

args = parser.parse_args()
# Access the argument
print(f'file_path: {args.file_path}')
print(f'key_path: {args.key_path}')
print(f'decrypt: {args.decrypt}')
# for help use: python args_help.py -h
# usege: python .\args_help.py "file_path\fileName.extention.aes" "file_path\keys.key" -d false
