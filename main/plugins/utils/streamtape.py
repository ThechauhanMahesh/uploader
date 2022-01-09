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

#response
{'status': 200, 
 'msg': 'Upload finished!', 
 'result': {'url': 'https://streamtape.com/v/V0aVPA9gegIKV6g/x_%281%29.mp4', 
            'sha256': 'e89791cd2bc63a33ffb2a617c660296e137be2466f20d74d77d306d4490c9937', 
            'name': 'x (1).mp4', 
            'size': '343468', 
            'content_type': 'video/mp4', 
            'id': 'V0aVPA9gegIKV6g'}}
            
            