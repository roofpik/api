from restful import Resource
from flask_restful import reqparse
import sendgrid
from offlineEmail import offlineEmailContent

def sendMail(email, code, adminid):
	client = sendgrid.SendGridClient("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")
	message = sendgrid.Mail()
	message.add_to(email)
	message.set_from("contact@roofpik.com")
	message.set_subject("[Team Roofpik]Email verification code")
	message.set_html("")
	result = client.send(message)
	if str(result[0]) == '200':
		return True
	return False

def validateName(name):
	return len(name) <= 40

def validateEmail(email):
	return (re.match(r'.*@.*\..*', email) and len(email) <= 255)

def genActivationCode():
	return '-'.join(str(random.randint(100,999)) for i in range(4))

class addNewAdmin(Resource):

	def post(self):

		parser = reqparse.RequestParser()
		parser.add_argument('fname', type=str)
		parser.add_argument('lname', type=str)
		parser.add_argument('email', type=str)
		parser.add_argument('uid', type=str)
		args = parser.parse_args()

		_fname = args['fname']
		_lname = args['lname']
		_email = args['email']
		_uid = args['uid']

		if not _fname or not validateName(_fname):
			return {'StatusCode':'400', 'Message':'Invalid name'}
		if not _email or not validateEmail(_email):
			return {'StatusCode':'400', 'Message':'Invalid email'}

		if not _uid:
			return {'StatusCode':'400', 'Message':'Invalid user'}

		_code = genActivationCode()

		if not sendMail(_email, _code, _admin_id):
			return {'StatusCode':'400', 'Message':'Email not sent'}

		return {'StatusCode':'200', 'Message':'A mail was sent to the email account with the verification link.', 'uid':_uid}
