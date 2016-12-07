from restful import Resource
from flask_restful import reqparse
import re
import random
import sendgrid
import datetime
import firedb
import socket
import md5
import string

def emailHtml(email, code, userid):

	html = """
<html>
  <head>
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
      <title>Verify your Roofpik account email address</title>
      
      <style type="text/css">
         /* Client-specific Styles */
         #outlook a {padding:0;} /* Force Outlook to provide a "view in browser" menu link. */
         body{width:100% !important; -webkit-text-size-adjust:100%; -ms-text-size-adjust:100%; margin:0; padding:0;}
         /* Prevent Webkit and Windows Mobile platforms from changing default font sizes, while not breaking desktop design. */
         .ExternalClass {width:100%;} /* Force Hotmail to display emails at full width */
         .ExternalClass, .ExternalClass p, .ExternalClass span, .ExternalClass font, .ExternalClass td, .ExternalClass div {line-height: 100%;} /* Force Hotmail to display normal line spacing.*/
         #backgroundTable {margin:0; padding:0; width:100% !important; line-height: 100% !important;}
         img {outline:none; text-decoration:none;border:none; -ms-interpolation-mode: bicubic;}
         a img {border:none;}
         .image_fix {display:block;}
         p {margin: 0px 0px !important;}
         table td {border-collapse: collapse;}
         table { border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt; }
         a {color: #0a8cce;text-decoration: none;text-decoration:none!important;}
         /*STYLES*/
         table[class=full] { width: 100%; clear: both; }
         /*IPAD STYLES*/
         @media only screen and (max-width: 640px) {
         a[href^="tel"], a[href^="sms"] {
         text-decoration: none;
         color: #0a8cce; /* or whatever your want */
         pointer-events: none;
         cursor: default;
         }
         .mobile_link a[href^="tel"], .mobile_link a[href^="sms"] {
         text-decoration: default;
         color: #0a8cce !important;
         pointer-events: auto;
         cursor: default;
         }
         table[class=devicewidth] {width: 440px!important;text-align:center!important;}
         table[class=devicewidthinner] {width: 420px!important;text-align:center!important;}
         img[class=banner] {width: 440px!important;height:220px!important;}
         img[class=colimg2] {width: 440px!important;height:220px!important;}
         
         
         }
         /*IPHONE STYLES*/
         @media only screen and (max-width: 480px) {
         a[href^="tel"], a[href^="sms"] {
         text-decoration: none;
         color: #0a8cce; /* or whatever your want */
         pointer-events: none;
         cursor: default;
         }
         .mobile_link a[href^="tel"], .mobile_link a[href^="sms"] {
         text-decoration: default;
         color: #0a8cce !important; 
         pointer-events: auto;
         cursor: default;
         }
         table[class=devicewidth] {width: 280px!important;text-align:center!important;}
         table[class=devicewidthinner] {width: 260px!important;text-align:center!important;}
         img[class=banner] {width: 280px!important;height:140px!important;}
         img[class=colimg2] {width: 280px!important;height:140px!important;}
         td[class=mobile-hide]{display:none!important;}
         td[class="padding-bottom25"]{padding-bottom:25px!important;}
        
         }
      </style>
   </head>
  <body>
  <!-- Start of preheader -->
<table width="100%" bgcolor="#ffffff" cellpadding="0" cellspacing="0" border="0" id="backgroundTable" st-sortable="preheader" >
   <tbody>
      <tr>
         <td>
            <table width="600" cellpadding="0" cellspacing="0" border="0" align="center" class="devicewidth">
               <tbody>
                  <tr>
                     <td width="100%">
                        <table width="600" cellpadding="0" cellspacing="0" border="0" align="center" class="devicewidth">
                           <tbody>
                              <!-- Spacing -->
                              <tr>
                                 <td width="100%" height="50">&nbsp;</td>
                              </tr>

                              <!-- Spacing -->
                              <tr>
                                 <td>
                                    <table width="100" align="right" border="0" cellpadding="0" cellspacing="0" class="devicewidth">
                                       <tbody>
                                          <tr >
                                             <td align="left" width="20" style="font-size:1px; line-height:1px;">                                                
                                                <img src="http://roofpik.com/img/icon/logo.png" alt="Roofpik" border="0"  height="32" style="display:inline; border:none; outline:none; text-decoration:none; margin-right:30px;">
                                             </td>
                                          </tr>
                                       </tbody>
                                    </table>
                                 </td>
                              </tr>
                              <!-- Spacing -->
                              <tr>
                                 <td width="100%" height="10"></td>
                              </tr>
                              <!-- Spacing -->
                           </tbody>
                        </table>
                     </td>
                  </tr>
               </tbody>
            </table>
         </td>
      </tr>
   </tbody>
</table>
<!-- End of preheader -->       


<!-- Start Full Text -->
<table width="100%" bgcolor="#ffffff" cellpadding="0" cellspacing="0" border="0" id="backgroundTable" st-sortable="full-text">
   <tbody>
      <tr>
         <td>
            <table width="600" cellpadding="0" cellspacing="0" border="0" align="center" class="devicewidth">
               <tbody>
                  <tr>
                     <td width="100%">
                        <table width="600" cellpadding="0" cellspacing="0" border="0" align="center" class="devicewidth">
                           <tbody>
                              <!-- Spacing -->
                              <tr>
                                 <td height="20" style="font-size:1px; line-height:1px; mso-line-height-rule: exactly;">&nbsp;</td>
                              </tr>
                              <!-- Spacing -->
                              <tr>
                                 <td>
                                    <table width="560" align="center" cellpadding="0" cellspacing="0" border="0" class="devicewidthinner">
                                       <tbody>
                                    
                                          <!-- spacing -->
                                          <tr>
                                             <td width="100%" height="20" style="font-size:1px; line-height:1px; mso-line-height-rule: exactly;">&nbsp;</td>
                                          </tr>
                                          <!-- End of spacing -->
                                          <!-- content -->
                                          <tr>
                                             <td style="font-family: Helvetica, arial, sans-serif; font-size: 16px; color: #666666; text-align:left; line-height: 30px; padding:0 0 30px;" st-content="fulltext-content">
                                                You have selected 


	"""
	html2 = """

        as your new Roofpik ID. To verify this email address belongs to you, click the link below:

                                             </td>
                                          </tr>

                                          <tr>
                                             <td style="font-family: Helvetica, arial, sans-serif; font-size: 16px; color: #666666; text-align:left; line-height: 30px;" st-content="fulltext-content">
                                               <a href="
	"""

	html3 = """

" style=" color: #ffffff; font-size: 16px; background: #3498db; padding: 10px 20px 10px 20px; text-decoration: none;" >Verify Email</a>

                                             </td>
                                          </tr>

                                           <tr>
                                             <td style="font-family: Helvetica, arial, sans-serif; font-size: 16px; color: #666666; text-align:left; line-height: 30px; font-weight:700; padding:20px 0;" st-content="fulltext-content">
                                                Why you received this email?

                                             </td>
                                          </tr>

                                          <tr>
                                             <td style="font-family: Helvetica, arial, sans-serif; font-size: 16px; color: #666666; text-align:left; line-height: 30px; padding:10px 0;" st-content="fulltext-content">
                                                Roofpik requires verification whenever an email address is selected as an Roofpik ID. Your email cannot be used until you verify it.
                                                


                                             </td>
                                          </tr>

                                            <tr>
                                             <td style="font-family: Helvetica, arial, sans-serif; font-size: 16px; color: #666666; text-align:left; line-height: 30px; padding:10px 0;" st-content="fulltext-content">
                                               
                                               If you did not make this request, you can ignore this email. No Roofpik ID will be created without verification.
                                               

                                             </td>
                                          </tr>

                                            <tr>
                                             <td style="font-family: Helvetica, arial, sans-serif; font-size: 16px; color: #666666; text-align:left; line-height: 30px; padding:20px 0 0;" st-content="fulltext-content">
                                               
                                             Team Roofpik
                                               

                                             </td>
                                          </tr>
                                          <!-- End of content -->
                                       </tbody>
                                    </table>
                                 </td>
                              </tr>
                              <!-- Spacing -->
                              <tr>
                                 <td height="20" style="font-size:1px; line-height:1px; mso-line-height-rule: exactly;">&nbsp;</td>
                              </tr>
                              <!-- Spacing -->
                           </tbody>
                        </table>
                     </td>
                  </tr>
               </tbody>
            </table>
         </td>
      </tr>
   </tbody>
</table>
<!-- end of full text -->

<!-- Start of seperator -->
<table width="100%" bgcolor="#ffffff" cellpadding="0" cellspacing="0" border="0" id="backgroundTable" st-sortable="seperator">
   <tbody>
      <tr>
         <td>
            <table width="600" align="center" cellspacing="0" cellpadding="0" border="0" class="devicewidth">
               <tbody>
                  <tr>
                     <td align="center" height="30" style="font-size:1px; line-height:1px;">&nbsp;</td>
                  </tr>
                  <tr>
                     <td width="550" align="center" height="1" bgcolor="#d1d1d1" style="font-size:1px; line-height:1px;">&nbsp;</td>
                  </tr>
                  <tr>
                     <td align="center" height="30" style="font-size:1px; line-height:1px;">&nbsp;</td>
                  </tr>
               </tbody>
            </table>
         </td>
      </tr>
   </tbody>
</table>
<!-- End of seperator -->   


<!-- Start of seperator -->
<table width="100%" bgcolor="#ffffff" cellpadding="0" cellspacing="0" border="0" id="backgroundTable" st-sortable="seperator">
   <tbody>
      <tr>
         <td>
            <table width="600" align="center" cellspacing="0" cellpadding="0" border="0" class="devicewidth">
               <tbody>
                  <tr>

                     <td align="center" height="30" style="font-size:1px; line-height:1px;">&nbsp;</td>
                  </tr>
                  <tr>
                    
                  <td align="center" valign="middle" style="font-family: Helvetica, arial, sans-serif; font-size: 12px;color: #666666; line-height:40px;" st-content="postfooter">
                                   Roofpik.com, 250 Vipul Trade Center, Sector 48, Gurgaon, India 122018 <a href="#" style="text-decoration: none; color: #0a8cce">contact@roofpik.com</a> 
                                 </td>

                   </tr>

<tr>
			<td align="center" valign="middle" style="font-family: Helvetica, arial, sans-serif; font-size: 12px;color: #666666; line-height:40px;" st-content="postfooter">
                                    Want to Unsubscribe? We're sorry to see you go, but happy to make it easy on you. <a href="#" style="text-decoration: none; color: #0a8cce">Unsubscribe</a> 
                                 </td>

                   </tr>



                  <tr>
                     <td align="center" height="30" style="font-size:1px; line-height:1px;">&nbsp;</td>
                  </tr>
               </tbody>
            </table>
         </td>
      </tr>
   </tbody>
</table>
<!-- End of seperator -->  



  </body>
</html>
	"""
	finalHtml = html + email + html2 + "http://139.162.3.205/verify-email/#/verify?id="+userid+"&email="+email+"&code="+code + html3
	return finalHtml

