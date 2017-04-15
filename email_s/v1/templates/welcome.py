# -*- coding: utf-8 -*-
from string import Template

def welcomeTemplate(name):


	html = """\

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <!-- utf-8 works for most cases -->
    <meta name="viewport" content="width=device-width">
    <!-- Forcing initial-scale shouldn't be necessary -->
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <!-- Use the latest (edge) version of IE rendering engine -->
    <meta name="x-apple-disable-message-reformatting">
    <!-- Disable auto-scale in iOS 10 Mail entirely -->
    <title>Welcome to Roofpik</title>
    <!-- The title tag shows in email notifications, like Android 4.4. -->
    <!-- Web Font / @font-face : END -->
    <!-- CSS Reset -->
    
</head>

<body width="100%" style="margin: 0; mso-line-height-rule: exactly;">


        <div>
           <style>
              body {
              margin: 0;
              background-color: #fafafa;
              }
              h4,
              p,
              h5,
              h3 {
              margin: 5px;
              }
           </style>
           <table style="font-size: 12px;  width: 100%; background-color: #fff; max-width: 650px; padding: 0 15px;        font-family: arial; border: 1px solid #eee; margin: 0 auto;">
              <tr>
                 <td colspan="2" style=" border-bottom: 1px dashed #ddd; padding-top: 15px; padding-bottom: 15px; line-height: 21px; color: #333;" "><img src="http://cdn.roofpik.com/emailer/cover.png" width="100% " /></td>
              </tr>
              <tr>
                 <td colspan="2 " style="padding-top: 15px; padding-bottom: 15px; line-height: 21px; color: #333; ">
                    Dear $name, <br><br>
                    <b>We’re glad to see you here!</b>
                    <br>
                    <br>               
                    <i>  We bring reviews "To the people", "By the people", "For the People"</i> 
                    <br><br> 
                    <b>Welcome</b> to the first of kind real estate community, we have thousands of reviews by verified residents. With a huge number of reviews and experiences, Roofpik can help you find your next home. Compare and select from 100's of properties to find a place that is best suited for you.   <br><br> 
                    Our unique property ranking and reviewing system helps make your choice simpler and easier.  <br> <br>            
                    
                    <i>Genuine Reviews  |  Validated Project Information | Trusted Agents  </i>
                 </td>
              </tr>
              <tr>
                 <td colspan="2 " style="padding-top: 15px; padding-bottom: 15px; line-height: 21px; color: #333; ">
                    Best Regards,<br>
                    Kanika S Katoch  (Co-Founder, Roofpik)<br><br>
                    Roofpik | 250,Second Floor, Vipul Trade Centre, Sohna Road, Sector-48, Gurgaon, 122018 | 
                 </td>
              </tr>
           </table>
        </div>


</body>

</html>



"""

	return Template(html).safe_substitute(name=name)