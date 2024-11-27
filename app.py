from unicodedata import category

from flask import Flask, send_from_directory, flash, render_template, request, session, redirect, abort, url_for, current_app
from sqlalchemy.sql.functions import session_user
from werkzeug.utils import secure_filename
from sqlalchemy.sql.expression import func, select
import os
import json
from datetime import datetime
from datetime import timedelta
from passlib.hash import pbkdf2_sha256
from datetime import datetime
import secrets
import sqlite3
from models import *


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
db = SQLAlchemy()
app.config['WTF_CSRF_SECRET_KEY'] = "b'f\xfa\x8b{X\x8b\x9eM\x83l\x19\xad\x84\x08\xaa"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://wali:wali123@localhost:3306/tms"
app.config['SECRET_KEY'] = "b'f\xfa\x8b{X\x8b\x9eM\x83l\x19\xad\x84\x08\xaa"
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static/img//')
app.config['UPLOAD_FOLDER_DOC'] = os.path.join(basedir, 'static/docs/')

# Configuration for the second database
app.config["SQLALCHEMY_BINDS"] = {
    'wali': 'mysql+pymysql://wali:wali123@localhost:3306/wali'
}
db2 = SQLAlchemy(app)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize
db.init_app(app)

def save_images(photo):
    hash_photo= secrets.token_urlsafe(20)
    _, file_extension = os.path.splitext(photo.filename)
    photo_name= hash_photo + file_extension
    file_path= os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'], photo_name)
    photo.save(file_path)
    return photo_name


@app.route('/download_resume/<filename>')
def download_resume(filename):
    # Define the folder where resumes are stored (this should match the upload folder)
    resume_folder = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])

    # Construct the full file path
    file_path = os.path.join(resume_folder, filename)

    # Check if the file exists
    if not os.path.exists(file_path):
        abort(404)  # Return a 404 error if the file doesn't exist
    wali = Resume.query.filter_by(id=1).first()
    # Get the 'rname' value from the resume data
    rname = wali.rname  # The file's original name can be used or set as per your data

    # Ensure the filename has a .pdf extension
    if not rname.lower().endswith('.pdf'):
        rname = rname + '.pdf'

    # Send the file with the renamed filename
    return send_from_directory(resume_folder, filename, as_attachment=True, download_name=rname)


# Function to save PDF or any document (like .pdf, .doc, .docx)
def save_document(doc):
    # Generate a secure random file name using secrets
    hash_doc = secrets.token_urlsafe(20)

    # Get the file extension
    _, file_extension = os.path.splitext(doc.filename)

    # Ensure the file extension is one of the allowed types (PDF, DOC, DOCX, etc.)
    allowed_extensions = ['.pdf', '.doc', '.docx']
    if file_extension.lower() not in allowed_extensions:
        raise ValueError("Invalid file type. Only PDF, DOC, DOCX are allowed.")

    # Generate the document name (combining the random hash and the file extension)
    doc_name = hash_doc + file_extension

    # Set the file path where the document will be saved
    file_path = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'], doc_name)

    # Save the document to the file system
    doc.save(file_path)

    return doc_name


@app.route("/", methods=['GET'])
def home():
    info = Users.query.order_by(Users.id).first()
    return render_template("index.html", info=info)

# about page
@app.route("/about", methods=['GET'])
def about():
    info = Users.query.order_by(Users.id).first()
    data = db2.session.query(Info).filter(Info.uid == 1).first()
    achievement = db2.session.query(Achievements).filter(Achievements.uid == 1).first()
    skills = db2.session.query(Skills).filter(Skills.uid == 1).all()
    edu = db2.session.query(Education).filter(Education.uid == 1).all()
    exp = db2.session.query(Work).filter(Work.uid == 1).order_by(Work.id.desc()).all()
    res = Resume.query.filter_by(id=1).first()
    return render_template("about.html", res=res, exp=exp, edu=edu, skills=skills, info=info, data=data, achievement=achievement)



@app.route("/portfolio", methods=['GET'])
def portfolio():
    p = db2.session.query(Portfolio).filter(Portfolio.uid == 1).all()

    return render_template("portfolio.html",p=p)

@app.route("/test", methods=['GET'])
def test():

    return render_template("login.html")

@app.route("/blog", methods=['GET'])
def blog():

    return render_template("blog.html")
#
# # Guest - Home Page
# @app.route("/")
# def home():
#     packs = Tbltourpackages.query.order_by(Tbltourpackages.Creationdate.desc()).all()
#     random = Tbltourpackages.query.order_by(func.random()).all()
#     return render_template('index.html', packs=packs, random=random)
#
#
# #   Guest - All Packages
# @app.route("/trips-list")
# def trips():
#     packs = Tbltourpackages.query.order_by(Tbltourpackages.Creationdate.desc()).all()
#     random = Tbltourpackages.query.order_by(func.random()).all()
#     return render_template('package-list.html', packs=packs, random=random)
#
#  Guest - Contact Us
@app.route("/contact-us")
def contact():
    packs = Tbltourpackages.query.order_by(Tbltourpackages.Creationdate.desc()).all()
    random = Tbltourpackages.query.order_by(func.random()).all()
    return render_template('contact.html', packs=packs, random=random)
