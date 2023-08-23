import typing
from PyQt5 import QtCore
import PyQt5.QtWidgets as w
import random as rd
from PyQt5.QtWidgets import QWidget
import numpy as np
import sys
import shutil
from PyQt5.uic import loadUi
from functools  import partial

# File Name
adminFile = 'Admin.txt'
teacherFile = 'Teacher.txt'
studentFile = 'Student.txt'

class Welcome(w.QDialog):
    def __init__(self):
        super(Welcome,self).__init__()

        loadUi('Welcome Screens\Welcome Screen.ui',self)
        self.start.clicked.connect(self.changeUI)

    def changeUI(self):
        ui = Login()
        self.close()
        ui.exec_()

class Login(w.QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi('Welcome Screens\Login Screen.ui',self)

        self.login.clicked.connect(self.checkDetails)
        self.signup.clicked.connect(lambda:(self.changeUI(SignUp())))
        types = ['Admin','Faculty','Student']
        for i in range(len(types)):
            self.type.addItem(types[i])
        self.type.currentIndexChanged.connect(self.changePlaceHolder)
    
    def changePlaceHolder(self):
        index = self.type.currentIndex()
        if index == 0:
            self.sid.setPlaceholderText('Admin ID')
        elif index == 1:
            self.sid.setPlaceholderText('Teacher ID')
        else:
            self.sid.setPlaceholderText('Student ID')

    def checkDetails(self):
        id = self.sid.toPlainText()
        pas = self.pas.toPlainText()
        types = self.type.currentText()
        msg = w.QMessageBox()
        msg.setWindowTitle('Information')
        msg.setStandardButtons(w.QMessageBox.Ok)
        if id == '' or pas == '':
            msg.setText('Please Enter All Fields')
            msg.exec_()
        else:
            if types == 'Admin':
                currentfile = adminFile
            elif types == 'Faculty':
                currentfile = teacherFile
            else:
                currentfile = studentFile
            
            flag = False
            with open(currentfile,'r') as file:
                for line in file:
                    arr = line.strip().split('|')
                    if arr[0] == id and arr[4] == pas:
                        User.sid = id
                        User.name = arr[1]
                        User.mail = arr[2]
                        User.contact = arr[3]
                        User.usertype = types
                        flag = True
                        break
            if flag == False:
                msg.setText('This User Does Not Exist')
                msg.exec_()
            else:
                if User.usertype == 'Admin':
                    self.changeUI(Admin())
                elif User.usertype == 'Faculty':
                    self.changeUI(Teacher())
                else:
                    self.changeUI(Student())

    def changeUI(self,obj):
        ui = obj
        self.close()
        ui.exec_()

class SignUp(w.QDialog):
    def __init__(self):
        super(SignUp,self).__init__()
        loadUi('Welcome Screens\Admission Screen.ui',self)

        self.signup.clicked.connect(self.addDetails)
        self.login.clicked.connect(lambda:(self.changeUI(Login())))
    
    def addDetails(self):
        sid = self.sid.toPlainText()
        name = self.name.toPlainText()
        mail = self.mail.toPlainText()
        contact = self.contact.toPlainText()
        pas = self.pas.toPlainText()
        conpass = self.conpass.toPlainText()
        msg = w.QMessageBox()
        msg.setWindowTitle('Information')
        msg.setStandardButtons(w.QMessageBox.Ok)
        if sid == '' or len(sid) != 5:
            msg.setText('Student ID should be of 5 Digits')
            msg.exec_()
        elif name == '' or mail == '' or contact == '' or pas == '' or conpass == '':
            msg.setText('Please Input All Fields')
            msg.exec_()
        elif pas != conpass:
            msg.setText('Password and Confirm Password Should be Same')
            msg.exec_()
        else:
            flag = False
            with open(studentFile,'r') as file:
                for line in file:
                    line = line.strip()
                    arr = line.split('|')
                    if arr[0] == sid:
                        flag = True
            if flag:
                msg.setText('This Student ID Already Exists')
                msg.exec_()
            else:
                file = open(studentFile,'a')
                file.write(f'{sid}|{name}|{mail}|{contact}|{pas}\n')
                file.close()
                User.sid = sid
                User.name = name
                User.mail = mail
                User.contact = contact
                User.usertype = 'Student'
                self.changeUI(Student())
                

    def changeUI(self,obj):
        ui = obj
        self.close()
        ui.exec_()

class User:
    sid = str()
    name = str()
    mail = str()
    contact = str()
    pas = str()
    conpass = str()
    usertype = str()

# Student Classes
class Student(w.QDialog):
    def __init__(self):
        super(Student,self).__init__()

        loadUi('Student\Student .ui',self)
        # Setting up Widget
        self.layout = w.QVBoxLayout()
        instance = StudentDashboard()
        self.layout.addWidget(instance)
        self.load.setLayout(self.layout)
        self.home.clicked.connect(lambda:(self.changeWidget(),StudentDashboard()))

    def changeWidget(self,obj):
        while self.layout.count():
           item = self.layout.takeAt(0)
           widget = item.widget()
           if widget:
               widget.setParent(None)
           else:
               self.clearLayout(item.layout())
        self.changeColor(obj)
        self.layout.addWidget(obj)

    def changeColor(self,obj):
        btn = self.sender()
        btn.setStyleSheet('background-color: rgba(255, 255, 255, 0);image: url(icons/blue/home.png);')
class StudentDashboard(w.QWidget):
    def __init__(self):
        super(StudentDashboard,self).__init__()
        loadUi('Student\Student Dashboard.ui',self)

        self.name.setText(User.name)
        self.mail.setText(User.mail)
        self.id.setText(User.sid)
        self.contact.setText(User.contact)

class CheckAttendance(w.QDialog):
    def __init__(self):
        super(CheckAttendance,self).__init__()
        loadUi('Student\Check Attendance.ui',self)

class CheckMarks(w.QDialog):
    def __init__(self):
        super(CheckMarks,self).__init__()
        loadUi('Student\Check Marks.ui',self)

class Classes(w.QDialog):
    def __init__(self):
        super(Classes,self).__init__()
        loadUi('Student\Classes.ui',self)

class Schedule(w.QDialog):
    def __init__(self):
        super(Schedule,self).__init__()
        loadUi('Student\Schedule.ui',self)

#Admin Classes
class Admin(w.QDialog):
    def __init__(self):
        super(Admin,self).__init__()
        loadUi('Admin\Admin.ui',self)

class AdminDashboard(w.QDialog):
    def __init__(self):
        super(AdminDashboard,self).__init__()
        loadUi('Admin\Admin Dashboard 1.ui',self)

class Hire(w.QDialog):
    def __init__(self):
        super(Hire,self).__init__()
        loadUi('Admin\Hire.ui',self)

class Fire(w.QDialog):
    def __init__(self):
        super(Fire,self).__init__()
        loadUi('Admin\Fire.ui',self)

class MakeClass(w.QDialog):
    def __init__(self):
        super(MakeClass,self).__init__()
        loadUi('Admin\Make a Class.ui',self)

class ShowTeachers(w.QDialog):
    def __init__(self):
        super(ShowTeachers,self).__init__()
        loadUi('Admin\Show All Teachers.ui',self)

class Update(w.QDialog):
    def __init__(self):
        super(Update,self).__init__()
        loadUi('Admin/Update.ui',self)

#Teacher Classes
class Teacher(w.QDialog):
    def __init__(self):
        super(Teacher,self).__init__()
        loadUi('Teacher\Teacher.ui',self)

class TeacherDashboard(w.QDialog):
    def __init__(self):
        super(TeacherDashboard,self).__init__()
        loadUi('Teacher\Teacher Dashboard.ui',self)

class MarksUpload(w.QDialog):
    def __init__(self):
        super(MarksUpload,self).__init__()
        loadUi('Teacher\Marks Upload.ui',self)

class StudentAttendance(w.QDialog):
    def __init__(self):
        super(StudentAttendance,self).__init__()
        loadUi('Teacher\Student Attendance.ui',self)

class Students(w.QDialog):
    def __init__(self):
        super(Students,self).__init__()
        loadUi('Teacher\Students.ui',self)

class TimeTable(w.QDialog):
    def __init__(self):
        super(TimeTable,self).__init__()
        loadUi('Teacher\Time Table.ui',self)

if __name__ == '__main__':
    app = w.QApplication(sys.argv)
    ui = Welcome()
    ui.show()
    app.exec_()
