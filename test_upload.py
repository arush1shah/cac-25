import requests

url = 'http://127.0.0.1:5000/upload-image'
file_path = '/Users/taratony/Downloads/letter.png'

with open(file_path, 'rb') as img_file:
    files = {'image': img_file}
    response = requests.post(url, files=files)
    #print(response.json())