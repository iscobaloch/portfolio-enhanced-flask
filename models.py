from flask_sqlalchemy import SQLAlchemy
from app import datetime

db = SQLAlchemy()
db2 = SQLAlchemy()

class Tbltourpackages(db.Model):
    __tablename__ = 'tbltourpackages'
    PackageId = db.Column(db.Integer, primary_key=True)
    PackageName = db.Column(db.String(150), nullable=False)
    PackageLocation = db.Column(db.String(120), nullable=False)
    PackagePrice = db.Column(db.String(15), nullable=True)
    PackageDetails = db.Column(db.String(1000), nullable=False)
    PackageImage = db.Column(db.String(120), nullable=False)
    Creationdate = db.Column(db.DATE, default=datetime.now())
    Duration = db.Column(db.Integer, nullable=True)
    Accommodation = db.Column(db.String(120), nullable=False)
    Meal = db.Column(db.String(120), nullable=False)
    Transport = db.Column(db.String(120), nullable=False)


class Log(db.Model):
    __bind_key__ = 'wali'
    __tablename__ = 'log'
    id = db2.Column(db2.Integer, primary_key=True)
    username = db2.Column(db2.String(150), nullable=False)
    password = db2.Column(db2.String(120), nullable=False)

class Tblbooking(db.Model):
    __tablename__ = 'tblbooking'
    BookingId = db.Column(db.Integer, primary_key=True)
    PackageId = db.Column(db.Integer, nullable=False)
    UserId = db.Column(db.Integer, nullable=False)
    FromDate = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    Comment = db.Column(db.String(5000), nullable=True)
    RegDate= db.Column(db.DATE, default=datetime.now())
    status=  db.Column(db.String(120), nullable=True)

class TblEnquiry(db.Model):
    __tablename__ = 'tblenquiry'
    id = db.Column(db.Integer, primary_key=True)
    FullName = db.Column(db.Integer, nullable=False)
    EmailId = db.Column(db.Integer, nullable=False)
    MobileNumber = db.Column(db.String(120), nullable=False)
    Subject = db.Column(db.String(5000), nullable=True)
    Description =  db.Column(db.String(120), nullable=True)
    PostingDate = db.Column(db.DATE, default=datetime.now())
    Status =  db.Column(db.String(120), nullable=True)




class About(db.Model):
    __tablename__ = 'about'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)

class Skills(db2.Model):
    __bind_key__ = 'wali'
    __tablename__ = 'Skills'
    id = db2.Column(db2.Integer, primary_key=True)
    uid = db2.Column(db2.Integer, nullable=False)
    skill = db2.Column(db2.String(100), nullable=False)
    percent = db2.Column(db2.Integer, nullable=False)

class Education(db2.Model):
    __bind_key__ = 'wali'
    __tablename__ = 'Education'
    id = db2.Column(db2.Integer, primary_key=True)
    uid = db2.Column(db2.Integer, nullable=False)
    degree = db2.Column(db2.String(100), nullable=False)
    years = db2.Column(db2.String(100), nullable=False)
    institute = db2.Column(db2.String(100), nullable=False)
    description = db2.Column(db2.String(100), nullable=False)

class Work(db2.Model):
    __bind_key__ = 'wali'
    __tablename__ = 'work'
    id = db2.Column(db2.Integer, primary_key=True)
    uid = db2.Column(db2.Integer, nullable=False)
    designation = db2.Column(db2.String(100), nullable=False)
    years = db2.Column(db2.String(100), nullable=False)
    org = db2.Column(db2.String(100), nullable=False)
    description = db2.Column(db2.String(500), nullable=False)
#
class Users(db2.Model):
    __bind_key__ = 'wali'
    __tablename__ = 'User'
    id = db2.Column(db2.Integer, primary_key=True)
    fname = db2.Column(db2.String(100), nullable=False)
    lname = db2.Column(db2.String(100), nullable=False)
    profession = db2.Column(db2.String(200), nullable=False)
    about = db2.Column(db2.String(1000), nullable=False)
    img = db2.Column(db2.String(500), nullable=False)

class Info(db2.Model):
    __bind_key__ = 'wali'
    __tablename__ = 'Info'
    id = db2.Column(db2.Integer, primary_key=True)
    uid = db2.Column(db2.String(100), nullable=False)
    DOB = db2.Column(db2.String(100), nullable=False)
    Phone = db2.Column(db2.String(100), nullable=False)
    email = db2.Column(db2.String(200), nullable=False)
    address = db2.Column(db2.String(100), nullable=False)
    nationality = db2.Column(db2.String(50), nullable=False)
    languages = db2.Column(db2.String(200), nullable=False)
    freelance = db2.Column(db2.String(100), nullable=False)

class Achievements(db2.Model):
    __bind_key__ = 'wali'
    __tablename__ = 'achievements'
    id = db2.Column(db2.Integer, primary_key=True)
    uid = db2.Column(db2.String(100), nullable=False)
    experience = db2.Column(db2.String(100), nullable=False)
    projects = db2.Column(db2.String(100), nullable=False)
    awards = db2.Column(db2.String(200), nullable=False)
    customer = db2.Column(db2.String(100), nullable=False)


class User(db.Model):
    __tablename__ = 'tblusers'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    regdate = db.Column(db.DATE, default=datetime.now())

class Chat(db.Model):
    __tablename__ = 'chat'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, nullable=False)
    sender = db.Column(db.Integer, nullable=False)
    message = db.Column(db.String(300), nullable=False)
    time = db.Column(db.DATE, default=datetime.now())
    status = db.Column(db.Integer, nullable=False)

#
class Admin(db.Model):
    __tablename__='admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String(200), nullable=False)

class Tblpages(db.Model):
    __tablename__='tblpages'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100), nullable=False)
    detail = db.Column(db.String(3000), nullable=False)