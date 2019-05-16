from django.core.mail import send_mail

from MarkBook.settings import EMAIL_HOST_USER


class SMS(object):
    def __init__(self, email, token):
        self.email = email
        self.token = token

    def send(self):
        msg = '''
            <p>您好，欢迎使用MarkBook，请在5分钟之内完成操作，否则验证失败</p>
            <p>点击下面下面激活即可完成注册，就可以开始使用啦。</p>
            <p><a href="http://127.0.0.1:8000/api/email_verify/?email={}&token={}">激活</a></p>
            <p>如果激活按钮没有生效，请复制一下链接到浏览器进行访问</p>
            <p>http://127.0.0.1:8000/api/email_verify/?email={}&token={}</p>
        '''.format(self.email, self.token, self.email, self.token)
        title = "MarkBook激活"
        body = "激活"
        try:
            send_mail(title, body, EMAIL_HOST_USER, [self.email], html_message=msg)
            return True
        except Exception as ex:
            print(ex)
            return False

    def send_edit(self):
        msg = '''
                   <p>您好，欢迎使用MarkBook，请在5分钟之内完成操作，否则验证失败</p>
                   <p>点击下面下面激活即可完成修改密码</p>
                   <p><a href="http://127.0.0.1:8000/api/edit_pwd/?email={}&token={}">验证</a></p>
                   <p>如果激活按钮没有生效，请复制一下链接到浏览器进行访问</p>
                   <p>http://127.0.0.1:8000/api/edit_pwd/?email={}&token={}</p>
               '''.format(self.email, self.token, self.email, self.token)
        title = "MarkBook修改密码"
        body = "修改密码"
        try:
            send_mail(title, body, EMAIL_HOST_USER, [self.email], html_message=msg)
            return True
        except Exception as ex:
            print(ex)
            return False


if __name__ == '__main__':
    sms = SMS("1299622716@qq.com")
    sms.send()