def sendMail(email, code, userid):
#	return "arpit"


	













	client = sendgrid.SendGridClient("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")
	message = sendgrid.Mail()
	html = emailHtml(email, code, userid)
	message.add_to(email)
	message.set_from("no-reply@roofpik.com")
	message.set_subject("Verify your roofpik account email address")
#	message.set_html("<html><head></head><body><a href='http://139.162.3.205/verify-email/#/verify?id="+userid+"&email="+email+"&code="+code+"'>Click here</a> to verify your email.</body></html>")
	message.set_html(html)
	result = client.send(message)
	if str(result[0]) == '200':
		return True
	return False	


def validateEmail(email):
	return re.match(r'.*@.*\..*', email)

def validatePhone(phone):
	return (re.match(r'\d{10}', phone))

def genActivationCode():
	return '-'.join(str(random.randint(1000,9999)) for i in range(4))

def genReferralCode():
	chars = "".join( [random.choice(string.letters) for i in xrange(4)] )
	return chars+str(random.randint(1000,9999))

class addNewUser(Resource):
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('name', type=str)
		parser.add_argument('email', type=str)
#		parser.add_argument('password', type=str)
		parser.add_argument('mobileNum', type=str)
		parser.add_argument('referralCode', type=str)
                parser.add_argument('deviceId', type=str)

		args = parser.parse_args()
		_name = args['name']
		_email = args['email']
