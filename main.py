import datetime
import json

import leancloud
import requests
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView, QMessageBox

from UI import Ui_HomeLabTool
import pymysql

# db = pymysql.connect("localhost", "testuser", "test123", "TESTDB", charset='utf8' )
# cursor = db.cursor()
# sql =
# cursor.execute(sql)
# db.close()
searchbody = {"sessionToken": "xxw5yzxpdvzhe8jgxp0eu7wa7"}
headers = {'content-type': "application/json", 'X-LC-Id': 'P14YXPmT8ep8ThQnWhMz0dz8-9Nh9j0Va',
           'X-LC-Key': "NL5yAEdLcHr3P2f7xSdAhqV9"}
conn = pymysql.connect("rm-bp1911970b1xw7y2uao.mysql.rds.aliyuncs.com", "ltpyeah", "LTP24681793xz", "labhome",
                       charset='utf8')
leancloud.init('P14YXPmT8ep8ThQnWhMz0dz8-9Nh9j0Va', 'NL5yAEdLcHr3P2f7xSdAhqV9')
# 阿里云数据库地址
exp = [20, 40, 61, 82, 105, 128, 154, 181, 211, 243, 278, 316, 358, 403, 452, 506, 564, 628, 696, 771, 851, 937, 1029,
       1129, 1235, 1349, 1470, 1600, 1737, 1883, 2038, 2202, 2376, 2559, 2753, 2957, 3171, 3396, 3633, 3881, 4141, 4413,
       4698, 4995, 5306, 5629, 5967, 6318, 6684, 7064, 7459, 7869, 8295, 8736, 9193, 9667, 10157, 10665, 11189, 11732,
       12292, 12870, 13466, 14082, 14716, 15370, 16043, 16737, 17450, 18184, 18939, 19715, 20513, 21332, 22174, 23038,
       23924, 24833, 25766, 26722, 27702, 28706, 29735, 30788, 31867, 32970, 34100, 35255, 36437, 37645, 38880, 40142,
       41432, 42749, 44094, 45468, 46870, 48302, 49762, 51253, 52773]
inclassgold = [8, 9, 11, 12, 14, 15, 17, 18, 20, 21]
inclassexp = [8, 9, 11, 12, 14, 15, 17, 18, 20, 21]
bountygold = [50, 60, 70, 80, 90, 100, 110, 120, 130, 140]
# afterclassgold = [30, 36, 42, 48, 54, 60, 66, 72, 78, 84]
afterclassexp = [30, 36, 42, 48, 54, 60, 66, 72, 78, 84]
challengeexp = [160, 192, 224, 256, 288, 320, 352, 384, 416, 448]
checkpointscore = [8, 9, 11, 12, 14, 15, 17, 18, 20, 21]
StudentObjectID = []
user = ['姓名', '用户名', '年龄', '课程阶段', '玩学创币', '经验', '等级', '称号']
teacher = ['邹贵华', '刘天鹏', '薯条老师', '徐津', '朱敏', '啾啾', '波波', '刘攀', '糖果老师']
stage = ['科学一阶', '科学二阶', '科学三阶', '编程一阶', '编程二阶', '创客一阶',
         '创客二阶', '创客三阶', 'Python', 'C++']
taskInfo = ['挑战任务发布状态', '挑战任务完成情况', '赏金任务发布状态', '赏金任务入场人数', '赏金任务完成情况', '本月发放玩学创币总数']
taskStatus = ['', '', '', '', '', '']
global content
global player
global data
global lock


class RewardWindow(QMainWindow):
    def __init__(self):
        super(RewardWindow, self).__init__()
        self.setWindowTitle('抽奖')
        self.browser = QWebEngineView()
        self.browser.load(QUrl(QFileInfo("任务转盘.html").absoluteFilePath()))
        self.setCentralWidget(self.browser)


class ChildWindow(QMainWindow):
    def __init__(self):
        super(ChildWindow, self).__init__()
        self.setWindowTitle('抽奖')
        self.browser = QWebEngineView()
        self.browser.load(QUrl(QFileInfo("任务转盘.html").absoluteFilePath()))
        self.setCentralWidget(self.browser)


