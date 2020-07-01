import os
import secrets
#from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db #bcrypt
from flaskblog.forms import PostForm #, RegistrationForm, LoginForm, UpdateAccountForm 
from flaskblog.models import Post #User, 
#from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

@app.route('/search_')
def search_():
    posts = Post.query.all()
    all_titles = Post.query.all()
    return render_template('search_.html', titles = all_titles, posts=posts)

@app.route("/search", methods=['GET', 'POST'])
def search():
    posts = Post.query.all()
    if request.method == "POST":
        form = request.form
        search_value = form["search_string"]
        search = "%{}%".format(search_value)
        results = Post.query.filter(Post.title.like(search)).all()
        return render_template('search_.html', titles = results, title='Search', legend = "Search Results", posts=posts)
    else:
        return redirect("/search_")


#@app.route("/register", methods=['GET', 'POST'])
#def register():
#    if current_user.is_authenticated:
#        return redirect(url_for('home'))
#    form = RegistrationForm()
#    if form.validate_on_submit():
#        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
#        db.session.add(user)
#        db.session.commit()
#        flash('Your account has been created! You are now able to log in', 'success')
#        return redirect(url_for('login'))
#    return render_template('register.html', title='Register', form=form)
#
#
#@app.route("/login", methods=['GET', 'POST'])
#def login():
#    if current_user.is_authenticated:
#        return redirect(url_for('home'))
#    form = LoginForm()
#    if form.validate_on_submit():
#        user = User.query.filter_by(email=form.email.data).first()
#        if user and bcrypt.check_password_hash(user.password, form.password.data):
#            login_user(user, remember=form.remember.data)
#            next_page = request.args.get('next')
#            return redirect(next_page) if next_page else redirect(url_for('home'))
#        else:
#            flash('Login Unsuccessful. Please check email and password', 'danger')
#    return render_template('login.html', title='Login', form=form)
#
#
#@app.route("/logout")
#def logout():
#    logout_user()
#    return redirect(url_for('home'))
#
#
#def save_picture(form_picture):
#    random_hex = secrets.token_hex(8)
#    _, f_ext = os.path.splitext(form_picture.filename)
#    picture_fn = random_hex + f_ext
#    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
#
#    output_size = (125, 125)
#    i = Image.open(form_picture)
#    i.thumbnail(output_size)
#    i.save(picture_path)
#
#    return picture_fn
#
#
#@app.route("/account", methods=['GET', 'POST'])
#@login_required
#def account():
#    form = UpdateAccountForm()
#    if form.validate_on_submit():
#        if form.picture.data:
#            picture_file = save_picture(form.picture.data)
#            current_user.image_file = picture_file
#        current_user.username = form.username.data
#        current_user.email = form.email.data
#        db.session.commit()
#        flash('Your account has been updated!', 'success')
#        return redirect(url_for('account'))
#    elif request.method == 'GET':
#        form.username.data = current_user.username
#        form.email.data = current_user.email
#    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
#    return render_template('account.html', title='Account',
#                            image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
#@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
        title=form.title.data, 
        path=form.path.data,
        parent_landing_page_path=form.parent_landing_page_path.data,
        landing_page_path=form.landing_page_path.data,
        repository_path=form.repository_path.data,
        github_repository_path=form.github_repository_path.data,
        short_description=form.short_description.data,
        long_description=form.long_description.data,
        long_description_html = form.long_description_html.data,
        technical_description = form.technical_description.data,
        databases_used = form.databases_used.data,
        technical_databases_used = form.technical_databases_used.data,
        created_by =  form.created_by.data,
        maintained_by=form.maintained_by.data, 
        maintained_by_backup=form.maintained_by_backup.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='Add New',
                            form=form, legend='Add New')


@app.route("/post/<post_title>")
def post(post_title):
    post = Post.query.get_or_404(post_title)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<post_title>/update", methods=['GET', 'POST'])
#@login_required
def update_post(post_title):
    post = Post.query.get_or_404(post_title)
    #if post.author != current_user:
    #    abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title=form.title.data
        post.path=form.path.data
        post.parent_landing_page_path=form.parent_landing_page_path.data
        post.landing_page_path=form.landing_page_path.data
        post.repository_path=form.repository_path.data
        post.github_repository_path=form.github_repository_path.data
        post.short_description=form.short_description.data
        post.long_description=form.long_description.data
        post.long_description_html = form.long_description_html.data
        post.technical_description = form.technical_description.data
        post.databases_used = form.databases_used.data
        post.technical_databases_used = form.technical_databases_used.data
        post.created_by = form.created_by.data
        post.maintained_by=form.maintained_by.data
        post.maintained_by_backup=form.maintained_by_backup.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_title=post.title))
    elif request.method == 'GET':
        form.title.data=post.title
        form.path.data=post.path
        form.parent_landing_page_path.data=post.parent_landing_page_path
        form.landing_page_path.data=post.landing_page_path
        form.repository_path.data=post.repository_path
        form.github_repository_path.data=post.github_repository_path
        form.short_description.data=post.short_description
        form.long_description.data=post.long_description
        form.long_description_html.data=post.long_description_html
        form.technical_description.data=post.technical_description
        form.databases_used.data =  post.databases_used
        form.technical_databases_used.data = post.technical_databases_used
        form.created_by.data=post.created_by
        form.maintained_by.data=post.maintained_by
        form.maintained_by_backup.data=post.maintained_by_backup
    return render_template('create_post.html', title='Update Post',
                            form=form, legend='Update Post')


@app.route("/post/<post_title>/delete", methods=['POST'])
#@login_required
def delete_post(post_title):
    post = Post.query.get_or_404(post_title)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

