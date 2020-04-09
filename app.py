from flask import Flask, redirect, render_template, request, session, abort, g
import sqlite3

app = Flask(__name__)
app.secret_key = 'super secret key'

DATAB='./assignment3.db'

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
		return render_template('home.html', value=session['user_name'])

@app.route('/login', methods=['POST'])
def authorize_login():

	db=get_db()

	db.row_factory = make_dicts 

	student=[]
	teacher=[]
	for user in query_db('select * from student'):
		if request.form['username']==list(user.values())[0] and request.form['password']==list(user.values())[1]:
			session['logged_in']=True
			session['user_type']='student'
			session['user_id']=list(user.values())[0]
			name_user = list(user.values())[2]

	if not session.get('logged_in'):
		for user2 in query_db('select * from teacher'):
			if request.form['username']==list(user2.values())[0] and request.form['password']==list(user2.values())[1]:
				session['logged_in']=True
				session['user_type']='teacher'
				session['user_id']=list(user2.values())[0]
				name_user = list(user2.values())[2]
		
	if not session.get('logged_in'):
		name_user='error'

	db.close()
	session['user_name']=name_user

	return home(name_user)

@app.route('/home')
def homepage():
	if not session.get('logged_in'):
		return render_template('login.html', value="Error: Please Log In")
	else:
		return render_template('home.html', value=session['user_name'])

@app.route('/register')
def reg():
	return render_template('registration.html')

@app.route('/logout')
def logout():
	session.clear()
	return render_template('login.html')

@app.route('/registerform', methods=['POST'])
def register_menu():
	connection=get_db()
	cursor=connection.cursor()
	usern=request.form['usn']
	passw=request.form['psw']
	name_us=request.form['name2']
	type_user=request.form['User Type']

	connection.row_factory = make_dicts 

	student=[]
	teacher=[]
	for user in query_db('select * from student'):
		if request.form['usn']==list(user.values())[0]:
			connection.close()
			return render_template('registration.html', value="Error: Username already exists!")

	for user2 in query_db('select * from teacher'):
		if request.form['usn']==list(user2.values())[0]:
			connection.close()
			return render_template('registration.html', value="Error: Username already exists!")
	
	if type_user=='student':
		try:
			cursor.execute('INSERT INTO student (s_id,s_password, s_name) VALUES (?,?,?)', (usern,passw, name_us))
			connection.commit()
			message = "success"
		except:
			connection.rollback()
			message="failure"
		finally:
			connection.close()
			#return
			return render_template('login.html', value="Successfully Registered!")

	else:
		try:
			cursor.execute('INSERT INTO teacher (t_id,t_password, t_name) VALUES (?,?,?)', (usern,passw, name_us))
			connection.commit()
			message = "success"
		except:
			connection.rollback()
			message="failure"
		finally:
			connection.close()
			#return
			return render_template('login.html', value="Successfully Registered!")


@app.route('/feedback', methods=['POST', 'GET'])
def feedback_display():
	if session['user_type']=='teacher' and session.get['logged_in']:
		db=get_db()
		db.row_factory = make_dicts 
		userid=session['user_id']
		feedback=[]
		for user in query_db('select * from feedback where t_id=?', [userid]):
			feedback.append(user)
		db.close()
		return render_template('teacherFeedback.html', value=session['user_name'], user=feedback)

	elif session['user_type']=='student' and session.get['logged_in']:
		db=get_db()
		db.row_factory = make_dicts 
		teacher=[]
		for user4 in query_db('select * from teacher'):
			teacher.append(user4)
		db.close()
		return render_template('studentFeedback.html', user4=teacher, value=session['user_name'])

	else:
		return render_template('login.html', value="Error: Please Log In")

@app.route('/feedbackform', methods=['POST'])
def feedback_form():
	connection=get_db()
	cursor=connection.cursor()
	instructor_name=request.form['instructor option']
	q1_response=request.form['q1']
	q2_response=request.form['q2']
	q3_response=request.form['q3']
	q4_response=request.form['q4']
	q5_response=request.form['q5']
	instructor_id=''

	connection.row_factory = make_dicts

	for user3 in query_db('select * from teacher'):
		if instructor_name==list(user3.values())[2]:
			instructor_id=list(user3.values())[0]

	try:
		cursor.execute('INSERT INTO feedback (t_id, q1, q2, q3, q4, q5) VALUES (?,?,?,?,?,?)', (instructor_id, q1_response, q2_response, q3_response, q4_response, q5_response))
		connection.commit()
		message = "success"
	except:
		connection.rollback()
		message="failure"
	finally:
		connection.close()
		#return
		return render_template('studentFeedback.html', value=session['user_name'], value2="Feedback sent!")


@app.route('/coursematerial')
def coursematerial():
	if not session.get('logged_in'):
		return render_template('login.html', value="Error: Please Log In")
	else:
		return render_template('coursematerial.html', value=session['user_name'])

@app.route('/assignments')
def assignments():
	if not session.get('logged_in'):
		return render_template('login.html', value="Error: Please Log In")
	else:
		return render_template('assignments.html', value=session['user_name'])

@app.route('/calendar')
def calendar():
	if not session.get('logged_in'):
		return render_template('login.html', value="Error: Please Log In")
	else:
		return render_template('calendar.html', value=session['user_name'])

@app.route('/courseteam')
def courseteam():
	if not session.get('logged_in'):
		return render_template('login.html', value="Error: Please Log In")
	else:
		return render_template('courseteam.html', value=session['user_name'])

@app.route('/resources')
def resources():
	if not session.get('logged_in'):
		return render_template('login.html', value="Error: Please Log In")
	else:
		return render_template('resources.html', value=session['user_name'])

@app.route('/grades')
def grades():
	if not session.get('logged_in'):
		return render_template('login.html', value="Error: Please Log In")
	else:
		return render_template('grades.html', value=session['user_name'])


if __name__ == "__main__":
	app.run(debug=True,port=5000)






