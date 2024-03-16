from flask import Flask, render_template, request, redirect, url_for
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

# Replace these with your actual email credentials
SENDER_EMAIL = 'yourmailid@gmail.com'
SENDER_PASSWORD = 'app password'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_leave_request', methods=['POST'])
def submit_leave_request():
    sender_name = request.form['sender_name']
    sender_email = request.form['sender_email']
    leave_reason = request.form['leave_reason']

    # Send leave request email to principal
    send_leave_request_email(sender_name, sender_email, leave_reason)

    return redirect(url_for('index'))

def send_leave_request_email(sender_name, sender_email, leave_reason):
    # Create message container
    msg = MIMEMultipart()
    msg['Subject'] = 'Leave Request'
    msg['From'] = SENDER_EMAIL
    msg['To'] = 'principalmailid@gmail.com'  # Replace with principal's email

    # Email body with HTML content
    body = f"""\
    <html>
    <head></head>
    <body>
        <p>Dear Principal,</p>
        <p>{sender_name} ({sender_email}) has submitted a leave request:</p>
        <p><strong>Reason:</strong> {leave_reason}</p>
        <p>Please click one of the following buttons to approve or decline this request:</p>
        <form action="http://127.0.0.1:5000/approve_leave_request" method="post">
            <input type="submit" value="Approve">
        </form>
        <form action="http://127.0.0.1:5000/decline_leave_request" method="post">
            <input type="submit" value="Decline">
        </form>
        <p>Thank you.</p>
    </body>
    </html>
    """

    # Attach body as HTML to email
    msg.attach(MIMEText(body, 'html'))

    # Connect to SMTP server and send email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, 'principalmailid@gmail.com', msg.as_string())

@app.route('/approve_leave_request', methods=['POST'])
def approve_leave_request():
    # Handle approval logic here
    # For simplicity, we'll just redirect to index page
    return redirect(url_for('index'))

@app.route('/decline_leave_request', methods=['POST'])
def decline_leave_request():
    # Handle decline logic here
    # For simplicity, we'll just redirect to index page
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)