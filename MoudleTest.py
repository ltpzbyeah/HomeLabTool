cursor = conn.cursor()
sql = "select * from user where name='%s'" % (nametext)
cursor.execute(sql)
data = cursor.fetchall()
objectID = data[0][1]
searchurl = 'https://p14yxpmt.lc-cn-e1-shared.com/1.1/classes/user/' + objectID
searchbody = {"sessionToken": "xxw5yzxpdvzhe8jgxp0eu7wa7"}
response = requests.get(searchurl, data=json.dumps(searchbody), headers=headers)
info = response.json()
ID = info['ID']
Name = info['Name']
Sex = info['Sex']
UserName = info['UserName']
Password = info['Password']
LoginDate = info['LoginDate']
Designation = info['Designation']
Stage = info['Stage']
Class1 = info['Class1']
Class2 = info['Class2']
Class3 = info['Class3']
Class4 = info['Class4']
Class5 = info['Class5']
Class6 = info['Class6']
Age = info['Age']
Exp = info['Exp']
Level = info['Level']
Gold = info['Gold']
StoryCheckpoint1 = info['StoryCheckpoint1']
StoryCheckpoint2 = info['StoryCheckpoint2']
StoryCheckpoint3 = info['StoryCheckpoint3']
StoryCheckpoint4 = info['StoryCheckpoint4']
StoryTaskFinish = info['StoryTaskFinish']
ChallengeTaskFinish = info['ChallengeTaskFinish']
BountyTaskFinish = info['BountyTaskFinish']
StoryTaskPublish = info['StoryTaskPublish']
ChallengeTaskPublish = info['ChallengeTaskPublish']
BountyTaskPublish = info['BountyTaskPublish']
StoryTaskReceived = info['StoryTaskReceived']
ChallengeTaskReceived = info['ChallengeTaskReceived']
BountyTaskReceived = info['BountyTaskReceived']
Year = info['Year']