#
# # Guest - View Trip Details
# @app.route("/trip_id=<id>" , methods=['POST','GET'])
# def booking(id):
#     result = db.session.query(Tbltourpackages).filter(Tbltourpackages.PackageId==id).first()
#     usr= db.session.query(User).filter(User.id==session.get('uid')).first()
#     if result:
#         if request.method == 'POST':
#             if session.get('user'):
#                 city= request.form.get('city')
#                 date= request.form.get('date')
#                 msg= request.form.get('message')
#                 bk= Tblbooking(PackageId=id, UserId=session.get('uid'), city=city, FromDate=date, Comment=msg, status='3')
#                 db.session.add(bk)
#                 db.session.commit()
#                 flash('Your Trip is Submitted')
#                 return redirect(url_for('booking_history'))
#             else:
#                 return redirect(url_for('signin'))
#         else:
#             return render_template('booking-page.html',  result=result, usr=usr)
#     else:
#         return render_template('404.html')
#
#
# # User - USER SIGNUP
# @app.route("/signup", methods=['POST','GET'])
# def signup():
#     if session.get('user'):
#         return redirect(url_for('user'))
#     else:
#         if request.method == 'POST':
#             fullname = request.form.get('fullname')
#             email = request.form.get('email')
#             mobile = request.form.get('mobile')
#             passw = request.form.get('password')
#             password = pbkdf2_sha256.hash(passw)
#             cur= User.query.filter_by(email=email).first()
#             if cur is None:
#                 usr= User(fullname=fullname,email=email, mobile=mobile ,password=password)
#                 db.session.add(usr)
#                 db.session.commit()
#                 return redirect(url_for('signin'))
#             else:
#                 error = 'username already exist choose another!'
#                 return render_template("user/pages-register.html", error=error)
#         else:
#             return render_template("user/pages-register.html")
#
# Admin - ADMIN LOGIN
@app.route("/admin" , methods=['POST','GET'])
def login():
     if session.get('admin'):
         return redirect(url_for('admin'))
     elif session.get('user'):
         session.clear()
         return render_template("admin/pages-login.html")
     else:
         if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            adm = Log.query.filter_by(username=username).first()
            if adm and pbkdf2_sha256.verify(password, adm.password):
                session['admin'] = adm.username
                session['aid']= adm.id
                return redirect(url_for('admin'))
            else:
                error='Invalid Username or Password'
                return render_template("admin/pages-login.html", error=error)
         else:
             return render_template("admin/pages-login.html")


#  Admin - EDIT PROFILE INFORMATION
@app.route('/profile', methods=['POST', 'GET'])
def Prof():
    if session.get('admin'):
        if request.method == 'POST':
            img = request.files.get('img')  # Get the uploaded image
            fname = request.form.get('fname')
            lname = request.form.get('lname')
            profession = request.form.get('profession')
            address = request.form.get('address')
            editor = request.form.get('editor')

            me = Users.query.filter_by(id=session.get('aid')).first()
            updte = db.session.query(Users).filter_by(id=session.get('aid')).first()

            # Check if an image was uploaded
            if img and img.filename:  # If a new image was uploaded
                _, file_extension = os.path.splitext(img.filename)

                # Check if the uploaded image has a valid extension (jpg, jpeg, png)
                if file_extension.lower() in ['.jpg', '.jpeg', '.png']:
                    # Remove the old image if it exists (avoid breaking the app if file doesn't exist)
                    if updte.img:
                        old_img_path = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'], updte.img)
                        if os.path.exists(old_img_path):
                            os.remove(old_img_path)

                    # Save the new image and get the filename
                    new_img_filename = save_images(img)
                    updte.img = new_img_filename  # Update with the new image filename
                else:
                    flash("Invalid file type. Please upload a valid image (JPG, JPEG, PNG).")
                    return redirect(url_for('Prof'))
            else:
                # No image uploaded, so keep the old image
                new_img_filename = updte.img  # Keep the old image filename

            # Update the user data
            updte.fname = fname
            updte.lname = lname
            updte.profession = profession
            updte.address = address
            updte.info = editor
            updte.img = new_img_filename  # Store the image filename (whether new or old)

            db.session.commit()

            flash("CHANGES WERE MADE SUCCESSFULLY")
            return redirect(url_for('Prof'))

        else:
            t = db.session.query(Users).filter(Users.id == session.get('aid')).first()
            if t:
                return render_template("admin/user.html", t=t)
            else:
                return render_template('404.html')
    else:
        flash('LOGIN FIRST TO PROCEED')
        return redirect(url_for('login'))


#Add Skills
@app.route("/add-skill", methods=['POST','GET'])
def add_skill():
    if session.get('admin'):
        if request.method == 'POST':
            skill = request.form.get('skill')
            percent= request.form.get('percent')
            skill = Skills(skill=skill, percent=percent, uid=session.get('aid'))
            db2.session.add(skill)
            db2.session.commit()
            flash("SKILL ADDED SUCCESSFULLY")
            return redirect(url_for('manage_skills'))
        else:
            return render_template("admin/add-skill.html")
    else:
        flash('LOGIN FIRST TO PROCEED')
        return render_template("admin/pages-login.html")


