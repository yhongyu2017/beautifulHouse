import hashlib


def md5(pwd):
    '''
    字符串加密
    :param pwd:
    :return:
    :creator:
    '''
    m = hashlib.md5()
    m.update(pwd.encode('utf8'))
    return m.hexdigest()