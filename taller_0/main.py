from flask import Flask,render_template,request,redirect,url_for,Response,session
from flask_sqlalchemy  import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = "abcd1234"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/taller_0.db'
db = SQLAlchemy(app)

### Create models sqlite3
class Register(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200))
    password = db.Column(db.String(8))
    name = db.Column(db.String(100))

class Task(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200))
    content = db.Column(db.String(200))
    date_start =db.Column(db.DateTime)
    date_end = db.Column(db.DateTime)
    category  = db.Column(db.String(200))
    place = db.Column(db.String(200))
    address = db.Column(db.String(200))
    type = db.Column(db.String(200))
### create URL and functions$

@app.route('/')
def Index():
    if 'email' in session:
        tasks = Task.query.filter_by(email= session['email']).order_by(Task.date_start.desc())
        return render_template('events.html',tasks=tasks)
    else:
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
        session['email'] = email
        return redirect(url_for('Index'))
    return redirect(url_for('Index'))

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
            return render_template('login.html')
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
            return render_template('login.html')
        else:
            return Response("{'menssage':'Email or password not found'}", status=404, mimetype='application/json')

@app.route('/create-task',methods=['POST'])
def create():
    if request.form.get('content') is not None:
        print(type(request.form['date_start']))
        print(request.form['date_start'])
        task = Task(date_start = datetime.strptime(request.form['date_start'],"%Y-%m-%d"),
                    date_end = datetime.strptime(request.form['date_end'],"%Y-%m-%d"),
                    category=request.form['category'],
                    place=request.form['place'],
                    address=request.form['address'],
                    type = request.form['type'],
                    content = request.form['content'],
                    email=session['email']
                    )
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('Index'))
    elif request.json.get('content') is not None:
        print(request.json)
        task = Task(date_start = datetime.strptime(request.json.get('date_start'), "%Y-%m-%d"),
                    date_end = datetime.strptime(request.json.get ('date_end'), "%Y-%m-%d"),
                    category = request.json.get('category'),
                    place = request.json.get('place'),
                    address = request.json.get('address'),
                    type = request.json.get('type'),
                    content = request.json.get('content'),
                    email = session['email']
                    )
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('Index'))

    else:
        return Response("{'menssage':'data not add'}",status=401,mimetype='application/json')

@app.route('/delete/<id>')
def delete(id):
    task = Task.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('Index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('Index'))

@app.route('/register',methods=['POST','GET'])
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(port=8080,debug=True)