#Add Education Certificate
@app.route("/add-education", methods=['POST','GET'])
def add_education():
    if session.get('admin'):
        if request.method == 'POST':
            degree = request.form.get('degree')
            years= request.form.get('years')
            institute = request.form.get('institute')
            description = request.form.get('description')
            education = Education(degree=degree, years=years, institute=institute, description=description, uid=session.get('aid'))
            db2.session.add(education)
            db2.session.commit()
            flash("EDUCATION ADDED SUCCESSFULLY")
            return redirect(url_for('manage_education'))
        else:
            return render_template("admin/add-education.html")
    else:
        flash('LOGIN FIRST TO PROCEED')
        return render_template("admin/pages-login.html")


#Add Work
@app.route("/add-experience", methods=['POST','GET'])
def add_experience():
    if session.get('admin'):
        if request.method == 'POST':
            designation = request.form.get('designation')
            years= request.form.get('years')
            org = request.form.get('org')
            description = request.form.get('description')
            experience = Work(designation=designation, years=years, org=org, description=description, uid=session.get('aid'))
            db2.session.add(experience)
            db2.session.commit()
            flash("EXPERIENCE ADDED SUCCESSFULLY")
            return redirect(url_for('manage_experience'))
        else:
            return render_template("admin/add-experience.html")
    else:
        flash('LOGIN FIRST TO PROCEED')
        return render_template("admin/pages-login.html")


#  Info Page admin
@app.route('/info', methods=['POST', 'GET'])
def info():
    if session.get('admin'):
        if request.method == 'POST':
            phone= request.form.get('phone')
            email = request.form.get('email')
            DOB = request.form.get('dob')
            languages = request.form.get('languages')
            address = request.form.get('address')
            nationality = request.form.get('nationality')
            freelance = request.form.get('freelance')
            me= Info.query.filter_by(uid=session.get('aid')).first()

            if me:
                updte = db.session.query(Info).filter_by(uid=session.get('aid')).first()
                updte.fname = phone
                updte.lname = email
                updte.DOB = DOB
                updte.address = address
                updte.nationality = nationality
                updte.languages = languages
                updte.freelance = freelance
                db.session.commit()
                flash("CHANGES WERE MADE SUCCESSFULLY")
                return redirect(url_for('info'))
            else:
                updte = db.session.query(Info).filter_by(uid=session.get('aid')).first()
                updte.fname = phone
                updte.lname = email
                updte.DOB = DOB
                updte.address = address
                updte.nationality = nationality
                updte.languages = languages
                updte.freelance = freelance
                db.session.commit()
                flash("CHANGES WERE MADE SUCCESSFULLY")
                return redirect(url_for('info'))
        else:
            t = db.session.query(Info).filter(Users.id==session.get('aid')).first()
            if t:
                return render_template("admin/info.html",t=t)
            else:
                return render_template('404.html')
    else:
        flash('LOGIN FIRST TO PROCEED')
        return redirect(url_for('login'))

# Admin manage skills
@app.route("/manage-skills")
def manage_skills():
    if session.get('admin'):
        skills = Skills.query.order_by(Skills.id.desc()).all()

        return render_template("admin/skills.html",skills=skills)
    else:
        flash('LOGIN FIRST TO PROCEED')
        return redirect(url_for('login'))


#Edit Skills
@app.route("/manage-skill/id=<id>/action=edit", methods=['POST', 'GET'])
def edit_skills(id):
    if session.get('admin'):
        if request.method == 'POST':
            skill = request.form.get('skill')
            percent = request.form.get('percent')
            hello= Skills.query.filter_by(id=id).first()
            updte = db.session.query(Skills).filter_by(id=id).first()
            updte.skill = skill
            updte.percent = percent
            db.session.commit()
            flash("CHANGES WERE MADE SUCCESSFULLY")
            return redirect(url_for('manage_skills'))
        else:
            t = db.session.query(Skills).filter(Skills.id==id).first()
            if t:
                return render_template("admin/edit-skills.html", id=id,t=t)
            else:
                return render_template('404.html')
    else:
        flash('LOGIN FIRST TO PROCEED')
        return redirect(url_for('login'))


#Delete Skill
@app.route("/edit-skill/action_delete=<int:id>", methods=['POST','GET'])
def delete_skill(id):
    if session.get('admin'):
        post = db.session.query(Skills).filter_by(id=id).first()
        if post is None:
            flash("This Item is Already Deleted")
            return redirect(url_for('manage_skills'))
        else:
            record= db.session.query(Skills).filter_by(id=id).first()
            db.session.delete(record)
            db.session.commit()
            flash('Skill Has been Deleted Successfully')
            return redirect(url_for('manage_skills'))
    else:
        flash('LOGIN FIRST TO PROCEED')
        return render_template("admin/pages-login.html")


# Admin manage education
@app.route("/manage-education")
def manage_education():
    if session.get('admin'):
        edu = Education.query.order_by(Education.id.desc()).all()

        return render_template("admin/education.html",edu=edu   )
    else:
        flash('LOGIN FIRST TO PROCEED')
        return redirect(url_for('login'))

