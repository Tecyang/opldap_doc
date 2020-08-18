import sys
import os
import json


class GenerateUser:

    path = os.path.dirname(__file__) + '/userimport'

    def getFileList(self):
        files = os.listdir(self.path)
        # 生成用户的起始id
        uid_number = 2055
        for file in files:
            print(file)
            if file.find('txt') > 0:
                self.generateUser(file,uid_number)
                uid_number = uid_number+1

    def generateUser(self, file,uid_number=2000):

        with open(self.path + '/' + file) as f:
            j_context = json.loads(f.read())
            f.close()

        templatePath = self.path + '/userTemplate.ldif'
        with open(templatePath) as f:
            template = f.read()
            USER = template.replace("UID",j_context.get('登陆名')) \
                .replace("SN",j_context.get('姓')) \
                .replace("CN",j_context.get('名')) \
                .replace("GIVEN_NAME",j_context.get('名')) \
                .replace("DISP_NAME",j_context.get('姓') + j_context.get('名')) \
                .replace("MAIL",j_context.get('邮箱')) \
                .replace("PASSWORD",j_context.get('密码')) \
                .replace("NUMBER",str(uid_number))
            print(USER)
            f.close()

            user = self.path + '/user.ldif'
            with open(user, 'a+') as f:
                f.write('\n' + USER + '\n')
                f.close()


if __name__ == "__main__":
    generateUser = GenerateUser()
    generateUser.getFileList()