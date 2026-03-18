from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from model import db, User, Issue
from config import Config
from datetime import datetime
import os
import json

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()
    print("✅ Database created!")

LOCALITIES = []
try:
    with open('localities.json', 'r') as f:
        locality_data = json.load(f)
        LOCALITIES = list(locality_data.keys())
except:
    LOCALITIES = ['vaishali', 'indirapuram', 'raj_nagar', 'vasundhara']

@app.route('/')
def home():
    return render_template('landing.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!')
            return redirect(url_for('dashboard'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username taken')
            return redirect(url_for('register'))
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registered! Please login.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    issues = Issue.query.order_by(Issue.created_at.desc()).limit(20).all()
    return render_template('dashboard.html', issues=issues, localities=LOCALITIES)

@app.route('/report', methods=['GET', 'POST'])
@login_required
def report_issue():
    if request.method == 'POST':
        issue = Issue(
            title=request.form['title'],
            description=request.form['description'],
            category=request.form['category'],
            locality=request.form['locality'],
            created_by=current_user.id
        )
        db.session.add(issue)
        db.session.commit()
        flash('Issue reported!')
        return redirect(url_for('dashboard'))
    return render_template('report.html', localities=LOCALITIES)

@app.route('/issue/<int:id>')
@login_required
def issue_detail(id):
    issue = Issue.query.get_or_404(id)
    return render_template('issue_detail.html', issue=issue)

@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash('Admin only!')
        return redirect(url_for('dashboard'))
    issues = Issue.query.all()
    return render_template('admin.html', issues=issues)

@app.route('/admin/update_status/<int:id>', methods=['POST'])
@login_required
def update_status(id):
    if not current_user.is_admin:
        return jsonify({'error': 'Admin only'}), 403
    issue = Issue.query.get_or_404(id)
    issue.status = request.form['status']
    issue.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify({'success': True, 'status': issue.status})

@app.route('/issues')
@login_required
def issues():
    issues_list = Issue.query.order_by(Issue.created_at.desc()).all()
    return render_template('issues.html', issues=issues_list, localities=LOCALITIES)


@app.route('/hall_of_shame')
def hall_of_shame():
    metrics = db.session.query(
        Issue.locality,
        db.func.count().label('total'),
        db.func.sum(
            db.case(
                (Issue.status != 'Resolved', 1),
                else_=0
            )
        ).label('unresolved')
    ).group_by(Issue.locality).all()

    try:
        with open('localities.json', 'r') as f:
            contacts = json.load(f)
    except:
        contacts = {}

    return render_template('hall_of_shame.html', metrics=metrics, contacts=contacts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('user_profile.html')

if __name__ == '__main__':
    os.makedirs('instance', exist_ok=True)
    app.run(debug=True, port=5000)