#Edit Education
@app.route("/manage-education/id=<id>/action=edit", methods=['POST', 'GET'])
def edit_education(id):
    if session.get('admin'):
        if request.method == 'POST':
            degree = request.form.get('degree')
            years = request.form.get('years')
            institute = request.form.get('institute')
            description = request.form.get('description')
            hello= Education.query.filter_by(id=id).first()
            updte = db.session.query(Education).filter_by(id=id).first()
            updte.skill = degree
            updte.percent = years
            updte.institute = institute
            updte.description = description
            db.session.commit()
            flash("CHANGES WERE MADE SUCCESSFULLY")
            return redirect(url_for('manage_education'))
        else:
            t = db.session.query(Education).filter(Education.id==id).first()
            if t:
                return render_template("admin/edit-education.html", id=id,t=t)
            else:
                return render_template('404.html')
    else:
        flash('LOGIN FIRST TO PROCEED')
        return redirect(url_for('login'))



# Manage Experience ADMIN
@app.route("/manage-experience")
def manage_experience():
    if session.get('admin'):
        exp = Work.query.order_by(Work.id.desc()).all()

        return render_template("admin/experience.html", exp=exp   )
    else:
        flash('LOGIN FIRST TO PROCEED')
        return redirect(url_for('login'))

#Edit Work Experience
@app.route("/manage-experience/id=<id>/action=edit", methods=['POST', 'GET'])
def edit_experience(id):
    if session.get('admin'):
        if request.method == 'POST':
            designation = request.form.get('designation')
            years = request.form.get('years')
            org = request.form.get('org')
            description = request.form.get('description')
            hello= Work.query.filter_by(id=id).first()
            updte = db.session.query(Work).filter_by(id=id).first()
            updte.designation = designation
            updte.years = years
            updte.org = org
            updte.description = description
            db.session.commit()
            flash("CHANGES WERE MADE SUCCESSFULLY")
            return redirect(url_for('manage_experience'))
        else:
            t = db.session.query(Work).filter(Work.id==id).first()
            if t:
                return render_template("admin/edit-experience.html", id=id,t=t)
            else:
                return render_template('404.html')
    else:
        flash('LOGIN FIRST TO PROCEED')
        return redirect(url_for('login'))

#Delete Education record
@app.route("/edit-education/action_delete=<int:id>", methods=['POST','GET'])
def delete_education(id):
    if session.get('admin'):
        post = db.session.query(Education).filter_by(id=id).first()
        if post is None:
            flash("This Item is Already Deleted")
            return redirect(url_for('manage_education'))
        else:
            record= db.session.query(Education).filter_by(id=id).first()
            db.session.delete(record)
            db.session.commit()
            flash('Education Record Has been Deleted Successfully')
            return redirect(url_for('manage_education'))
    else:
        flash('LOGIN FIRST TO PROCEED')
        return render_template("admin/pages-login.html")

# Manage Portfolio
@app.route("/manage-portfolio")
def manage_portfolio():
    if session.get('admin'):
        edu = Portfolio.query.order_by(Portfolio.id.desc()).all()
        rec = db2.session.query(Portfolio).filter_by(uid=session.get('aid')).all()

        # Iterate over each portfolio record to ensure 'website' field is fully qualified
        for portfolio in rec:
            if portfolio.website and not portfolio.website.startswith(('http://', 'https://')):
                portfolio.website = "https://" + portfolio.website

        return render_template("admin/portfolio.html", edu=edu, rec=rec)
    else:
        flash('LOGIN FIRST TO PROCEED')
        return redirect(url_for('login'))


# Add Portfolio
@app.route("/add-portfolio", methods=['POST','GET'])
def add_portfolio():
    if session.get('admin'):
        if request.method == 'POST':
            cat = request.form.get('projcat')
            ptype= request.form.get('ptype')
            client = request.form.get('client')
            plang = request.form.get('plang')
            url = request.form.get('url')
            thumb = save_images(request.files.get('thumb'))
            portfolio= Portfolio(category=cat, project=ptype, client=client, progr=plang,
            website=url, thumb=thumb, uid=session.get('aid'))
            db2.session.add(portfolio)
            db2.session.commit()
            flash("PROJECT ADDED SUCCESSFULLY")
            return redirect(url_for('manage_portfolio'))
        else:
            t = db.session.query(Users).filter(Users.id == session.get('aid')).first()
            return render_template("admin/add-portfolio.html", t=t)
    else:
        flash('LOGIN FIRST TO PROCEED')
        return render_template("admin/pages-login.html")

#Delete Portfolio record
@app.route("/edit-portfolio/action_delete=<int:id>", methods=['POST','GET'])
def delete_portfolio(id):
    if session.get('admin'):
        post = db.session.query(Portfolio).filter_by(id=id).first()
        if post is None:
            flash("This Item is Already Deleted")
            return redirect(url_for('manage_portfolio'))
        else:
            record= db.session.query(Portfolio).filter_by(id=id).first()
            db.session.delete(record)
            db.session.commit()
            flash('Project Has been Deleted Successfully')
            return redirect(url_for('manage_portfolio'))
    else:
        flash('LOGIN FIRST TO PROCEED')
        return render_template("admin/pages-login.html")

