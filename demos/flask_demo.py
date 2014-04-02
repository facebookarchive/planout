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

from planout.experiment import SimpleExperiment
from planout.ops.random import *

class HeaderExperiment(SimpleExperiment):
    def assign(self, params, userid):
        params.header_text= UniformChoice(choices=['Hi', 'Hello'], unit=userid)
        params.header_color = UniformChoice(choices=['#aa332a', '#4422e5'],
            unit=userid)

@app.route('/')
def main():
    # if no userid is defined make one up
    if 'userid' not in session:
        session['userid'] = str(uuid4())

    header_exp = HeaderExperiment(userid=session['userid'])
    header = header_exp.get('header_text')
    color = header_exp.get('header_color')
    
    return render_template_string("""
    <html>
      <head>
        <title>Welcome to Planout!</title>
      </head>
      <body>
        <h1><font color="{{color}}">{{ header }}</font></h1>
      <form method="POST" action="/reset">
      <input type="submit" value="Reset UserId">
      </body>
    </html>
    """, header=header, color=color)

@app.route('/signup', methods=['POST'])
def reset():
    session.clear()
    return redirect(url_for('main'))


@app.route('/reset', methods=['POST'])
def reset():
    session.clear()
    return redirect(url_for('main'))

if __name__ == '__main__':
    app.run()
    
