from flask import Flask,render_template,request,redirect,url_for,flash,Response
from flask_sqlalchemy  import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/taller_0.db'
db = SQLAlchemy(app)

### Create models sqlite3
class Register(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200))
    password = db.Column(db.String(8))
    name = db.Column(db.String(100))

### create URL and functions

@app.route('/')
def Index():
    return render_template('login.html')

@app.route('/sign_in',methods=['GET','POST'])
def sign_in():
    email = ''
    password = ''
    if request.args.get('emailLogin'):
        email = request.args.get('emailLogin')
        password = request.args.get('passwordLogin')
    else:
        email = request.json.get('emailLogin')
        password = request.json.get('passwordLogin')
    query = Register.query.filter_by(email=email).first()
    if query.password == password:
        return Response("{'menssage':'Session start'}",status=201,mimetype='application/json')
    return Response("{'menssage':'Email or password not found'}", status=404, mimetype='application/json')

@app.route('/sign_up',methods=['GET','POST'])
def sign_up():
    if request.form.get('emailRe') is not None:
        email = request.form["emailRe"]
        query = Register.query.filter_by(email= email).first()
        if query is None:
            register = Register(email=request.form["emailRe"],
                                password=request.form["passwordRe"],
                                name=request.form["nameRe"])
            db.session.add(register)
            db.session.commit()
            return redirect(url_for('login.html'))
        else:
            return Response("{'menssage':'Email or password not found'}", status=404, mimetype='application/json')
    else:
        email = request.json.get("email")
        query = Register.query.filter_by(email=email).first()
        if query is None:
            register = Register(email=request.json.get("email"),
                                password=request.json.get("password"),
                                name=request.json.get("name"))
            db.session.add(register)
            db.session.commit()
            return redirect(url_for('login.html'))
        else:
            return Response("{'menssage':'Email or password not found'}", status=404, mimetype='application/json')

if __name__ == '__main__':
    app.run(port=3000)

