import requests
from util import login


email = ""
psw = ""
fingerprint = ""




session = requests.Session()
session.headers.update({
    'Accept': 'application/json'

})

fingerprint = login.Start(session, email, psw)