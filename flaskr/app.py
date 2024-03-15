from flask import Flask, render_template, send_from_directory, url_for, request, session, redirect, abort, Response, flash
from flask_login import LoginManager, UserMixin, \
                                login_required, login_user, logout_user, current_user
import os
import __modules__.paginate as paginate
import __modules__.getsize as calcLogSize
import __modules__.getfiles as getfiles
from datetime import timedelta

# config
PER_PAGE = 6
app = Flask(__name__)
app.secret_key = "secret_xx"
app.permanent_session_lifetime = timedelta(seconds=1000000)
app.config['UPLOAD_FOLDER'] = 'C:\\Users\\em.vannin\\Documents\\scripts\\projects\\acs-web-portal\\tests\\access_logs'

# config: login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# silly user model
class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.name = "user" + str(id)
        self.password = self.name + "_secret"
        
users = [User(id) for id in range(1,5)]

@app.before_request
def before_request():
    session.permanent = True
    session.modified = True

@app.route('/')
def home():
    return redirect(url_for('login'))

# protected urls
@app.route("/list", methods=["GET", "POST"])
@login_required
def list_files():
    if not current_user.is_authenticated:
        print("NOT AUTHORIZED")
        return Response("NOT AUTHORIZED")
    
    search_term = request.form.get("search")
    directory = app.config['UPLOAD_FOLDER']
    
    if not search_term:
        search_term = session.get('search_term', "")
    if search_term:
        session['search_term'] = search_term

    if request.method == "POST":
        submitted_action = request.form.get("submit_action")
        if submitted_action == "search":
            if not search_term:
                search_term = session.get('search_term', "")
            if search_term:
                session['search_term'] = search_term
        elif submitted_action == "clear":
            session.pop('search_term', None)
            search_term = ""
    
    logs = getfiles.get_files(directory, search_term, os)
    paginated_log, page, prev_url, next_url, total_pages, links = paginate.paginator('list_files', logs, request, PER_PAGE, url_for)
    
    log_info = []
    for log in paginated_log:
        log_path = os.path.join(directory, log)
        size = os.path.getsize(log_path)
        log_size = calcLogSize.get_size(size)
        log_info.append({'filename': log, 'size': log_size})
    return render_template('index.html', index=page, logs=log_info, paginated_log=paginated_log, page=page, prev_url=prev_url, next_url=next_url, total_pages=total_pages, links=links, search_term=search_term)

@app.route('/download/<filename>')
@login_required
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/view/<filename>')
@login_required
def view_file(filename):
    try:
        file_to_read = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        with open(file_to_read, 'r') as f:
            file_content = f.read()
    except FileNotFoundError:
        return f"File not found: {filename}"
    except Exception as e:
        return f"Error reading file: {e}"
    
    return render_template('viewer.html', content=file_content, filename=filename)

# somewhere to login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if password == username + "_secret":
            id = username.split('user')[1]
            user = User(id)
            login_user(user)
            return redirect(url_for('list_files'))
        else:
            flash("Incorrect Credentials!", category="message")
            return redirect(url_for('login'))
        
    return render_template('login.html')

# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')

# unauthorized callback
@login_manager.unauthorized_handler
def unauthorized_callback():
    flash("You are not authorized!", category="message")
    return redirect(url_for('login'))

# callback to reload the user object
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# unit test in loopback
if __name__ == '__main__':
    app.run(port=5000, debug=True)