#		_password = args['password']
		_mobile_num = args['mobileNum']
		_referral_code = args['referralCode']
                _device_id = args['deviceId']
		
#		if not all([_name, _email, _password, _mobile_num]):
		if not all([_name, _email, _mobile_num]):
			return {'StatusCode':'400', 'Message':'Please enter all the required details correctly'}
		if not validateEmail(_email):
			return {'StatusCode':'400', 'Message':'Please enter a valid email address'}
		if not validatePhone(str(_mobile_num)):
			return {'StatusCode':'400', 'Message':'Please enter a 10 digit mobile number'}
	
		fire_users = firedb.roofpik_connect('users/data', auth = True)

		users = fire_users.get()
		if users:
			for user in users:
#				return user
				if users[user]['email']['userEmail'] == _email:
					if users[user]['email']['emailFlag'] == False:
						sendMail(_email, users[user]['email']['code'], user)
						return {'StatusCode':'200', 'Message':'An email has been re-sent to ' + _email + ' with the verification link.'}
					else:
						return {'StatusCode':'400', 'Message':'This email is already registered'}
				if users[user]['mobile']['mobileNum'] == _mobile_num:
					if users[user]['email']['emailFlag'] == False and users[user]['email']['userEmail'] == _email:
                                                sendMail(_email, users[user]['email']['code'], user)
                                                return {'StatusCode':'200', 'Message':'An email has been re-sent to ' + _email + ' with the verification link.'}
					else:
                                                return {'StatusCode':'400', 'Message':'This mobile is already registered'}
		# _password = md5.md5(_password).hexdigest()
		_code = genActivationCode()
		_my_referral_code = genReferralCode()

		data = {
			'name' : _name,
#			'password' : _password,
			'createdTime' : str(datetime.datetime.now()),
			'activeFlag' : True,
                        'deviceId': _device_id,
			'referralCode' : _referral_code,
			'myReferralCode' : _my_referral_code,
			'email' : {
				'userEmail' : _email,
				'code' : _code,
				'activeFlag' : True,
				'usedFlag' : False,
				'emailFlag' : False,
				'createdTime' : str(datetime.datetime.now())
			},
			'mobile' : {
				'mobileNum' : _mobile_num,
				'mobileFlag' : False
			}
		}

		result = fire_users.post(data)
		_user_id = result['name']

		sendMail(_email, _code, _user_id)		

		return {'StatusCode':'200', 'Message':'An email has been sent to ' + _email + ' with the verification link.'}
