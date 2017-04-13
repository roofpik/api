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
    <style>
    html,
    body {
        margin: 0 auto !important;
        padding: 0 !important;
        height: 100% !important;
        width: 100% !important;
        font-family: Helvetica, Lucida Grande, Arial, sans-serif;
        font-size: 12px;
        line-height: 18px;
        color: #666666;
        text-align: justify;
    }
    
    * {
        -ms-text-size-adjust: 100%;
        -webkit-text-size-adjust: 100%;
    }
    
    div[style*="margin: 16px 0"] {
        margin: 0 !important;
    }
    /* What it does: Stops Outlook from adding extra spacing to tables. */
    
    table,
    td {
        mso-table-lspace: 0pt !important;
        mso-table-rspace: 0pt !important;
    }
    /* What it does: Fixes webkit padding issue. Fix for Yahoo mail table alignment bug. Applies table-layout to the first 2 tables then removes for anything nested deeper. */
    
    table {
        border-spacing: 0 !important;
        border-collapse: collapse !important;
        table-layout: fixed !important;
        margin: 0 auto !important;
    }
    
    table table table {
        table-layout: auto;
    }
    /* What it does: Uses a better rendering method when resizing images in IE. */
    
    img {
        -ms-interpolation-mode: bicubic;
    }
    /* What it does: A work-around for iOS meddling in triggered links. */
    
    *[x-apple-data-detectors] {
        color: inherit !important;
        text-decoration: none !important;
    }
    /* What it does: A work-around for Gmail meddling in triggered links. */
    
    .x-gmail-data-detectors,
    .x-gmail-data-detectors *,
    .aBn {
        border-bottom: 0 !important;
        cursor: default !important;
    }
    /* What it does: Prevents Gmail from displaying an download button on large, non-linked images. */
    
    .a6S {
        display: none !important;
        opacity: 0.01 !important;
    }
    /* If the above doesn't work, add a .g-img class to any image in question. */
    
    img.g-img + div {
        display: none !important;
    }
    /* What it does: Prevents underlining the button text in Windows 10 */
    
    .button-link {
        text-decoration: none !important;
    }
    /* What it does: Removes right gutter in Gmail iOS app: https://github.com/TedGoas/Cerberus/issues/89  */
    /* Create one of these media queries for each additional viewport size you'd like to fix */
    /* Thanks to Eric Lepetit @ericlepetitsf) for help troubleshooting */
    
    @media only screen and (min-device-width: 375px) and (max-device-width: 413px) {
        /* iPhone 6 and 6+ */
        .email-container {
            min-width: 375px !important;
        }
    }
    </style>
    <!-- What it does: Makes background images in 72ppi Outlook render at correct size. -->
    <!--[if gte mso 9]>
    <xml>
        <o:OfficeDocumentSettings>
            <o:AllowPNG/>
            <o:PixelsPerInch>96</o:PixelsPerInch>
        </o:OfficeDocumentSettings>
    </xml>
    <![endif]-->
    <!-- Progressive Enhancements -->
    <style>
    /* What it does: Hover styles for buttons */
    
    .button-td,
    .button-a {
        transition: all 100ms ease-in;
    }
    
    .button-td:hover,
    .button-a:hover {
        background: #555555 !important;
        border-color: #555555 !important;
    }
    /* Media Queries */
    
    @media screen and (max-width: 600px) {
        .email-container {
            width: 100% !important;
            margin: auto !important;
        }
        /* What it does: Forces elements to resize to the full width of their container. Useful for resizing images beyond their max-width. */
        .fluid {
            max-width: 100% !important;
            height: auto !important;
            margin-left: auto !important;
            margin-right: auto !important;
        }
        /* What it does: Forces table cells into full-width rows. */
        .stack-column,
        .stack-column-center {
            display: block !important;
            width: 100% !important;
            max-width: 100% !important;
            direction: ltr !important;
        }
        /* And center justify these ones. */
        .stack-column-center {
            text-align: center !important;
        }
        /* What it does: Generic utility class for centering. Useful for images, buttons, and nested tables. */
        .center-on-narrow {
            text-align: center !important;
            display: block !important;
            margin-left: auto !important;
            margin-right: auto !important;
            float: none !important;
        }
        table.center-on-narrow {
            display: inline-block !important;
        }
    }
    </style>
</head>

<body width="100%" bgcolor="#222222" style="margin: 0; mso-line-height-rule: exactly;">
    <center style="width: 100%; background: #222222; text-align: left;">
        <!-- Visually Hidden Preheader Text : BEGIN -->
        <div style="display:none;font-size:1px;line-height:1px;max-height:0px;max-width:0px;opacity:0;overflow:hidden;mso-hide:all;font-family: sans-serif;">
            (Optional) This text will appear in the inbox preview, but not the email body.
        </div>
        <!-- Visually Hidden Preheader Text : END -->
        <!-- Email Header : BEGIN -->
        <!-- Email Header : END -->
        <!-- Email Body : BEGIN -->
        <table role="presentation" aria-hidden="true" cellspacing="0" cellpadding="0" border="0" align="center" width="600" style="margin: auto;" class="email-container">
            <!-- 1 Column Text + Button : BEGIN -->
            <tr>
                <td bgcolor="#ffffff" style="padding: 40px; text-align: left; line-height: 20px; color: #555555;">
                   Dear $name, 
                    <br><br>
                     You now have access to iTunes Connect, our exclusive, partner-facing website. You may access iTunes Connect using the link below: 
                    <br><br>
                     iTunes Connect Log in using the existing username and password for your Apple Developer account. With iTunes Connect, you can enter into a Paid Applications agreement, setup and edit information about your application, view sales and trend information, retrieve financial reports (if applicable), and create new user accounts for other people at your company. If you have any questions regarding your iTunes Connect account please Contact Us. Best Regards, The App Store Team
                    <br>
                    <br>
                    <!-- Button : BEGIN -->
                  
                    <!-- Button : END -->
                </td>
            </tr>
            <!-- 1 Column Text + Button : END -->
            <!-- Background Image with Text : BEGIN -->
         
          
            <!-- 1 Column Text : END -->
        </table>
        <!-- Email Body : END -->
        <!-- Email Footer : BEGIN -->
        <table role="presentation" aria-hidden="true" cellspacing="0" cellpadding="0" border="0" align="center" width="600" style="margin: auto;" class="email-container">
            <tr>
                <td style="padding: 40px 10px;width: 100%;font-size: 12px; font-family: sans-serif; line-height:18px; text-align: center; color: #888888;" class="x-gmail-data-detectors">
                    <webversion style="color:#cccccc; text-decoration:underline; font-weight: bold;">View as a Web Page</webversion>
                    <br>
                    <br> Company Name
                    <br>123 Fake Street, SpringField, OR, 97477 US
                    <br>(123) 456-7890
                    <br>
                    <br>
                    <unsubscribe style="color:#888888; text-decoration:underline;">unsubscribe</unsubscribe>
                </td>
            </tr>
        </table>
        <!-- Email Footer : END -->
    </center>
</body>

</html>






"""

	return Template(html).safe_substitute(name=name)