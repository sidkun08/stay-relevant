import requests

def download_files(file_url, file_path):
    downloading = requests.get(url=file_url)
    if downloading.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(downloading.content)
        print("Great")
    else:
        print('Trash')

urls = [
    ''
]