# EDIT PORTFOLIO INFORMATION
@app.route("/manage-portfolio/action_edit=<id>", methods=['POST', 'GET'])
def edit_portfolio(id):
    if session.get('admin'):
        if request.method == 'POST':
            img= request.files.get('thumb')
            cat = request.form.get('projcat')
            project = request.form.get('ptype')
            client = request.form.get('client')
            url = request.form.get('url')
            progr = request.form.get('plang')
            hello= Portfolio.query.filter_by(id=id).first()
            _, file_extension = os.path.splitext(img.filename)
            if ('.jpg' or '.jpeg' or '.png') in file_extension:
                updte = db.session.query(Portfolio).filter_by(id=id).first()
                os.remove(app.config['UPLOAD_FOLDER']+updte.PackageImage)
                updte.project = project
                updte.category = cat
                updte.client = client
                updte.progr = progr
                updte.thumb = save_images(request.files.get('timage'))
                updte.website = url
                db.session.commit()
                flash("CHANGES WERE MADE SUCCESSFULLY")
                return redirect(url_for('manage_portfolio'))
            else:
                updte = db.session.query(Portfolio).filter_by(id=id).first()
                updte.project = project
                updte.category = cat
                updte.client = client
                updte.thumb = hello.thumb
                updte.website = url
                updte.progr = progr
                db.session.commit()
                flash("POST AS BEEN UPDATED")
                return redirect(url_for('manage_portfolio'))
        else:
            t = db.session.query(Portfolio).filter(Portfolio.id==id).first()
            if t:
                return render_template("admin/edit-portfolio.html", id=id,t=t)
            else:
                return render_template('404.html')
    else:
        flash('LOGIN FIRST TO PROCEED')
        return redirect(url_for('login'))


# Function to save PDF or any document (like .pdf, .doc, .docx)
def save_document(doc):
    # Generate a secure random file name using secrets
    hash_doc = secrets.token_urlsafe(20)

    # Get the file extension
    _, file_extension = os.path.splitext(doc.filename)

    # Ensure the file extension is one of the allowed types (PDF, DOC, DOCX, etc.)
    allowed_extensions = ['.pdf', '.doc', '.docx']
    if file_extension.lower() not in allowed_extensions:
        raise ValueError("Invalid file type. Only PDF, DOC, DOCX are allowed.")

    # Generate the document name (combining the random hash and the file extension)
    doc_name = hash_doc + file_extension

    # Set the file path where the document will be saved
    file_path = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'], doc_name)

    # Save the document to the file system
    doc.save(file_path)

    return doc_name

#Manage Resume
@app.route("/manage-resume")
def manage_resume():
    if session.get('admin'):
        res = Resume.query.order_by(Resume.id).first()

        return render_template("admin/manage-resume.html",res=res   )
    else:
        flash('LOGIN FIRST TO PROCEED')
        return redirect(url_for('login'))



#Edit Resume
@app.route('/edit-resume', methods=['POST', 'GET'])
def edit_resume():
    if session.get('admin'):
        if request.method == 'POST':
            doc = request.files.get('resume')  # Get the uploaded document
            rname = request.form.get('rname')


            me = Resume.query.filter_by(uid=session.get('aid')).first()
            updte = db.session.query(Resume).filter_by(id=session.get('aid')).first()

            # Check if a resume (document) was uploaded
            if doc and doc.filename:  # If a new document was uploaded
                try:
                    # Save the document and get the filename
                    new_doc_filename = save_document(doc)
                    # Optionally, remove old document if it exists
                    if updte.resume:
                        old_doc_path = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER_DOC'], updte.resume)
                        if os.path.exists(old_doc_path):
                            os.remove(old_doc_path)
                    updte.resume = new_doc_filename  # Store the document filename
                except ValueError as e:
                    flash(str(e))
                    return redirect(url_for('Prof'))

            else:
                # No document uploaded, so keep the old one
                new_doc_filename = updte.resume  # Keep the old document filename

            # Update the user data
            updte.rname = rname
            updte.update_time = datetime.now()
            updte.uid = session.get('aid')
            updte.resume = new_doc_filename  # Store the document filename (whether new or old)

            db.session.commit()

            flash("CHANGES WERE MADE SUCCESSFULLY")
            return redirect(url_for('Prof'))

        else:
            res = db.session.query(Resume).filter(Resume.uid == session.get('aid')).first()
            if res:
                return render_template("admin/update-resume.html", res=res)
            else:
                return render_template('404.html')
    else:
        flash('LOGIN FIRST TO PROCEED')
        return redirect(url_for('login'))


# Admin - ADMIN ADD NEW TOUR
@app.route("/add-tour", methods=['POST','GET'])
def add_tour():
    if session.get('admin'):
        if request.method == 'POST':
            title = request.form.get('title')
            location = request.form.get('location')
            transport = request.form.get('transport')
            meal = request.form.get('meal')
            accommodation = request.form.get('accommodation')
            duration = request.form.get('duration')
            pdetails = request.form.get('editor')
            price = request.form.get('price')
            f = save_images(request.files.get('timage'))
            tour = Tbltourpackages(PackageName=title, PackageDetails=pdetails, PackageLocation=location, Transport=transport, Meal=meal,Duration=duration,
                                   Accommodation=accommodation,PackagePrice=price, PackageImage =f)
            db.session.add(tour)
            db.session.commit()
            flash("TOUR ADDED SUCCESSFULLY")
            return redirect(url_for('manage_tours'))
        else:
            return render_template("admin/add-tour.html")
    else:
        flash('LOGIN FIRST TO PROCEED')
        return render_template("admin/pages-login.html")

