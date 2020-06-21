import datetime
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QTableWidgetItem, QApplication, QHeaderView, QMessageBox, QWidget
from UI import Ui_HomeLabTool
import leancloud

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
user = ['姓名', '用户名', '密码', '注册时间', '年龄', '课程阶段', '玩学创币', '经验', '等级', '称号']
teacher = ['魏泽宇', '刘天鹏', '薯条老师', '徐津', '朱敏', '啾啾', '波波', '刘攀', '糖果老师']
stage = ['a', 'b', 'Lasy', 'NewKicky', 'HUNA', 'EV3', 'Scratch', 'Arduino', 'Python', 'C++']
taskInfo = ['挑战任务发布状态', '挑战任务完成情况', '赏金任务发布状态', '赏金任务入场人数', '赏金任务完成情况', '本月发放玩学创币总数']
taskStatus = ['', '', '', '', '', '']
global content
global player
global data
global lock


class mywindow(QtWidgets.QWidget, Ui_HomeLabTool):
    _signal = pyqtSignal(str)

    def __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)
        self.tableWidget.setShowGrid(False)
        self.tableWidget_2.setShowGrid(False)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.pushButton_search.clicked.connect(self.search)
        self.pushButton_finish.clicked.connect(self.score)
        self.pushButton_confirm.clicked.connect(self.UserLogin)
        self.pushButton_publishStoryTask.clicked.connect(self.PublishStoryTask)
        self.pushButton_publishChallengeTask.clicked.connect(self.PublishChallengeTask)
        self.pushButton_publishBountyTask.clicked.connect(self.PublishBountyTask)
        self.stackedWidget.setCurrentIndex(2)
        self.comboBox_Class.activated.connect(self.StudentShow)
        self.comboBox_User.currentTextChanged.connect(self.refreshframe)
        self.comboBox_User.activated.connect(self.AvatarHide)
        self.comboBox_Teacher.currentTextChanged.connect(self.stackedwidgetshow)
        self.comboBox_Student.activated.connect(self.TaskInfoShow)
        self.comboBox_task.currentTextChanged.connect(self.stackedwidgetshow2)
        self.comboBox_TeacherClass.activated.connect(self.TeacherStudentShow)
        self.comboBox_TeacherStudent.currentTextChanged.connect(self.discard)
        self.comboBox_TeacherStudent.activated.connect(self.showstatus)
        self.pushButton_discard.clicked.connect(self.discard)
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

        nametext = self.lineEdit_search.text()
        try:
            Todo = leancloud.Object.extend('user')
            query = Todo.query
            query.equal_to('Name', nametext)
            student_list = query.find()
            objectid = student_list[0]._attributes.get('objectId')
            todo = query.get(objectid)
            teacher = todo.get('Teacher')
            username = todo.get('UserName')
            password = todo.get('Password')
            time = todo.get('Time')
            name = todo.get('Name')
            age = todo.get('Age')
            stage = todo.get('Stage')
            gold = todo.get('Gold')
            exp = todo.get('Exp')
            level = todo.get('Level')
            designation = todo.get('Designation')
            content = []
            content.append(name)
            content.append(username)
            content.append(time.date())
            content.append(name)
            content.append(age)
            content.append(stage)
            content.append(gold)
            content.append(exp)
            content.append(level)
            content.append(designation)
            self.UserDataShow(content)
            self.lineEdit_search.clear()
            self.widget.show()
        except:
            QMessageBox.information(self, '警告', '搜不到该学生的任何记录')

    def UserDataShow(self, content):
        for i in range(10):
            text1 = QTableWidgetItem(str(user[i]))
            text2 = QTableWidgetItem(str(content[i]))
            self.tableWidget.setItem(i, 0, text1)
            self.tableWidget.setItem(i, 1, text2)

    def stackedwidgetshow(self):
        self.stackedWidget.show()
        if self.stackedWidget.currentIndex() == 0:
            self.TeacherStudentShow()
        else:
            self.comboBox_Class.clear()
            self.ClassShow()

    def AvatarHide(self):
        self.label_Avatar.hide()

    def stackedwidgetshow2(self):
        self.stackedWidget.show()
        if self.comboBox_task.currentText() == '剧情任务(课上)':
            self.stackedWidget_2.setCurrentIndex(0)
        else:
            self.stackedWidget_2.setCurrentIndex(1)

    def showstatus(self):
        studentname = self.comboBox_TeacherStudent.currentText()
        UserTodo = leancloud.Object.extend('user')
        UserQuery = UserTodo.query
        UserQuery.equal_to('Name', studentname)
        student_list = UserQuery.find()
        objectid = student_list[0]._attributes.get('objectId')
        usertodo = UserQuery.get(objectid)
        StoryCheckpoint1 = usertodo.get('StoryCheckpoint1')
        StoryCheckpoint2 = usertodo.get('StoryCheckpoint2')
        StoryCheckpoint3 = usertodo.get('StoryCheckpoint3')
        StoryCheckpoint4 = usertodo.get('StoryCheckpoint4')
        StoryTask = usertodo.get('StoryTask')
        ChallengeTask = usertodo.get('ChallengeTask')
        BountyTask = usertodo.get('BountyTask')
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
            if StoryTask == True:
                self.label_action1.setText('已完成')
                self.label_action1.setDisabled(True)
            if ChallengeTask == True:
                self.label_action1.setText('已完成')
                self.label_action1.setDisabled(True)
            if BountyTask == True:
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
        self.comboBox_TeacherClass.clear()
        self.pushButton_discard.hide()
        self.pushButton_submit.hide()

    def TaskInfoShow(self):
        taskStatus = ['', '', '', '', '', '']
        classname = self.comboBox_Class.currentText()
        studentname = self.comboBox_Student.currentText()
        UserTodo = leancloud.Object.extend('user')
        UserQuery = UserTodo.query
        UserQuery.equal_to('Name', studentname)
        student_list = UserQuery.find()
        objectid = student_list[0]._attributes.get('objectId')
        usertodo = UserQuery.get(objectid)
        ChallengeFinishTaskStatus = usertodo.get('ChallengeTask')
        BountyFinishTaskStatus = usertodo.get('BountyTask')
        TaskTodo = leancloud.Object.extend('task')
        TaskQuery = TaskTodo.query
        TaskQuery.equal_to('Class', classname)
        student_list = TaskQuery.find()
        objectid = student_list[0]._attributes.get('objectId')
        tsaktodo = TaskQuery.get(objectid)
        ChallengePublishTaskStatus = tsaktodo.get('ChallengeTask')
        BountyPublishTaskStatus = tsaktodo.get('BountyTask')
        if ChallengeFinishTaskStatus == True:
            taskStatus[1] = '已完成'
        else:
            taskStatus[1] = '未完成'
        if BountyFinishTaskStatus == True:
            taskStatus[4] = '已完成'
        else:
            taskStatus[4] = '未完成'
        if ChallengePublishTaskStatus == True:
            taskStatus[0] = '已完成'
        else:
            taskStatus[0] = '未完成'
        if BountyPublishTaskStatus == True:
            taskStatus[2] = '已完成'
        else:
            taskStatus[2] = '未完成'
        for i in range(6):
            text1 = QTableWidgetItem(str(taskInfo[i]))
            text2 = QTableWidgetItem(str(taskStatus[i]))
            self.tableWidget_2.setItem(i, 0, text1)
            self.tableWidget_2.setItem(i, 1, text2)

    def ClassShow(self):
        teachername = self.comboBox_Teacher.currentText()
        Todo = leancloud.Object.extend('class')
        query = Todo.query
        query.equal_to('Teacher', teachername)
        student_list = query.find()
        list = []
        for i in student_list:
            objectid = i._attributes.get('objectId')
            todo = query.get(objectid)
            list.append(todo.get('Class'))
        self.comboBox_Class.addItems(list)
        self.StudentShow()

    def StudentShow(self):
        self.comboBox_Student.clear()
        classname = self.comboBox_Class.currentText()
        Todo = leancloud.Object.extend('class')
        query = Todo.query
        query.equal_to('Class', classname)
        student_list = query.find()
        objectid = student_list[0]._attributes.get('objectId')
        todo = query.get(objectid)
        list = []
        for i in range(8):
            a = todo.get('Student' + str(i + 1))
            if a != '':
                list.append(a)
        self.comboBox_Student.addItems(list)
        self.TaskInfoShow()

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
            list.append(todo.get('Class'))

        self.comboBox_TeacherClass.addItems(list)

    def TeacherStudentShow(self):
        self.comboBox_TeacherStudent.clear()
        self.discard()
        classname = self.comboBox_TeacherClass.currentText()
        Todo = leancloud.Object.extend('class')
        query = Todo.query
        query.equal_to('Class', classname)
        student_list = query.find()
        objectid = student_list[0]._attributes.get('objectId')
        todo = query.get(objectid)
        list = []
        for i in range(8):
            a = todo.get('Student' + str(i + 1))
            if a != '':
                list.append(a)
        Todo = leancloud.Object.extend('task')
        query = Todo.query
        query.equal_to('Class', classname)
        student_list = query.find()
        objectid = student_list[0]._attributes.get('objectId')
        todo = query.get(objectid)
        StroyTaskStatus = todo.get('StoryTask')
        ChallengeTaskStatus = todo.get('ChallengeTask')
        BountyTaskStatus = todo.get('BountyTask')
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
        self.comboBox_TeacherStudent.clear()
        self.comboBox_TeacherStudent.addItems(list)
        self.showstatus()

    def PublishStoryTask(self):
        a = datetime.datetime.now()
        classname = self.comboBox_TeacherClass.currentText()
        Todo = leancloud.Object.extend('task')
        query = Todo.query
        query.equal_to('Class', classname)
        student_list = query.find()
        objectid = student_list[0]._attributes.get('objectId')
        todo = Todo.create_without_data(objectid)
        todo.set('StoryTask', True)
        todo.save()
        self.TeacherStudentShow()

    def PublishChallengeTask(self):
        a = datetime.datetime.now()
        classname = self.comboBox_TeacherClass.currentText()
        Todo = leancloud.Object.extend('task')
        query = Todo.query
        query.equal_to('Class', classname)
        student_list = query.find()
        objectid = student_list[0]._attributes.get('objectId')
        todo = Todo.create_without_data(objectid)
        todo.set('ChallengeTask', True)
        todo.save()
        self.TeacherStudentShow()

    def PublishBountyTask(self):
        a = datetime.datetime.now()
        classname = self.comboBox_TeacherClass.currentText()
        Todo = leancloud.Object.extend('task')
        query = Todo.query
        query.equal_to('Class', classname)
        student_list = query.find()
        objectid = student_list[0]._attributes.get('objectId')
        todo = Todo.create_without_data(objectid)
        todo.set('BountyTask', True)
        todo.save()
        self.TeacherStudentShow()

    def finishStoryTask(self):
        self.label_storyTaskFinishStatus.setEnabled(1)

    def finishChallengeTask(self):
        self.label_challengeTaskFinishStatus.setEnabled(1)

    def finishBountyTask(self):
        self.label_bountyTaskFinishStatus.setEnabled(1)

    def score(self):
        try:
            if self.stackedWidget_2.currentIndex() == 0:
                if self.radioButton_checkpoint1.isChecked() == True:
                    self.label_checkpoint1.setText('完成')
                if self.radioButton_checkpoint2.isChecked() == True:
                    self.label_checkpoint2.setText('完成')
                if self.radioButton_checkpoint3.isChecked() == True:
                    self.label_checkpoint3.setText('完成')
                if self.radioButton_checkpoint4.isChecked() == True:
                    self.label_checkpoint4.setText('完成')
            else:
                if self.comboBox_task.currentText() == '剧情任务(课后)':
                    if self.radioButton_S.isChecked() == True:
                        self.label_action1.setText('完成')
                    if self.radioButton_SS.isChecked() == True:
                        self.label_action1.setText('优秀')
                    if self.radioButton_SSS.isChecked() == True:
                        self.label_action1.setText('极佳')
                if self.comboBox_task.currentText() == '挑战任务':
                    if self.radioButton_S.isChecked() == True:
                        self.label_action2.setText('完成')
                    if self.radioButton_SS.isChecked() == True:
                        self.label_action2.setText('优秀')
                    if self.radioButton_SSS.isChecked() == True:
                        self.label_action2.setText('极佳')
                if self.comboBox_task.currentText() == '赏金任务':
                    if self.radioButton_S.isChecked() == True:
                        self.label_action3.setText('完成')
                    if self.radioButton_SS.isChecked() == True:
                        self.label_action3.setText('优秀')
                    if self.radioButton_SSS.isChecked() == True:
                        self.label_action3.setText('极佳')
        except:
            pass

    def discard(self):
        self.label_checkpoint1.clear()
        self.label_checkpoint2.clear()
        self.label_checkpoint3.clear()
        self.label_checkpoint4.clear()
        self.label_action1.clear()
        self.label_action2.clear()
        self.label_action3.clear()

    def submit(self):
        button = QMessageBox.question(self, '提示', '是否确认提交修改，该操作不可撤销！', QMessageBox.Yes | QMessageBox.No,
                                      QMessageBox.Yes)
        if button == QMessageBox.Yes:

            if self.stackedWidget.currentIndex() == 0:  # 教师界面
                if self.stackedWidget_2.currentIndex() == 0:  # 课上关卡
                    name = self.comboBox_TeacherStudent.currentText()
                    Todo = leancloud.Object.extend('user')
                    query = Todo.query
                    query.equal_to('Name', name)
                    student_list = query.find()
                    objectid = student_list[0]._attributes.get('objectId')
                    todo = query.get(objectid)
                    stage = todo.get('Stage')
                    gold = todo.get('Gold')
                    exp = todo.get('Exp')
                    level = todo.get('Level')
                    todo = Todo.create_without_data(objectid)
                    taskstatus = [False, False, False, False]
                    if self.label_checkpoint1.text() == '完成':
                        taskstatus[0] = True
                        gold += 3
                        exp += inclassexp[int(stage) - 1]
                    if self.label_checkpoint2.text() == '完成':
                        taskstatus[1] = True
                        gold += 3
                        exp += inclassexp[int(stage) - 1]
                    if self.label_checkpoint3.text() == '完成':
                        taskstatus[2] = True
                        gold += 3
                        exp += inclassexp[int(stage) - 1]
                    if self.label_checkpoint4.text() == '完成':
                        taskstatus[3] = True
                        gold += 3
                        exp += inclassexp[int(stage) - 1]
                    taskstatus = list(taskstatus)
                    name = self.comboBox_TeacherStudent.currentText()
                    print(name)
                    Todo = leancloud.Object.extend('user')
                    query = Todo.query
                    query.equal_to('Name', name)
                    student_list = query.find()
                    objectid = student_list[0]._attributes.get('objectId')
                    print(objectid)
                    todo = Todo.create_without_data(objectid)
                    todo.set('StoryCheckpoint1', taskstatus[0])
                    todo.set('StoryCheckpoint2', taskstatus[1])
                    todo.set('StoryCheckpoint3', taskstatus[2])
                    todo.set('StoryCheckpoint4', taskstatus[3])
                    todo.set('Exp', exp)
                    todo.set('Gold', gold)
                    todo.save()
                if self.stackedWidget_2.currentIndex() == 1:  # 课后任务+挑战+赏金
                    name = self.comboBox_TeacherStudent.currentText()
                    Todo = leancloud.Object.extend('user')
                    query = Todo.query
                    query.equal_to('Name', name)
                    student_list = query.find()
                    objectid = student_list[0]._attributes.get('objectId')
                    todo = query.get(objectid)
                    stage = todo.get('Stage')
                    gold = todo.get('Gold')
                    exp = todo.get('Exp')
                    level = todo.get('Level')
                    todo = Todo.create_without_data(objectid)
                    taskstatus = [False, False, False]
                    taskstatus = list(taskstatus)
                    todo.set('StoryTask', taskstatus[0])
                    todo.set('ChallengeTask', taskstatus[1])
                    todo.set('BountyTask', taskstatus[2])
                    todo.set('Exp', exp)
                    todo.set('Level', level)
                    todo.set('Gold', gold)
        else:
            pass

    def resetChallengeTask(self):
        button1 = QMessageBox.question(self, '提示', '是否确认提交修改，该操作不可撤销！', QMessageBox.Yes | QMessageBox.No,
                                       QMessageBox.Yes)
        if button1 == QMessageBox.Yes:
            button2 = QMessageBox.question(self, '警告', '真的确定吗？', QMessageBox.Yes | QMessageBox.No,
                                           QMessageBox.Yes)
            if button2 == QMessageBox.Yes:
                Todo = leancloud.Object.extend('')
                query = Todo.query
                student_list = query.find()
                for i in student_list:
                    objectid = i._attributes.get('objectId')
                    todo = Todo.create_without_data(objectid)
                    todo.set()
                    todo.save()

    def resetBountyTask(self):
        button1 = QMessageBox.question(self, '提示', '是否确认提交修改，该操作不可撤销！', QMessageBox.Yes | QMessageBox.No,
                                       QMessageBox.Yes)
        if button1 == QMessageBox.Yes:
            button2 = QMessageBox.question(self, '警告', '真的确定吗？', QMessageBox.Yes | QMessageBox.No,
                                           QMessageBox.Yes)
            if button2 == QMessageBox.Yes:
                Todo = leancloud.Object.extend('Test')
                query = Todo.query
                student_list = query.find()
                for i in student_list:
                    objectid = i._attributes.get('objectId')
                    todo = Todo.create_without_data(objectid)
                    todo.set()
                    todo.save()

    def refreshLevel(self):
        button1 = QMessageBox.question(self, '提示', '是否确认提交，该操作不可撤销！', QMessageBox.Yes | QMessageBox.No,
                                       QMessageBox.Yes)
        if button1 == QMessageBox.Yes:
            button2 = QMessageBox.question(self, '警告', '真的确定吗？', QMessageBox.Yes | QMessageBox.No,
                                           QMessageBox.Yes)
            if button2 == QMessageBox.Yes:
                Todo = leancloud.Object.extend('Test')
                query = Todo.query
                student_list = query.find()
                for i in student_list:
                    objectid = i._attributes.get('objectId')
                    todo = Todo.create_without_data(objectid)
                    todo.set('ID', 110)
                    todo.save()

    def refreshDesignation(self):
        button1 = QMessageBox.question(self, '提示', '是否确认提交修改，该操作不可撤销！', QMessageBox.Yes | QMessageBox.No,
                                       QMessageBox.Yes)
        if button1 == QMessageBox.Yes:
            button2 = QMessageBox.question(self, '警告', '真的确定吗？', QMessageBox.Yes | QMessageBox.No,
                                           QMessageBox.Yes)
            if button2 == QMessageBox.Yes:
                Todo = leancloud.Object.extend('Test')
                query = Todo.query
                student_list = query.find()
                for i in student_list:
                    objectid = i._attributes.get('objectId')
                    todo = Todo.create_without_data(objectid)
                    todo.set('ID', 110)
                    todo.save()
    # 添加一个退出的提示事件


class NewWidget(QWidget):
    def closeEvent(self, event):
        result = QtWidgets.QMessageBox.question(self, "Xpath Robot", "Do you want to exit?",
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if (result == QtWidgets.QMessageBox.Yes):
            event.accept()
        else:
            event.ignore()


import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    new = NewWidget()  # 重写的QWidget组件
    ui = mywindow()  # 正常用的窗口
    ui.setupUi(new)  # 一定要继承上
    new.show()
    sys.exit(app.exec_())
