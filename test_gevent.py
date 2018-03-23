from gevent import monkey; monkey.patch_all()

from time import sleep
from bottle import route, run, get, template


#THIS WILL STILL RUN EVEN IF WE GO TO http://localhost:8080/ which is below
@route('/stream')
def stream():
    print 'START'
    sleep(3)
    print 'MIDDLE'
    sleep(10)
    print 'END'

@route('/')
def default():
    return template('login')

# Static Routes
#USED for our CSS, JS and other assets
@get('/<filename:path>')
def static(filename):
    return static_file(filename, root='static/')

run(host='0.0.0.0', port=8080, server='gevent')
