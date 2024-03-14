from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'adhithya@2005'
app.config['MYSQL_DB'] = 'flask'

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
    
    
    
    
    

    # Assuming the registration is successful, redirect to the login page
    return redirect('/login')

@app.route('/upload')
def upload():
    return render_template('upload.html')
    

if __name__ == '__main__':
    app.run(debug=True)
