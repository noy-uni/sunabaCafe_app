import os
from flask import Flask, request, url_for, render_template, redirect, make_response, session, abort
from markupsafe import escape
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'Nozomi_Super_Secret_Key'



@app.route('/remember_me/<name>')
def remember_me(name):
  session['user'] = name
  return f"{name}様を、お屋敷の記録台帳に記帳いたしましたわ。"

@app.route('/who_am_i')
def who_am_i():
  name = session.get('user', '名もなき旅人')
  return f"あなたは{name}様ですわね。"

# ……… 保存先の指定 ………
app.config['UPLOAD_FOLDER']  ='static/images'

@app.route('/upload', methods=['GET', 'POST'])
def upload_file_get():
  if request.method == 'POST':
    # 宝箱（request.files）からファイルを取り出しますわ
    if 'the_file' not in request.files:
      return 'ファイルが届いておりませんわ！'

    f = request.files['the_file']

    if f.filename == '':
      return 'ファイルが選択されておりませんわ！'

    # 2. 魔法の関数で名前を浄化し、保存いたします
    filename = secure_filename(f.filename)
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # 3. 無事に保存できたら、完了画面へご案内しますわ
    img_url = url_for('static', filename = f'images/{filename}')
    return f'''
      <h2> 無事にお預かりいたしましたわ！</h2>
      <img src= "{img_url}" style="max-width:500px;">
      <br>
      <a href = "{url_for('upload_file_get')}">戻る</a>
    '''
  # 4. 「見る（GET）」だけなら、静かにフォームを表示します
  return render_template('upload.html')


#……… Cookieを焼きますわ！ ………
@app.route('/set_cookie')
def set_cookie():
    resp = make_response("cookieを差し上げましたわ！")

    resp.set_cookie('username', 'Nozomi')

    return resp

@app.route('/get_cookie')
def get_cookie():
  username = request.cookies.get('username')
  return f"あら、あなたは{username}様ではありませんか！"


@app.route("/")
def index():
  return "お屋敷へようこそですわ！"

@app.route('/login')
def login():
  return 'login'

@app.route('/welcome/<username>')
def welcome_guest(username):
  return f"ようこそ、{username}様。お茶の用意がてきでおりますわ！"

@app.route('/projects/')
def projects():
  return 'The project page'

@app.route('/about')
def about():
  return 'The about page'

@app.route('/post/<int:post_id>')
def show_post(post_id):
  return f'Post {post_id}'

@app.get('/hello')
def hello_get():
  return render_template('hello.html')

@app.post('/hello')
def hello_post():
    name = request.form.get('username')
    return render_template('hello.html', person=name)

@app.route('/secret')
def secret():
  code = request.args.get('code', '合言葉を忘れていらっしゃいますわよ？')

  if code != 'Rose':
    abort(403)

  return f"<h1>お屋敷の秘密の図書館へようこそ。ここだけの内緒話ですわ。<h1>"


@app.route('/test')
def test_args():
    # request.args の中身をそのまま全部見せていただきますわ！
    return str(request.args)

@app.route('/debug_args')
def debug_args():
  return f"URLから届いた中身: {request.args}"

if __name__ == "__main__":
    app.run(debug=True)