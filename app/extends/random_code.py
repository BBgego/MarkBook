import hashlib
import random


# 获取验证码
def get_random_code():
    return str(random.randint(1000, 9999))


# md5加密
def md5_code(code):
    md = hashlib.md5()
    md.update(code.encode())
    return md.hexdigest()


# if __name__ == '__main__':
#     code = get_random_code()
#     print(code)
#     m_code = md5_code(code)
#     print(m_code)