# # User - User Login Page
# @app.route("/login" , methods=['POST','GET'])
# def signin():
#      if session.get('user'):
#          return redirect(url_for('user'))
#      elif session.get('admin'):
#          session.clear()
#          return render_template("user/pages-login.html")
#      else:
#          if request.method == "POST":
#             email = request.form.get("email")
#             password = request.form.get("password")
#             usr = User.query.filter_by(email=email).first()
#             if usr and pbkdf2_sha256.verify(password, usr.password):
#                 session['user'] = usr.email
#                 session['uid']= usr.id
#
#                 session['username']= usr.fullname
#                 return redirect(url_for('user'))
#             else:
#                 error='Invalid Email or Password'
#                 return render_template("user/pages-login.html", error=error)
#          else:
#              return render_template("user/pages-login.html")
#
# # User - USER DASHBOARD
# @app.route("/user_dashboard")
# def user():
#     if session.get('user'):
#         return render_template("user/user.html")
#     else:
#         flash('LOGIN FIRST TO ACCESS DASHBOARD')
#         return redirect(url_for('signin'))
#
#
#  Admin - ADMIN DASHBOARD
@app.route("/dashboard")
def admin():
    if session.get('admin'):
        member= User.query.all()
        bkk = Tblbooking.query.all()
        cats = Tbltourpackages.query.all()
        mgs = Chat.query.all()
        booking = db.session.query(User, Tblbooking, Tbltourpackages).filter(Tblbooking.UserId == User.id).filter(
            Tblbooking.PackageId == Tbltourpackages.PackageId) \
            .order_by(Tblbooking.RegDate.desc()).all()
        msg= db.session.query(Chat,User).filter(Chat.uid==User.id).filter(Chat.sender>1).order_by(Chat.time.desc()).all()
        return render_template("admin/admin.html",cats=cats,bkk=bkk, mgs=mgs, member=member, booking=booking, msg=msg)
    else:
        flash('LOGIN FIRST TO ACCESS DASHBOARD')
        return redirect(url_for('login'))



#  Admin - EDIT TOUR INFORMATION
@app.route("/manage-tour/id=<id>/action=edit", methods=['POST', 'GET'])
def edit_tour(id):
    if session.get('admin'):
        if request.method == 'POST':
            img= request.files.get('timage')
            title = request.form.get('title')
            location = request.form.get('location')
            transport = request.form.get('transport')
            meal = request.form.get('meal')
            accommodation = request.form.get('accommodation')
            duration = request.form.get('duration')
            tdetails = request.form.get('editor')
            price = request.form.get('price')
            hello= Tbltourpackages.query.filter_by(PackageId=id).first()
            _, file_extension = os.path.splitext(img.filename)
            if ('.jpg' or '.jpeg' or '.png') in file_extension:
                updte = db.session.query(Tbltourpackages).filter_by(PackageId=id).first()
                os.remove(app.config['UPLOAD_FOLDER']+updte.PackageImage)
                updte.PackageName = title
                updte.PackageLocation = location
                updte.PackageImage = save_images(request.files.get('timage'))
                updte.Transport = transport
                updte.Meal = meal
                updte.Accommodation = accommodation
                updte.Duration = duration
                updte.PackagePrice = price
                updte.PackageDetails = tdetails
                db.session.commit()
                flash("CHANGES WERE MADE SUCCESSFULLY")
                return redirect(url_for('manage_tours'))
            else:
                updte = db.session.query(Tbltourpackages).filter_by(PackageId=id).first()
                updte.PackageName = title
                updte.PackageLocation = location
                updte.PackageImage = hello.PackageImage
                updte.Transport = transport
                updte.Meal = meal
                updte.Accommodation = accommodation
                updte.Duration = duration
                updte.PackagePrice = price
                updte.PackageDetails = tdetails
                db.session.commit()
                flash("POST AS BEEN UPDATED")
                return redirect(url_for('manage_tours'))
        else:
            t = db.session.query(Tbltourpackages).filter(Tbltourpackages.PackageId==id).first()
            if t:
                return render_template("admin/edit-tour.html", id=id,t=t)
            else:
                return render_template('404.html')
    else:
        flash('LOGIN FIRST TO PROCEED')
        return redirect(url_for('login'))


#  Admin - DELETE A TOUR PACKAGE
@app.route("/edit-tour/action_delete=<int:id>", methods=['POST','GET'])
def delete_pack(id):
    if session.get('admin'):
        post = db.session.query(Tbltourpackages).filter_by(PackageId=id).first()
        if post is None:
            flash("This Item is Already Deleted")
            return redirect(url_for('manage_tours'))
        else:
            record= db.session.query(Tbltourpackages).filter_by(PackageId=id).first()
            os.remove(app.config['UPLOAD_FOLDER']+record.PackageImage)
            db.session.delete(record)
            db.session.commit()
            flash('Package Has been Deleted')
            return redirect(url_for('manage_tours'))
    else:
        flash('LOGIN FIRST TO PROCEED')
        return render_template("admin/pages-login.html")


#  Admin - MANAGE BOOKINGS
@app.route("/manage-bookings",  methods=['POST','GET'])
def manage_bookings():
    if session.get('admin'):
        if request.method == 'POST':
            st = request.form.get('myselect')
            bkid= request.form.get('bkid')
            bk = db.session.query(Tblbooking).filter_by(BookingId=bkid).first()
            bk.status = st
            db.session.commit()
            return redirect(request.url)
        else:
            booking = db.session.query(User, Tblbooking, Tbltourpackages).filter(Tblbooking.UserId==User.id).filter(Tblbooking.PackageId==Tbltourpackages.PackageId)\
            .order_by(Tblbooking.RegDate.desc()).all()
            return render_template("admin/bookings.html",booking=booking)
    else:
        flash('LOGIN FIRST TO PROCEED')
        return redirect(url_for('login'))


