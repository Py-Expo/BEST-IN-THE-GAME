from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'adhithya@2005'
app.config['MYSQL_DB'] = 'flask'

SENDER_EMAIL = 'thyaa4752@gmail.com'
SENDER_PASSWORD = 'kvvk hoiz hfiw enbk'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
TIMEOUT = 100


app.config['UPLOAD_FOLDER'] = 'uploads/'

mysql = MySQL(app)

@app.route("/")
def admin():
    return render_template("admin.html")

@app.route("/login", methods=['GET'])
def login():
    return render_template("login.html")

@app.route("/logincheck", methods=["POST", "GET"])
def logincheck():
    email = request.form.get('email')
    password = request.form.get('password')
    print(email, password)
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
    user = cur.fetchone()
    cur.close()
    print(user)

    if user: 
        return redirect('/upload')
    else:
        return '''
        <script>
            alert("Login unsuccessfully");
            window.location.href = '/login'; // Redirect to login page
        </script>
        '''

@app.route("/register", methods=['GET'])
def register():
    return render_template("register.html")    

@app.route("/registersave", methods=['POST'])
def registersave():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
    mysql.connection.commit()

    cur.close()
    return redirect('/login')
    
    
    
    
    

    # Assuming the registration is successful, redirect to the login page
    return redirect('/login')

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/savefile' , methods=['POST'])
def savefile():
    # Read the file content
    file = request.files['document']
    filename = file.filename
    print(app.config['UPLOAD_FOLDER'], filename)
        # Create the upload directory if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    with open(file_path, "rb") as file:
        file_data = file.read()

    # Insert the file data into the database
    insert_query = "INSERT INTO files (file_name,file_data) VALUES (%s,%s)"
    cur = mysql.connection.cursor()
    cur.execute(insert_query, (filename,file_data,))
    mysql.connection.commit()

    # Close the connection
    cur.close()
    send_email("Test","test.com",file,file_path)
    return render_template('upload.html')

def fetchemail():
    return "thyaa4752@gmail.com"

def fetchcc():
    return "dhanvanth.2301@gmail.com"

@app.route('/approve_document', methods=['POST','GET'])
def approve_leave_request():
    return render_template('response.html', message="Your document has been approved.")


@app.route('/decline_document', methods=['POST','GET'])
def decline_leave_request():
    return render_template('response.html', message="Your document has been declined.")
    
def send_email(sender_name, sender_email, document, file_path):
    receiver_email=fetchemail()
    cc_email=fetchcc()
    # Create message container
    msg = MIMEMultipart()
    msg['Subject'] = 'Document Approval Request'
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver_email  # Replace with principal's email
    msg['Cc'] = cc_email

    # Email body with HTML content
    body = f"""\
    <html>
    <head></head>
    <body>
        <p>Dear Sir/Madam,</p>
        <p>{ SENDER_EMAIL } has submitted a document approval request:</p>
        <p>Please click one of the following buttons to approve or decline this request:</p>
        <form action="http://127.0.0.1:5000/approve_document" method="post">
            <input type="submit" value="Approve">
        </form>
        <form action="http://127.0.0.1:5000/decline_document" method="post">
            <input type="submit" value="Decline">
        </form>
        <p>Thank you.</p>
    </body>
    </html>
    """
    
    filename = document.name[8:]
    attachment_path = file_path

    # Open the file to be attached
    with open(attachment_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)

    # Attach body as HTML to email
    part.add_header(
    "Content-Disposition",
    f"attachment; filename={ filename }",
)
    msg.attach(part)
    msg.attach(MIMEText(body, 'html'))

    # Connect to SMTP server and send email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=TIMEOUT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
    
    

if __name__ == '__main__':
    app.run(debug=True)
