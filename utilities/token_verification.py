import jwt
import json
import requests
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend
import re
PEMSTART = "-----BEGIN CERTIFICATE-----\n"
PEMEND = "\n-----END CERTIFICATE-----\n"

def verify_token(token):
    try:
        headers = jwt.get_unverified_header(token)
        x5t = headers['x5t']
        mspubkey = get_key(x5t)
        IDTOKEN = token
        tenant_id = "553cc67e-03c7-4071-ae58-fdac604c5006"
        cert_str = PEMSTART + mspubkey + PEMEND
        cert_obj = load_pem_x509_certificate(cert_str.encode(), default_backend())
        public_key = cert_obj.public_key()
        decoded = jwt.decode(IDTOKEN, public_key, algorithms=['RS256'], audience=tenant_id)
        m = re.search('[a-zA-Z0-9_.+-]+@(?:(?:[a-zA-Z0-9-]+\.)?[a-zA-Z]+\.)?(symbtechnologies)\.com', decoded['upn'])
        if decoded and m:
            print ("Decoded!",decoded)
            return decoded
        else:
            print ("Could not decode token.")
            return False
    except Exception as e:
        print(e)
        return False

def get_key(x5t):
    res = requests.get('https://login.microsoftonline.com/common/.well-known/openid-configuration')
    jwk_uri = res.json()['jwks_uri']
    response = requests.get(jwk_uri)
    keys = json.loads(response.text)
    for data in keys['keys']:
        if data['x5t'] == x5t:
            return data['x5c'][0]
        else:
            return False 