#   Admin - MANAGE TOURS
@app.route("/manage-tours")
def manage_tours():
    if session.get('admin'):
        tours = db.session.query(Tbltourpackages).order_by(Tbltourpackages.Creationdate.desc()).all()

        return render_template("admin/manage-packages.html",tours=tours)
    else:
        flash('LOGIN FIRST TO PROCEED')
        return render_template("admin/pages-login.html")

#  Admin -  GUEST USER CONTACT HELP
@app.route("/manage-help",  methods=['POST','GET'])
def guest_help():
    if session.get('admin'):
        if request.method == 'POST':
            id= request.form.get('eqid')
            st= request.form.get('st')
            stats = db.session.query(TblEnquiry).filter_by(id=id).first()
            stats.Status = st
            db.session.commit()
            return redirect(request.url)
        else:
            msg = TblEnquiry.query.order_by(TblEnquiry.PostingDate.desc()).all()
            return render_template("admin/guest-help.html",msg=msg)
    else:
        flash('LOGIN FIRST TO PROCEED')
        return redirect(url_for('login'))

#   Admin -  MANAGE USERS
@app.route("/manage-users")
def manage_users():
    if session.get('admin'):
        users = User.query.order_by(User.regdate.desc()).all()

        return render_template("admin/manage-users.html",users=users)
    else:
        flash('LOGIN FIRST TO PROCEED')
        return redirect(url_for('login'))
#
# #  User -  USER BOOKING HISTORY
# @app.route("/booking-history")
# def booking_history():
#     if session.get('user'):
#         b = db.session.query(Tblbooking,Tbltourpackages).filter(Tblbooking.UserId==session.get('uid')).filter(Tblbooking.PackageId==Tbltourpackages.PackageId)\
#             .order_by(Tblbooking.RegDate.desc()).all()
#
#         return render_template("user/booking-history.html",b=b)
#     else:
#         flash('LOGIN FIRST TO PROCEED')
#         return redirect(url_for('user'))
#
# # User -  User Chat Screen
# @app.route("/chat" , methods=['POST','GET'])
# def uchat():
#     if session.get('user'):
#         if request.method == 'POST':
#             msg = request.form.get('msg')
#             cht = Chat(uid=session.get('uid'), message=msg, sender=session.get('uid'), status='2')
#             db.session.add(cht)
#             db.session.commit()
#             return redirect(request.url)
#         else:
#             result = db.session.query(Chat,User).filter(Chat.uid==session.get('uid')).filter(User.id==session.get('uid')).order_by(Chat.time).all()
#             user= About.query.filter(About.id==1).first()
#             return render_template("user/apps-chat.html",user=user, result=result)
#
#     else:
#         flash('LOGIN FIRST TO PROCEED')
#         return redirect(url_for('signin'))
#
# # Admin -  ADMIN CHAT SCREEN
# @app.route("/chat=<uid>" , methods=['POST','GET'])
# def chat(uid):
#     if session.get('admin'):
#         if request.method == 'POST':
#             msg = request.form.get('msg')
#             cht = Chat(uid=uid, message=msg, sender=session.get('aid'), status='1')
#             db.session.add(cht)
#             db.session.commit()
#             return redirect(request.url)
#         else:
#             result = Chat.query.filter(Chat.uid==uid).order_by(Chat.time).all()
#             user= User.query.filter(User.id==uid).first()
#             if user:
#                 return render_template("admin/apps-chat.html",user=user, result=result, uid=uid)
#             else:
#                 return render_template('404.html')
#
#     else:
#         flash('LOGIN FIRST TO PROCEED')
#         return redirect(url_for('login'))
#
# Admin -  ADMIN CONTACT HELP NOTIFICATIONS
@app.route("/help", methods=['POST','GET'])
def help():
    if session.get('admin'):
        if request.method == 'POST':
            status = request.form.get('read')
            uid = request.form.get('usr')
            cht = request.form.get('cht')
            ch= db.session.query(Chat).filter_by(id=cht).first()
            ch.status=status
            db.session.commit()
            return redirect("../chat="+uid)
        else:
            u = User.query.all()
            r = db.session.query(Chat, User).filter(User.id==Chat.uid).order_by(Chat.time.desc()).all()
            return render_template("admin/chat.html", u=u, r=r)
    else:
        flash('LOGIN FIRST TO PROCEED')
        return redirect(url_for('login'))


#  Admin -  EDIT PAGE TYPES
@app.route("/page_type=<type>", methods=['POST','GET'])
def pges(type):
    if session.get('admin'):
        if request.method == 'POST':
            detail = request.form.get('editor')
            typ= db.session.query(Tblpages).filter_by(type=type).first()
            typ.detail=detail
            db.session.commit()
            return redirect('page_type='+type)
        else:
            t = db.session.query(Tblpages).filter_by(type=type).first()
            if t:
                return render_template("admin/pages.html", t=t)
            else:
                return render_template('404.html')
    else:
        flash('LOGIN FIRST TO PROCEED')
        return redirect(url_for('login'))


