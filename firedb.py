from firebase import Firebase
from firebase_token_generator import create_token

def roofpik_connect(url, auth = False):
	url = 'https://roofpik-948d0.firebaseio.com/' + url
#	url = 'https://roofpik-26701.firebaseio.com/' + url
	if auth is True:
		auth_payload = {"uid": "bhptnfQoq1eEytRBbjjGDrv40oC2"}
#		auth_payload = {"uid": "mKu9O7vMCkhb3Vr7lmd5tDWNjZv1"}
		token = create_token("neftLmN0eBpzsRLAasLcer70wt6KqM6OZmoHKgFd", auth_payload)
	#	token = create_token("C261yE4hTVRHXV7eSJXUMfnFFayssep7OT6uRa2z", auth_payload)
		return Firebase(url, auth_token=token)
	return Firebase(url)


