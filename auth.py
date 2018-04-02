from passlib.apps import custom_app_context as pwd_context
from beaker.middleware import SessionMiddleware

@route('/login', method=['GET'])
@view('login')
def login_form():
    return {}

@route('/login', method=['POST'])
@view('login')
def handle_login():
    #Handles log-in credentials by comparing them to what is in the users collection and sets the login cookie
    username = request.forms.username
    password = request.forms.password
    remember = request.forms.remember
    #Let's confirm these aren't blank
    if username == "" or password == "":
        return {"error":"These can't be blank"}
    #Now let's get the data for the user
    user = users.find_one({"username":username})
    if user is None:
        return {"error":"%s is not a valid user" %(username)}
    #Now let's check that the password is right.
    if pwd_context.verify(password, user['pwdhash']):
        #Success, let's set the session and send them back to the dashboard
        s = bottle.request.environ.get('beaker.session')
        s['logged_in'] = True
        s['username'] = username
        if remember == "on":
            s['session.cookie_expires'] = 60*60*24*30
            s.save()
        redirect("/")
    else:
        return {"error":"Incorrect password"}

@route('/logout', method=['GET'])
def handle_logout():
    s = bottle.request.environ.get('beaker.session')
    s.invalidate()
    redirect("/")

def get_username():
    s = bottle.request.environ.get('beaker.session')
    if "username" in s:
        return s['username']
    else:
	redirect("/login")
        #return None

@route('/register', method=['GET'])
@view('register')
def register_form():
    return {}

@route('/register', method=['POST'])
@view('register')
def handle_register():
    #Handles user registration by adding a new user to the users collection
    username = request.forms.username
    email = request.forms.email
    password1 = request.forms.password1
    password2 = request.forms.password2
    #Let's make sure they aren't all null
    if username == "" or email == "" or password1 == "" or password2 == "":
        return {"error":"You left something blank"}
    #Confirm passwords are the same
    if password1 != password2:
        return {"error":"Passwords don't match"}
    #Let's check the database for this username
    user = users.find_one({"username":username})
    if user is not None:
        return {"error":"Username %s already exists" %(username)}
    #At this point we're ready to create the user, let's hash this password to store it.
    pwdhash = pwd_context.encrypt(password1)
    users.insert({"username":username,"pwdhash":pwdhash,"email":email})
    return {"success":"Username %s created" %(username)}



session_opts = {
    'session.type': 'file',
    'session.data_dir': '/data/web/mybeaker',
    'session.auto': True,
    'session.secret':'ZnJU_XgGQR_r1MccHI_aRqFu-8hj6Nmnednt-dkFbGgOSTiwMmiRlcXTjnzQHzk5U_c='
}

mybeaker = SessionMiddleware(app(), session_opts)
run(app=mybeaker, host=http_server,  port=http_port)
run(host=http_server, port=http_port)
run(reloader=True)
