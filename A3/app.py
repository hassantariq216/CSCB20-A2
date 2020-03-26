from flask import Flask, redirect, render_template, request, session, abort, g
import sqlite3

app = Flask(__name__)
app.secret_key = 'super secret key'

DATAB='./database.db'

# Connecting database to flask
# Source: https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
def get_db():
	db=getattr(g, '_database', None)

	if db is None:
		db=g._database=sqlite3.connect(DATAB)
	return db

# get results from database through query
# Source: https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# 
# Source: https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

# close connection to database
# Source: https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/', defaults={'name_user': ''})
def home(name_user):
	if not session.get('logged_in'):
		if name_user=='error':
			return render_template('login.html', value="Error: Incorrect Username and/or Password")
		else:
			return render_template('login.html')
	else:
		return render_template('welcomeScreen.html', value=name_user)

@app.route('/login', methods=['POST'])
def authorize_login():

	db=get_db()

	#put data from db into dict form for iterations
	db.row_factory = make_dicts 

	# debug_arr=[]
	student=[]
	teacher=[]
	for user in query_db('select * from student'):
		if request.form['username']==list(user.values())[0] and request.form['password']==list(user.values())[1]:
			session['logged_in']=True
			name_user = list(user.values())[2]

	if not session.get('logged_in'):
		for user2 in query_db('select * from teacher'):
			if request.form['username']==list(user2.values())[0] and request.form['password']==list(user2.values())[1]:
				session['logged_in']=True
				name_user = list(user2.values())[2]
		
	if not session.get('logged_in'):
		name_user='error'

	db.close()
	# return list(debug_arr[1].values())[1].__str__()
	return home(name_user)

@app.route('/home')
def homepage():
	return render_template('index.html')

@app.route('/register')
def reg():
	return render_template('registration.html')

@app.route('/registerform', methods=['POST'])
def register_menu():
	connection=get_db()
	cursor=connection.cursor()
	usern=request.form['usn']
	passw=request.form['psw']
	name_us=request.form['User Type']

	try:
		cursor.execute('INSERT INTO student (s_id,s_password, s_name) VALUES (?,?,?)', (usern,passw, name_us))
		connection.commit()
		message = "success"

	except:
		connection.rollback()
		message="failure"

	finally:
		connection.close()
		# return message
		return render_template('login.html')


if __name__ == "__main__":
	app.run(debug=True)






