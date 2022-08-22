import hashlib,json
public_key = 'ylyh!@#'
public_key_Patient = 'ylhz#!@'

def get_sign_md5(data_str):
    new_data_str = data_str + public_key
    m = hashlib.md5()   #实例化md5对象
    m.update(new_data_str.encode(encoding='utf-8'))  ##把字符串转成bytes类型,加密
    return m.hexdigest()

def get_mobile_md5(mobile_str):
    hl = hashlib.md5()
    hl.update(mobile_str.encode(encoding='utf-8'))
    return hl.hexdigest()

def get_signPatient_md5(str):
    new_str = str + public_key_Patient
    m = hashlib.md5()   #实例化md5对象
    m.update(new_str.encode(encoding='utf-8'))  ##把字符串转成bytes类型,加密
    return m.hexdigest()