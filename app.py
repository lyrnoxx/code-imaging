from flask import Flask, render_template, session,url_for,request,redirect

from pygments import highlight 
from pygments.formatters import HtmlFormatter
from pygments.lexers import Python3Lexer
from pygments.styles import get_all_styles

app=Flask(__name__)
app.secret_key="haa"

PLACEHOLDER="print('Hello, World!')"
DEFAULT_STYLE='monokai'

@app.route('/',methods=['GET'])
def code():
    if session.get('code') is None:
        session['code']=PLACEHOLDER
    lines=session['code'].split('\n')
    context={"message":"Paste your python code",
             'code':session['code'],
             'num_lines':len(lines),
             'max_chars':len(max(lines,key=len))
             }
    return render_template("code_input.html",**context)

@app.route("/save_code",methods=['POST'])
def save_code():
    session['code']=request.form.get('code')
    return redirect(url_for('code'))

@app.route('/reset_session',methods=['POST'])
def reset_session():
    session.clear()
    session['code']=PLACEHOLDER
    return redirect(url_for('code'))

@app.route('/style',methods=['GET'])
def style():
    if session.get('style') is None:
        session['style'] =DEFAULT_STYLE
    formatter=HtmlFormatter(style=session['style'])
    context={
        'message':'Select your style',
        'all_styles':list(get_all_styles()),
        'style_definitions':formatter.get_style_defs(),
        'style_bg_color':formatter.style.background_color,
        'highlighted_code':highlight(
        session['code'],Python3Lexer(),formatter
        ),
    }
    return render_template("style_selection.html",**context)

@app.route('/save_style',methods=['POST'])
def save_style():
    if request.form.get('style') is not None:
        session['style']=request.form.get('style')
    if request.form.get('code') is not None:
        session['code']=request.form.get('code')
    return redirect(url_for('style'))