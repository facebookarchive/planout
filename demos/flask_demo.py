
import random
from uuid import uuid4
from flask import (
    Flask, 
    session,
    request, 
    redirect,
    url_for, 
    render_template_string
)
app = Flask(__name__)

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='3.14159', # shhhhh
))

from planout import SimpleExperiment, UniformChoice

class HeaderCopy(SimpleExperiment):
    def assign(self, params, userid):
        params.header = UniformChoice(choices=['Hi', 'Hello'], unit=userid)

@app.route('/')
def main():
    if 'userid' not in session:
        session['userid'] = str(uuid4())

    #random.seed(hash(session['userid']))
    #header = random.choice(['Hello', 'Hi'])

    header = HeaderCopy(userid=session['userid']).get('header')
    
    return render_template_string("""
<html>
  <head>
    <title>Welcome to Planout!</title>
  </head>
  <body>
    <h1>{{ header }}</h1>
  <form method="POST" action="/reset">
  <input type="submit" value="Reset UserId">
  </body>
</html>
    """, header=header)

@app.route('/reset', methods=['POST'])
def reset():
    session.clear()
    return redirect(url_for('main'))

if __name__ == '__main__':
    app.run()
    