#  EDIT CONTACT INFO
@app.route("/edit-contact", methods=['POST','GET'])
def edit_contact():
    if session.get('admin'):
        if request.method == 'POST':
            aid = request.form.get('aid')
            phone = request.form.get('phone')
            email = request.form.get('email')
            abt= db.session.query(About).filter_by(id=aid).first()
            abt.email=email
            abt.phone=phone
            db.session.commit()
            return redirect(request.url)
        else:
            a= db.session.query(About).filter_by(id=1).first()
            return render_template("admin/edit-contact.html", a=a)
    else:
        flash('LOGIN FIRST TO PROCEED')
        return redirect(url_for('login'))


# #  Guest contact(enquiry) Page
# @app.route("/contact-us", methods=['POST','GET'])
# def contact_us():
#     if request.method == 'POST':
#         fullname = request.form.get('fname')
#         phone = request.form.get('phone')
#         email = request.form.get('email')
#         subject = request.form.get('subject')
#         description = request.form.get('msg')
#         enq= TblEnquiry(FullName=fullname, EmailId=email, MobileNumber=phone, Subject=subject, Description=description, Status='2')
#         db.session.add(enq)
#         db.session.commit()
#         flash('MESSAGE HAS BEEN SENT')
#         return redirect(request.url)
#     else:
#         ct= db.session.query(Tbltourpackages).filter_by(id=1).first()
#         print(ct.email)
#         return render_template("contact.html", ct=ct)
#
#
# #  GUEST USER PAGE TYPE
# @app.route("/page_<type>")
# def info(type):
#             t = db.session.query(Tblpages).filter_by(type=type).first()
#             if t:
#                 return render_template("page.html", t=t)
#             else:
#                 return render_template('404.html')
#
#
# #   UPDATE PROFILE SECTION
# @app.route("/update-profile", methods=['POST','GET'])
# def update_profile():
#     if session.get('user'):
#         if request.method=='POST':
#             email= request.form.get('email')
#             fname= request.form.get('fname')
#             mobile= request.form.get('mobile')
#             upt = db.session.query(User).filter_by(id=session.get('uid')).first()
#             upt.email= email
#             upt.fullname= fname
#             upt.mobile = mobile
#             db.session.commit()
#             session['username'] = fname
#             flash('PROFILE UPDATED SUCCESSFULLY')
#             user = User.query.filter_by(id=session.get('uid')).first()
#             return render_template('user/update-profile.html', user=user)
#         else:
#             user = User.query.filter_by(id=session.get('uid')).first()
#             return render_template('user/update-profile.html', user=user)
#     else:
#         return redirect(url_for('signin'))
#
#
#
#   PASSWORD CHANGE SECTION
@app.route("/change-password", methods=['POST','GET'])
def change_password():
    if session.get('admin'):
        if request.method=='POST':
            oldpass=request.form.get('oldpass')
            password = pbkdf2_sha256.hash(request.form.get('password'))
            adm = Admin.query.filter_by(id=session.get('aid')).first()
            if pbkdf2_sha256.verify(oldpass, adm.password):
                upt = db.session.query(Admin).filter_by(id=session.get('aid')).first()
                upt.password = password
                db.session.commit()
                flash('PASSWORD UPDATED SUCCESSFULLY')
                return render_template("admin/change-password.html")
            else:
                error='YOUR OLD PASSWORD WAS INCORRECT'
                return render_template("admin/change-password.html", error=error)
        else:
            return render_template("admin/change-password.html")
    elif session.get('user'):
        if request.method=='POST':
            oldpass=request.form.get('oldpass')
            password = pbkdf2_sha256.hash(request.form.get('password'))
            usr = User.query.filter_by(id=session.get('uid')).first()
            if pbkdf2_sha256.verify(oldpass, usr.password):
                upt = db.session.query(User).filter_by(id=session.get('uid')).first()
                upt.password = password
                db.session.commit()
                flash('PASSWORD UPDATED SUCCESSFULLY')
                return render_template("user/change-password.html")
            else:
                error='YOUR OLD PASSWORD WAS INCORRECT'
                return render_template("user/change-password.html", error=error)
        else:
            return render_template("user/change-password.html")
    else:
        flash('LOGIN FIRST TO ACCESS DASHBOARD')
        return redirect(url_for('login'))

# Logout
@app.route("/logout")
def logout():
    if session.get('admin'):
        session.clear()
        return redirect(url_for('home'))
    elif session.get('user'):
        session.clear()
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))

# create  custom Error pages
#Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

# Internal server error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"),500

# Custom filter for calculating "X time ago" using local machine time
@app.template_filter('time_ago')
def time_ago_filter(dt):
    # Get the current local machine time
    now = datetime.now()

    # Calculate the difference between current time and the given timestamp
    delta = now - dt

    # Return the formatted string depending on the time difference
    if delta < timedelta(minutes=1):
        return "Just now"
    elif delta < timedelta(hours=1):
        return f"{delta.seconds // 60} minutes ago"
    elif delta < timedelta(days=1):
        return f"{delta.seconds // 3600} hours ago"
    elif delta < timedelta(days=30):
        return f"{delta.days} days ago"
    else:
        return f"{delta.days // 30} months ago"  # Shows in months for larger dates


if __name__ == "__main__":

    app.run(debug=True)