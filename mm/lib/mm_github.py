import requests
import mm_util

def sign_in(creds):
    r = requests.get('https://mavensmate.appspot.com/github', params={'username':creds['username'], 'password':creds['password']}, verify=False)
    r.raise_for_status()
    return mm_util.parse_rest_response(r.text)

    
