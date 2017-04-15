# -*- coding: utf-8 -*-
from string import Template

def reviewTemplate(name, project):


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
         <td colspan="2" style=" border-bottom: 1px dashed #ddd; padding-top: 15px; padding-bottom: 15px; line-height: 21px; color: #333;""><img src="ROOFPIK-COVER-PHOTO.png" width="100%" /></td>
      </tr>
      <tr>
         <td colspan="2" style="padding-top: 15px; padding-bottom: 15px; line-height: 21px; color: #333;">
            Dear $name, <br><br>
            <i>Thank you for contributing- "It Matters A Lot"</i>
            <br>
            <br>
            <i>  We bring reviews"To the people", "By the people", "For the People"</i>               
            Over <b>4000 genuine reviews</b> to help you Buy, Sell or Rent
            Read them at <a href="http://www.roofpik.com/"> roofpik</a>
            <br>
            <br> Roofpik is an "unbiased and neutral platform" that is just a click away. So no more tiring search to find genuine reviews, sweaty visits to numerous properties, localities to choose one for your self.
            <br>
            <br> Roofpik is NOT just another property search portal
            <br>
            <br>
             <i>Genuine Reviews  |  Validated Project Information | Trusted Agents  </i>
         </td>
      </tr>
      <tr>
         <td colspan="2" style="padding-top: 15px; padding-bottom: 15px; line-height: 21px; color: #333;">
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

	return Template(html).safe_substitute(name=name, project=project)