#from streamtape api docs
import requests
import hashlib

def upload(login, key, file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
        sha256 = sha256_hash.hexdigest()
    url = f'https://api.streamtape.com/file/ul?login={login}&key={key}&sha256={sha256}'
    data = requests.get(url).json()
    upload_url = data['result']['url']
    file = {'file': open(file_path, 'rb')}
    upload_request = requests.post(upload_url, files=file)
    upload_response = upload_request.json()
    return upload_response 
    #status: 200 => Success