class mywindow(QtWidgets.QWidget, Ui_HomeLabTool):
    _signal = pyqtSignal(str)

    def __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)
        self.tableWidget_UserInfo.setShowGrid(False)
        self.tableWidget_TaskInfo.setShowGrid(False)
        self.tableWidget_UserInfo.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tableWidget_UserInfo.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.tableWidget_TaskInfo.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tableWidget_TaskInfo.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.pushButton_search.clicked.connect(self.search)
        self.pushButton_confirm.clicked.connect(self.UserLogin)
        self.pushButton_publishStoryTask.clicked.connect(self.PublishStoryTask)
        self.pushButton_publishChallengeTask.clicked.connect(self.PublishChallengeTask)
        self.pushButton_publishBountyTask.clicked.connect(self.PublishBountyTask)
        self.pushButton_classmode.clicked.connect(self.ClassMode)
        self.pushButton_afterclassmode.clicked.connect(self.AfterClassMode)
        self.stackedWidget.setCurrentIndex(2)
        self.comboBox_TeacherStudent.activated.connect(self.search)
        self.comboBox_Student.activated.connect(self.search)
        self.comboBox_Class.activated.connect(self.StudentShow)
        self.comboBox_User.currentTextChanged.connect(self.refreshframe)
        self.comboBox_User.activated.connect(self.AvatarHide)
        self.comboBox_Teacher.currentTextChanged.connect(self.stackedwidgetshow)
        self.comboBox_Student.activated.connect(self.TaskInfoShow)
        self.comboBox_TeacherClass.activated.connect(self.TeacherStudentShow)
        self.comboBox_TeacherStudent.currentTextChanged.connect(lambda: self.CheckboxStatus(False))
        self.comboBox_TeacherStudent.activated.connect(self.showstatus)
        self.pushButton_discard.clicked.connect(self.discardAll)
        self.pushButton_submit.clicked.connect(self.submit)
        self.pushButton_publishStoryTask.setDisabled(True)
        self.pushButton_publishChallengeTask.setDisabled(True)
        self.pushButton_publishBountyTask.setDisabled(True)
        self.pushButton_finishChallengeTask.clicked.connect(self.resetChallengeTask)
        self.pushButton_finishBountyTask.clicked.connect(self.resetBountyTask)
        self.pushButton_refreshLevel.clicked.connect(self.refreshLevel)
        self.pushButton_refreshDesignation.clicked.connect(self.refreshDesignation)
        self.pushButton_discard.hide()
        self.pushButton_submit.hide()
        self.pushButton_Lottery.clicked.connect(self.lottery)
        self.pushButton_Lock.clicked.connect(self.Lock)
        self.pushButton_SelectAll.clicked.connect(self.SelectAll)
        self.label_Avatar.hide()

    def lottery(self):
        self.chile_Win = ChildWindow()
        self.chile_Win.show()

    def classmode(self):
        self.chile_Win = ChildWindow()
        self.chile_Win.show()

    def UserLogin(self):
        if self.comboBox_User.currentText() == '星智博士':
            if self.lineEdit_teacher_password.text() == '123456':
                self.stackedWidget.setCurrentIndex(1)
                self.lineEdit_teacher_password.clear()
                self.stackedwidgetshow()
                self.lineEdit_teacher_password.setEnabled(False)
                self.pushButton_discard.show()
                self.pushButton_submit.show()
            else:
                self.lineEdit_teacher_password.clear()
        else:  # 教师登录
            try:
                Todo = leancloud.Object.extend('teacher')
                query = Todo.query
                query.equal_to('Teacher', self.comboBox_User.currentText())
                student_list = query.find()
                objectid = student_list[0]._attributes.get('objectId')
                todo = query.get(objectid)
                password = todo.get('Password')
                if self.lineEdit_teacher_password.text() == password:
                    self.stackedWidget.setCurrentIndex(0)
                    self.stackedWidget_2.setCurrentIndex(0)
                    self.lineEdit_teacher_password.clear()
                    self.hideWidget()
                    self.TeacherClassShow()
                    self.lineEdit_teacher_password.setEnabled(False)
                    pix = QPixmap('1.png')
                    self.label_Avatar.setPixmap(pix)
                    self.label_Avatar.show()
                    self.pushButton_discard.show()
                    self.pushButton_submit.show()

                else:
                    self.lineEdit_teacher_password.clear()
            except:
                pass

    def search(self):
        if self.lineEdit_search.text() != '':
            nametext = self.lineEdit_search.text()
        else:
            if self.stackedWidget_2.currentIndex() == 0:
                nametext = self.comboBox_TeacherStudent.currentText()
            else:
                nametext = self.comboBox_Student.currentText()
        # try:
        cursor = conn.cursor()
        sql = "select * from user where name='%s'" % (nametext)
        cursor.execute(sql)
        cursor.execute(sql)
        data = cursor.fetchall()
        objectID = data[0][1]
        searchurl = 'https://p14yxpmt.lc-cn-e1-shared.com/1.1/classes/user/' + objectID
        searchbody = {"sessionToken": "xxw5yzxpdvzhe8jgxp0eu7wa7"}
        response = requests.get(searchurl, data=json.dumps(searchbody), headers=headers)
        info = response.json()
        Name = info['Name']
        UserName = info['UserName']
        Designation = info['Designation']
        Stage = info['Stage']
        Age = info['Age']
        Exp = info['Exp']
        Level = info['Level']
        Gold = info['Gold']
        content = []
        content.append(Name)
        content.append(UserName)
        content.append(Age)
        content.append(Stage)
        content.append(Gold)
        content.append(Exp)
        content.append(Level)
        content.append(Designation)
        self.UserDataShow(content)
        self.widget.show()
        self.lineEdit_search.clear()

        # except:
        #     QMessageBox.information(self, '警告', '搜不到该学生的任何记录')

    def Lock(self):
        if self.pushButton_Lock.text() == '锁定修改':
            key = False
            self.LockCheckBox(key)
            self.pushButton_Lock.setText('解除锁定')
        else:
            if self.pushButton_Lock.text() == '解除锁定':
                key = True
                self.LockCheckBox(key)
                self.pushButton_Lock.setText('锁定修改')

    def hideWidget(self):
        self.widget_Task1.hide()
        self.widget_Task2.hide()
        self.widget_Task3.hide()
        self.widget_Task4.hide()
        self.widget_Task5.hide()
        self.widget_Task6.hide()
        self.widget_Task7.hide()
        self.widget_Task8.hide()
        self.widget_Task9.hide()
        self.widget_Task10.hide()

    def SelectAll(self):
        self.CheckboxStatus(True)

    def UserDataShow(self, content):
        for i in range(8):
            text1 = QTableWidgetItem(str(user[i]))
            text2 = QTableWidgetItem(str(content[i]))
            self.tableWidget_UserInfo.setItem(i, 0, text1)
            self.tableWidget_UserInfo.setItem(i, 1, text2)

    def stackedwidgetshow(self):
        self.stackedWidget.show()
        if self.stackedWidget.currentIndex() == 0:
            self.TeacherStudentShow()
        else:
            self.comboBox_Class.clear()
            self.ClassShow()

    def AvatarHide(self):
        self.label_Avatar.hide()

    def ClassMode(self):
        self.stackedWidget_2.setCurrentIndex(0)
        self.pushButton_classmode.setDisabled(True)
        self.pushButton_afterclassmode.setEnabled(True)
        self.TaskFinishStatusShow()

    def AfterClassMode(self):
        self.stackedWidget_2.setCurrentIndex(1)
        self.pushButton_afterclassmode.setDisabled(True)
        self.pushButton_classmode.setEnabled(True)

    def stackedwidgetshow2(self):
        self.stackedWidget.show()
        if self.comboBox_task.currentText() == '剧情任务(课上)':
            self.stackedWidget_2.setCurrentIndex(0)
        else:
            self.stackedWidget_2.setCurrentIndex(1)

    def showstatus(self):
        studentname = self.comboBox_TeacherStudent.currentText()
        cursor = conn.cursor()
        sql = "select * from user where name='%s'" % (studentname)
        cursor.execute(sql)
        data = cursor.fetchall()
        objectID = data[0][1]
        searchurl = 'https://p14yxpmt.lc-cn-e1-shared.com/1.1/classes/user/' + objectID
        searchbody = {"sessionToken": "xxw5yzxpdvzhe8jgxp0eu7wa7"}
        response = requests.get(searchurl, data=json.dumps(searchbody), headers=headers)
        info = response.json()
        StoryCheckpoint1 = info['StoryCheckpoint1']
        StoryCheckpoint2 = info['StoryCheckpoint2']
        StoryCheckpoint3 = info['StoryCheckpoint3']
        StoryCheckpoint4 = info['StoryCheckpoint4']
        StoryTaskFinish = info['StoryTaskFinish']
        ChallengeTaskFinish = info['ChallengeTaskFinish']
        BountyTaskFinish = info['BountyTaskFinish']
        try:
            if StoryCheckpoint1 == True:
                self.label_checkpoint1.setText('已完成')
                self.label_checkpoint1.setDisabled(True)
            if StoryCheckpoint2 == True:
                self.label_checkpoint2.setText('已完成')
                self.label_checkpoint2.setDisabled(True)
            if StoryCheckpoint3 == True:
                self.label_checkpoint3.setText('已完成')
                self.label_checkpoint3.setDisabled(True)
            if StoryCheckpoint4 == True:
                self.label_checkpoint4.setText('已完成')
                self.label_checkpoint4.setDisabled(True)
            if StoryTaskFinish == True:
                self.label_action1.setText('已完成')
                self.label_action1.setDisabled(True)
            if ChallengeTaskFinish == True:
                self.label_action1.setText('已完成')
                self.label_action1.setDisabled(True)
            if BountyTaskFinish == True:
                self.label_action1.setText('已完成')
                self.label_action1.setDisabled(True)
        except:
            pass

    def refreshframe(self):
        try:
            if self.lineEdit_teacher_password.isEnabled(False):
                self.label_Avatar.clear()
            else:
                pass
        except:
            pass
        self.lineEdit_teacher_password.setEnabled(True)
        self.stackedWidget.setCurrentIndex(2)
        self.lineEdit_teacher_password.clear()
        self.tableWidget_UserInfo.clear()
        self.comboBox_TeacherClass.clear()
        self.pushButton_discard.hide()
        self.pushButton_submit.hide()

    def TaskInfoShow(self):
        taskStatus = ['', '', '', '', '', '']
        classname = self.comboBox_Class.currentText()
        studentname = self.comboBox_Student.currentText()
        cursor = conn.cursor()
        sql = "select * from user where name='%s'" % (studentname)
        cursor.execute(sql)
        data = cursor.fetchall()
        objectID = data[0][1]
        searchurl = 'https://p14yxpmt.lc-cn-e1-shared.com/1.1/classes/user/' + objectID
        searchbody = {"sessionToken": "xxw5yzxpdvzhe8jgxp0eu7wa7"}
        response = requests.get(searchurl, data=json.dumps(searchbody), headers=headers)
        info = response.json()
        ChallengeTaskFinish = info['ChallengeTaskFinish']
        BountyTaskFinish = info['BountyTaskFinish']
        ChallengeTaskPublish = info['ChallengeTaskPublish']
        BountyTaskPublish = info['BountyTaskPublish']
        if ChallengeTaskFinish == True:
            taskStatus[1] = '已完成'
        else:
            taskStatus[1] = '未完成'
        if BountyTaskFinish == True:
            taskStatus[4] = '已完成'
        else:
            taskStatus[4] = '未完成'
        if ChallengeTaskPublish == True:
            taskStatus[0] = '已完成'
        else:
            taskStatus[0] = '未完成'
        if BountyTaskPublish == True:
            taskStatus[2] = '已完成'
        else:
            taskStatus[2] = '未完成'
        for i in range(6):
            text1 = QTableWidgetItem(str(taskInfo[i]))
            text2 = QTableWidgetItem(str(taskStatus[i]))
            self.tableWidget_TaskInfo.setItem(i, 0, text1)
            self.tableWidget_TaskInfo.setItem(i, 1, text2)

    def ClassShow(self):
        teachername = self.comboBox_Teacher.currentText()
        cursor = conn.cursor()
        sql = "select * from class where teacher='%s'" % (teachername)
        cursor.execute(sql)
        data = cursor.fetchall()
        list = []
        for i in data:
            list.append(i[0])
        self.comboBox_Class.addItems(list)
        self.StudentShow()

    def StudentShow(self):
        self.comboBox_Student.clear()
        classname = self.comboBox_Class.currentText()
        cursor = conn.cursor()
        sql = "select * from class where classname='%s'" % (classname)
        cursor.execute(sql)
        data = cursor.fetchall()
        list = []
        i = data[0]
        for j in range(2, 12):
            if i[j] != '':
                list.append(i[j])
        self.comboBox_Student.addItems(list)
        self.TaskInfoShow()

    def TaskWidgetShow(self, count):
        if count > 0:
            self.widget_Task1.show()
            self.label_student1.setText(self.comboBox_TeacherStudent.itemText(0))
            if count > 1:
                self.widget_Task2.show()
                self.label_student2.setText(self.comboBox_TeacherStudent.itemText(1))
                if count > 2:
                    self.widget_Task3.show()
                    self.label_student3.setText(self.comboBox_TeacherStudent.itemText(2))
                    if count > 3:
                        self.widget_Task4.show()
                        self.label_student4.setText(self.comboBox_TeacherStudent.itemText(3))
                        if count > 4:
                            self.widget_Task5.show()
                            self.label_student5.setText(self.comboBox_TeacherStudent.itemText(4))
                            if count > 5:
                                self.widget_Task6.show()
                                self.label_student6.setText(self.comboBox_TeacherStudent.itemText(5))
                                if count > 6:
                                    self.widget_Task7.show()
                                    self.label_student7.setText(self.comboBox_TeacherStudent.itemText(6))
                                    if count > 7:
                                        self.widget_Task8.show()
                                        self.label_student8.setText(self.comboBox_TeacherStudent.itemText(7))
                                        if count > 8:
                                            self.widget_Task9.show()
                                            self.label_student9.setText(self.comboBox_TeacherStudent.itemText(8))
                                            if count > 9:
                                                self.widget_Task10.show()
                                                self.label_student10.setText(self.comboBox_TeacherStudent.itemText(9))

    def TeacherClassShow(self):
        teachername = self.comboBox_User.currentText()
        Todo = leancloud.Object.extend('class')
        query = Todo.query
        query.equal_to('Teacher', teachername)
        student_list = query.find()
        list = []
        for i in student_list:
            objectid = i._attributes.get('objectId')
            todo = query.get(objectid)
            list.append(todo.get('Classname'))

        self.comboBox_TeacherClass.addItems(list)
        self.TeacherStudentShow()

    def TeacherStudentShow(self):
        self.comboBox_TeacherStudent.clear()
        checkboxkey = False
        self.CheckboxStatus(checkboxkey)
        classname = self.comboBox_TeacherClass.currentText()
        Todo = leancloud.Object.extend('class')
        query = Todo.query
        query.equal_to('Classname', classname)
        student_list = query.find()
        objectid = student_list[0]._attributes.get('objectId')
        todo = query.get(objectid)
        list = []
        for i in range(8):
            a = todo.get('Student' + str(i + 1))
            if a != '':
                list.append(a)
        self.comboBox_TeacherStudent.clear()
        self.comboBox_TeacherStudent.addItems(list)
        studentname = self.comboBox_TeacherStudent.currentText()
        cursor = conn.cursor()
        sql = "select * from user where name='%s'" % (studentname)
        cursor.execute(sql)
        data = cursor.fetchall()
        objectID = data[0][1]
        searchurl = 'https://p14yxpmt.lc-cn-e1-shared.com/1.1/classes/user/' + objectID
        response = requests.get(searchurl, data=json.dumps(searchbody), headers=headers)
        info = response.json()
        StroyTaskStatus = info['StoryTaskFinish']
        ChallengeTaskStatus = info['ChallengeTaskFinish']
        BountyTaskStatus = info['BountyTaskFinish']
        if StroyTaskStatus == False:
            self.pushButton_publishStoryTask.setEnabled(True)
        else:
            self.pushButton_publishStoryTask.setEnabled(False)
        if ChallengeTaskStatus == False:
            self.pushButton_publishChallengeTask.setEnabled(True)
        else:
            self.pushButton_publishChallengeTask.setEnabled(False)
        if BountyTaskStatus == False:
            self.pushButton_publishBountyTask.setEnabled(True)
        else:
            self.pushButton_publishBountyTask.setEnabled(False)

        self.showstatus()
        self.hideWidget()
        count = self.comboBox_TeacherStudent.count()
        self.TaskWidgetShow(count)
        self.TaskFinishStatusShow()

    def PublishStoryTask(self):
        pass
        # a = datetime.datetime.now()
        # classname = self.comboBox_TeacherClass.currentText()
        # Todo = leancloud.Object.extend('task')
        # query = Todo.query
        # query.equal_to('Classname', classname)
        # student_list = query.find()
        # objectid = student_list[0]._attributes.get('objectId')
        # todo = Todo.create_without_data(objectid)
        # todo.set('StoryTask', True)
        # # todo.save()
        # self.TeacherStudentShow()

    def PublishChallengeTask(self):
        pass
        # a = datetime.datetime.now()
        # classname = self.comboBox_TeacherClass.currentText()
        # Todo = leancloud.Object.extend('task')
        # query = Todo.query
        # query.equal_to('Class', classname)
        # student_list = query.find()
        # objectid = student_list[0]._attributes.get('objectId')
        # todo = Todo.create_without_data(objectid)
        # todo.set('ChallengeTask', True)
        # # todo.save()
        # self.TeacherStudentShow()

    def PublishBountyTask(self):
        pass
        # a = datetime.datetime.now()
        # classname = self.comboBox_TeacherClass.currentText()
        # Todo = leancloud.Object.extend('task')
        # query = Todo.query
        # query.equal_to('Class', classname)
        # student_list = query.find()
        # objectid = student_list[0]._attributes.get('objectId')
        # todo = Todo.create_without_data(objectid)
        # todo.set('BountyTask', True)
        # # todo.save()
        # self.TeacherStudentShow()

    def finishStoryTask(self):
        self.label_storyTaskFinishStatus.setEnabled(1)

    def finishChallengeTask(self):
        self.label_challengeTaskFinishStatus.setEnabled(1)

    def finishBountyTask(self):
        self.label_bountyTaskFinishStatus.setEnabled(1)

    def discardAll(self):
        if self.pushButton_Lock.text() == '锁定修改':
            button = QMessageBox.question(self, '提示', '是否确认放弃全部修改，该操作不可撤销！', QMessageBox.Yes | QMessageBox.No,
                                          QMessageBox.Yes)
            if button == QMessageBox.Yes:
                self.CheckboxStatus(False)
            else:
                pass
        else:
            pass

    def LockCheckBox(self, key):
        self.checkBox_student1_1.setEnabled(key)
        self.checkBox_student1_2.setEnabled(key)
        self.checkBox_student1_3.setEnabled(key)
        self.checkBox_student1_4.setEnabled(key)
        self.checkBox_student2_1.setEnabled(key)
        self.checkBox_student2_2.setEnabled(key)
        self.checkBox_student2_3.setEnabled(key)
        self.checkBox_student2_4.setEnabled(key)
        self.checkBox_student3_1.setEnabled(key)
        self.checkBox_student3_2.setEnabled(key)
        self.checkBox_student3_3.setEnabled(key)
        self.checkBox_student3_4.setEnabled(key)
        self.checkBox_student4_1.setEnabled(key)
        self.checkBox_student4_2.setEnabled(key)
        self.checkBox_student4_3.setEnabled(key)
        self.checkBox_student4_4.setEnabled(key)
        self.checkBox_student5_1.setEnabled(key)
        self.checkBox_student5_2.setEnabled(key)
        self.checkBox_student5_3.setEnabled(key)
        self.checkBox_student5_4.setEnabled(key)
        self.checkBox_student6_1.setEnabled(key)
        self.checkBox_student6_2.setEnabled(key)
        self.checkBox_student6_3.setEnabled(key)
        self.checkBox_student6_4.setEnabled(key)
        self.checkBox_student7_1.setEnabled(key)
        self.checkBox_student7_2.setEnabled(key)
        self.checkBox_student7_3.setEnabled(key)
        self.checkBox_student7_4.setEnabled(key)
        self.checkBox_student8_1.setEnabled(key)
        self.checkBox_student8_2.setEnabled(key)
        self.checkBox_student8_3.setEnabled(key)
        self.checkBox_student8_4.setEnabled(key)
        self.checkBox_student9_1.setEnabled(key)
        self.checkBox_student9_2.setEnabled(key)
        self.checkBox_student9_3.setEnabled(key)
        self.checkBox_student9_4.setEnabled(key)
        self.checkBox_student10_1.setEnabled(key)
        self.checkBox_student10_2.setEnabled(key)
        self.checkBox_student10_3.setEnabled(key)
        self.checkBox_student10_4.setEnabled(key)

    def CheckboxStatus(self, checkboxkey):
        try:
            if self.pushButton_Lock.text() == '锁定修改':
                self.checkBox_student1_1.setChecked(checkboxkey)
                self.checkBox_student1_2.setChecked(checkboxkey)
                self.checkBox_student1_3.setChecked(checkboxkey)
                self.checkBox_student1_4.setChecked(checkboxkey)
                self.checkBox_student2_1.setChecked(checkboxkey)
                self.checkBox_student2_2.setChecked(checkboxkey)
                self.checkBox_student2_3.setChecked(checkboxkey)
                self.checkBox_student2_4.setChecked(checkboxkey)
                self.checkBox_student3_1.setChecked(checkboxkey)
                self.checkBox_student3_2.setChecked(checkboxkey)
                self.checkBox_student3_3.setChecked(checkboxkey)
                self.checkBox_student3_4.setChecked(checkboxkey)
                self.checkBox_student4_1.setChecked(checkboxkey)
                self.checkBox_student4_2.setChecked(checkboxkey)
                self.checkBox_student4_3.setChecked(checkboxkey)
                self.checkBox_student4_4.setChecked(checkboxkey)
                self.checkBox_student5_1.setChecked(checkboxkey)
                self.checkBox_student5_2.setChecked(checkboxkey)
                self.checkBox_student5_3.setChecked(checkboxkey)
                self.checkBox_student5_4.setChecked(checkboxkey)
                self.checkBox_student6_1.setChecked(checkboxkey)
                self.checkBox_student6_2.setChecked(checkboxkey)
                self.checkBox_student6_3.setChecked(checkboxkey)
                self.checkBox_student6_4.setChecked(checkboxkey)
                self.checkBox_student7_1.setChecked(checkboxkey)
                self.checkBox_student7_2.setChecked(checkboxkey)
                self.checkBox_student7_3.setChecked(checkboxkey)
                self.checkBox_student7_4.setChecked(checkboxkey)
                self.checkBox_student8_1.setChecked(checkboxkey)
                self.checkBox_student8_2.setChecked(checkboxkey)
                self.checkBox_student8_3.setChecked(checkboxkey)
                self.checkBox_student8_4.setChecked(checkboxkey)
                self.checkBox_student9_1.setChecked(checkboxkey)
                self.checkBox_student9_2.setChecked(checkboxkey)
                self.checkBox_student9_3.setChecked(checkboxkey)
                self.checkBox_student9_4.setChecked(checkboxkey)
                self.checkBox_student10_1.setChecked(checkboxkey)
                self.checkBox_student10_2.setChecked(checkboxkey)
                self.checkBox_student10_3.setChecked(checkboxkey)
                self.checkBox_student10_4.setChecked(checkboxkey)
            else:
                pass
        except:
            pass

    def CollectScore(self):
        TotalScore = [['', 0, 0, 0, 0], ['', 0, 0, 0, 0], ['', 0, 0, 0, 0], ['', 0, 0, 0, 0], ['', 0, 0, 0, 0],
                      ['', 0, 0, 0, 0], ['', 0, 0, 0, 0], ['', 0, 0, 0, 0], ['', 0, 0, 0, 0], ['', 0, 0, 0, 0]]
        for i in range(10):
            TotalScore[i][0] = self.comboBox_TeacherStudent.itemText(i)
        if TotalScore[0][0] != '':
            if self.checkBox_student1_1.isChecked() == True:
                TotalScore[0][1] = 1
            if self.checkBox_student1_2.isChecked() == True:
                TotalScore[0][2] = 1
            if self.checkBox_student1_3.isChecked() == True:
                TotalScore[0][3] = 1
            if self.checkBox_student1_4.isChecked() == True:
                TotalScore[0][4] = 1
            if TotalScore[1][0] != '':
                if self.checkBox_student2_1.isChecked() == True:
                    TotalScore[1][1] = 1
                if self.checkBox_student2_2.isChecked() == True:
                    TotalScore[1][2] = 1
                if self.checkBox_student2_3.isChecked() == True:
                    TotalScore[1][3] = 1
                if self.checkBox_student2_4.isChecked() == True:
                    TotalScore[1][4] = 1
                if TotalScore[2][0] != '':
                    if self.checkBox_student3_1.isChecked() == True:
                        TotalScore[2][1] = 1
                    if self.checkBox_student3_2.isChecked() == True:
                        TotalScore[2][2] = 1
                    if self.checkBox_student3_3.isChecked() == True:
                        TotalScore[2][3] = 1
                    if self.checkBox_student3_4.isChecked() == True:
                        TotalScore[2][4] = 1
                    if TotalScore[3][0] != '':
                        if self.checkBox_student4_1.isChecked() == True:
                            TotalScore[3][1] = 1
                        if self.checkBox_student4_2.isChecked() == True:
                            TotalScore[3][2] = 1
                        if self.checkBox_student4_3.isChecked() == True:
                            TotalScore[3][3] = 1
                        if self.checkBox_student4_4.isChecked() == True:
                            TotalScore[3][4] = 1
                        if TotalScore[4][0] != '':
                            if self.checkBox_student5_1.isChecked() == True:
                                TotalScore[4][1] = 1
                            if self.checkBox_student5_2.isChecked() == True:
                                TotalScore[4][2] = 1
                            if self.checkBox_student5_3.isChecked() == True:
                                TotalScore[4][3] = 1
                            if self.checkBox_student5_4.isChecked() == True:
                                TotalScore[4][4] = 1
                            if TotalScore[5][0] != '':
                                if self.checkBox_student6_1.isChecked() == True:
                                    TotalScore[5][1] = 1
                                if self.checkBox_student6_2.isChecked() == True:
                                    TotalScore[5][2] = 1
                                if self.checkBox_student6_3.isChecked() == True:
                                    TotalScore[5][3] = 1
                                if self.checkBox_student6_4.isChecked() == True:
                                    TotalScore[5][4] = 1
                                if TotalScore[6][0] != '':
                                    if self.checkBox_student7_1.isChecked() == True:
                                        TotalScore[6][1] = 1
                                    if self.checkBox_student7_2.isChecked() == True:
                                        TotalScore[6][2] = 1
                                    if self.checkBox_student7_3.isChecked() == True:
                                        TotalScore[6][3] = 1
                                    if self.checkBox_student7_4.isChecked() == True:
                                        TotalScore[6][4] = 1
                                    if TotalScore[7][0] != '':
                                        if self.checkBox_student8_1.isChecked() == True:
                                            TotalScore[7][1] = 1
                                        if self.checkBox_student8_2.isChecked() == True:
                                            TotalScore[7][2] = 1
                                        if self.checkBox_student8_3.isChecked() == True:
                                            TotalScore[7][3] = 1
                                        if self.checkBox_student8_4.isChecked() == True:
                                            TotalScore[7][4] = 1
                                        if TotalScore[8][0] != '':
                                            if self.checkBox_student9_1.isChecked() == True:
                                                TotalScore[8][1] = 1
                                            if self.checkBox_student9_2.isChecked() == True:
                                                TotalScore[8][2] = 1
                                            if self.checkBox_student9_3.isChecked() == True:
                                                TotalScore[8][3] = 1
                                            if self.checkBox_student9_4.isChecked() == True:
                                                TotalScore[8][4] = 1
                                            if TotalScore[9][0] != '':
                                                if self.checkBox_student10_1.isChecked() == True:
                                                    TotalScore[9][1] = 1
                                                if self.checkBox_student10_2.isChecked() == True:
                                                    TotalScore[9][2] = 1
                                                if self.checkBox_student10_3.isChecked() == True:
                                                    TotalScore[9][3] = 1
                                                if self.checkBox_student10_4.isChecked() == True:
                                                    TotalScore[9][4] = 1
        return TotalScore

    def TaskFinishStatusShow(self):
        if self.stackedWidget_2.currentIndex() == 0:
            StoryFinishStatus = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            for i in range(self.comboBox_TeacherStudent.count()):
                studentname = self.comboBox_TeacherStudent.itemText(i)
                cursor = conn.cursor()
                sql = "select * from user where name='%s'" % (studentname)
                cursor.execute(sql)
                data = cursor.fetchall()
                print(data)
                objectID = data[0][1]
                print(objectID)
                searchurl = 'https://p14yxpmt.lc-cn-e1-shared.com/1.1/classes/user/' + objectID
                searchbody = {"sessionToken": "xxw5yzxpdvzhe8jgxp0eu7wa7"}
                response = requests.get(searchurl, data=json.dumps(searchbody), headers=headers)
                info = response.json()
                SC1 = info['StoryCheckpoint1']
                SC2 = info['StoryCheckpoint2']
                SC3 = info['StoryCheckpoint3']
                SC4 = info['StoryCheckpoint4']
                if SC1 == SC2 == SC3 == SC4 == True:
                    StoryFinishStatus[i] = 1
            if StoryFinishStatus[0] == 1:
                self.widget_Task1.setDisabled(True)
            if StoryFinishStatus[1] == 1:
                self.widget_Task2.setDisabled(True)
            if StoryFinishStatus[2] == 1:
                self.widget_Task3.setDisabled(True)
            if StoryFinishStatus[3] == 1:
                self.widget_Task4.setDisabled(True)
            if StoryFinishStatus[4] == 1:
                self.widget_Task5.setDisabled(True)
            if StoryFinishStatus[5] == 1:
                self.widget_Task6.setDisabled(True)
            if StoryFinishStatus[6] == 1:
                self.widget_Task7.setDisabled(True)
            if StoryFinishStatus[7] == 1:
                self.widget_Task8.setDisabled(True)
            if StoryFinishStatus[8] == 1:
                self.widget_Task9.setDisabled(True)
            if StoryFinishStatus[9] == 1:
                self.widget_Task10.setDisabled(True)

    def submit(self):
        global StoryTaskGold
        button = QMessageBox.question(self, '提示', '是否确认提交修改，该操作不可撤销！', QMessageBox.Yes | QMessageBox.No,
                                      QMessageBox.Yes)
        if button == QMessageBox.Yes:
            # 教师界面
            if self.stackedWidget.currentIndex() == 0:
                # 课上关卡
                if self.stackedWidget_2.currentIndex() == 0:
                    checkdata = self.CollectScore()
                    for i in checkdata:
                        Gold = 0
                        Exp = 0
                        name = i[0]
                        if name != '':
                            studentname = name
                            Gold = (i[1] + i[2] + i[3] + i[4]) * 3
                            self.AddGold(studentname, Gold)
                            Exp = (i[1] + i[2] + i[3] + i[4]) * 3
                            self.AddExp(studentname, Exp)
                # 剧情+挑战+赏金
                if self.stackedWidget_2.currentIndex() == 1:
                    Exp = 0
                    Gold = 0
                    StoryTaskExp = 0
                    ChallengeTaskExp = 0
                    StoryTaskGold = 0
                    BountyTaskGold = 0
                    studentname = self.comboBox_TeacherStudent.currentText()
                    Todo = leancloud.Object.extend('user')
                    query = Todo.query
                    query.equal_to('Name', studentname)
                    student_list = query.find()
                    objectid = student_list[0]._attributes.get('objectId')
                    todo = query.get(objectid)
                    stage = todo.get('Stage')
                    if self.radioButton_FinishStoryTask.isChecked():
                        StoryTaskGold = 5
                        StoryTaskExp = (8 + 2 * stage) * 3
                    else:
                        pass
                    if self.radioButton_GoodStoryTask.isChecked():
                        StoryTaskGold = 7
                        StoryTaskExp = (8 + 2 * stage) * 3
                    else:
                        pass
                    if self.radioButton_ExcellentStoryTask.isChecked():
                        StoryTaskGold = 10
                        StoryTaskExp = (8 + 2 * stage) * 3
                    else:
                        pass
                    if self.checkBox_ExtraReward.isChecked():
                        StoryTaskGold += 50
                    else:
                        pass
                    if self.radioButton_ChallengeTaskFinish.isChecked():
                        ChallengeTaskExp = ((8 + 2 * stage) * 16) * 3
                    else:
                        pass
                    if self.radioButton_BountyTaskFinish.isChecked():
                        BountyTaskGold = (50 + (stage - 1) * 10) * 3
                    else:
                        pass
                    Exp = int(StoryTaskExp + ChallengeTaskExp)
                    Gold = int(StoryTaskGold + BountyTaskGold)
                    self.AddExp(studentname, Exp)
                    self.AddGold(studentname, Gold)

        else:
            pass

    def resetChallengeTask(self):
        button1 = QMessageBox.question(self, '提示', '是否确认提交修改，该操作不可撤销！', QMessageBox.Yes | QMessageBox.No,
                                       QMessageBox.Yes)
        if button1 == QMessageBox.Yes:
            button2 = QMessageBox.question(self, '警告', '真的确定吗？', QMessageBox.Yes | QMessageBox.No,
                                           QMessageBox.Yes)
            if button2 == QMessageBox.Yes:
                # Todo = leancloud.Object.extend('')
                # query = Todo.query
                # student_list = query.find()
                # for i in student_list:
                #     objectid = i._attributes.get('objectId')
                #     todo = Todo.create_without_data(objectid)
                #     todo.set()
                #     todo.save()
                pass

    def resetBountyTask(self):
        button1 = QMessageBox.question(self, '提示', '是否确认提交修改，该操作不可撤销！', QMessageBox.Yes | QMessageBox.No,
                                       QMessageBox.Yes)
        if button1 == QMessageBox.Yes:
            button2 = QMessageBox.question(self, '警告', '真的确定吗？', QMessageBox.Yes | QMessageBox.No,
                                           QMessageBox.Yes)
            if button2 == QMessageBox.Yes:
                # Todo = leancloud.Object.extend('Test')
                # query = Todo.query
                # student_list = query.find()
                # for i in student_list:
                #     objectid = i._attributes.get('objectId')
                #     todo = Todo.create_without_data(objectid)
                #     todo.set()
                #     todo.save()
                pass

    def refreshLevel(self):
        button1 = QMessageBox.question(self, '提示', '是否确认提交，该操作不可撤销！', QMessageBox.Yes | QMessageBox.No,
                                       QMessageBox.Yes)
        if button1 == QMessageBox.Yes:
            button2 = QMessageBox.question(self, '警告', '真的确定吗？', QMessageBox.Yes | QMessageBox.No,
                                           QMessageBox.Yes)
            if button2 == QMessageBox.Yes:
                # Todo = leancloud.Object.extend('Test')
                # query = Todo.query
                # student_list = query.find()
                # for i in student_list:
                #     objectid = i._attributes.get('objectId')
                #     todo = Todo.create_without_data(objectid)
                #     todo.set('ID', 110)
                #     todo.save()
                pass

    def refreshDesignation(self):
        button1 = QMessageBox.question(self, '提示', '是否确认提交修改，该操作不可撤销！', QMessageBox.Yes | QMessageBox.No,
                                       QMessageBox.Yes)
        if button1 == QMessageBox.Yes:
            button2 = QMessageBox.question(self, '警告', '真的确定吗？', QMessageBox.Yes | QMessageBox.No,
                                           QMessageBox.Yes)
            if button2 == QMessageBox.Yes:
                # Todo = leancloud.Object.extend('Test')
                # query = Todo.query
                # student_list = query.find()
                pass
                # for i in student_list:
                #     objectid = i._attributes.get('objectId')
                #     todo = Todo.create_without_data(objectid)
                #     todo.set('ID', 110)
                #     todo.save()

    def AddExp(self, studentname, Exp):
        pass
        # # print(Exp)
        # # print(studentname)
        # Todo = leancloud.Object.extend('user')
        # # query = Todo.query
        # # query.equal_to('Name', name)
        # # student_list = query.find()
        # # objectid = student_list[0]._attributes.get('objectId')
        # # todo = Todo.create_without_data(objectid)
        # # todo.set('Exp', exp)
        # # todo.save()

    def AddGold(self, studentname, Gold):
        pass
        # print(Gold)
        # print(studentname)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = mywindow()
    ui.show()
    sys.exit(app.exec_())
