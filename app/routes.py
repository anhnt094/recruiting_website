import json
import requests

from app import app, db
from app.models import User, Job
from app.forms import LoginForm, RegistrationForm
from dateutil import parser
from flask import render_template, flash, redirect, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from markdown2 import Markdown
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
#@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home Page', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            return redirect(url_for('index'))
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/job_lists')
def job_lists():
    request_new_data()
    # job_lists = Job.query.all()
    # return render_template('job_lists.html', title='Job lists', job_lists=job_lists)
    return redirect(url_for('jobs_per_page', page_num=1))



@app.route('/job_lists/<int:jobID>')
def job_descriptions(jobID):
    job = Job.query.filter_by(github_issues_number=jobID).first()
    if not job:
        return 'Job not found !'
    markdowner = Markdown()
    return render_template('job_descriptions.html', title='Job descriptions', job=job, content=markdowner.convert(job.content))


@app.route('/job_lists/p/<int:page_num>')
def jobs_per_page(page_num):
    jobs = Job.query.paginate(per_page=10, page=page_num, error_out=True)
    return render_template('jobs_per_page.html', title='Jobs per page', jobs=jobs)


def request_new_data():
    # url = 'https://api.github.com/repos/awesome-jobs/vietnam/issues?state=open&page=1&per_page=100'
    url = 'https://api.github.com/repos/awesome-jobs/vietnam/issues?state=open&page=1&per_page=100'
    resp = requests.get(url)
    results = json.loads(resp.text)
    for result in results:
        exist_job = Job.query.filter_by(github_issues_number=result['number']).first()
        if exist_job:
            break
        else:
            job = Job(title=result['title'],
                github_url=result['html_url'],
                github_issues_number=result['number'],
                author=result['user']['login'],
                created_time=parser.parse(result['created_at']),
                updated_time=parser.parse(result['updated_at']),
                content=result['body'])

            db.session.add(job)
            db.session.commit()


