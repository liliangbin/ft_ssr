import base64
import json
import requests

wrong_password = 'abababababa'


# base64 解码 需要是4的倍数
def base64decode(s):
    # transtab = str.maketrans('-_', '+/')
    # s = s.translate(transtab)
    if len(s) % 4 != 0:
        s = s + (4 - len(s) % 4) * '='
    return base64.urlsafe_b64decode(s.encode())


def decode_ss(ss):
    code_base64 = ss[5:ss.find('@')]
    method_pwd = base64decode(code_base64)
    method_b, pwd_b = method_pwd.split(b':', 1)
    server = ss[ss.find('@') + 1:ss.rfind(':')]
    if ss.find('#') == -1:
        port = ss[ss.rfind(':') + 1:]
    else:
        port = ss[ss.rfind(':') + 1:ss.find('#')]
    ss_conf = {'server': server, 'server_port': int(port),
               'password': pwd_b.decode(), 'method': method_b.decode()}
    print(json.dumps(ss_conf, indent=4))

    pwd_base64 = base64.urlsafe_b64encode(pwd_b)

    ssr = [server, port, 'origin', method_b.decode(), 'plain',
           pwd_base64.decode()]
    ssrlink = ':'.join(ssr) + '/?obfsparam=&protoparam=&remarks='
    ssrlink_base64 = base64.urlsafe_b64encode(ssrlink.encode())
    ssrlink_output = 'ssr://' + ssrlink_base64.decode()
    print(ssrlink_output)


# ssr 修改组名和备注
def decode_ssr(ssr, group='', remarks='', out_date=False):
    base_connection_url = base64decode(ssr[6:])
    server, server_port, protocol, method, obfs, other = base_connection_url.decode().split(':')
    password_base64, param_base64 = other.split("/?")
    password = base64decode(password_base64)
    params = param_base64.split("&")

    key = {}
    for param in params:
        k, v = param.split("=", 1)
        if v:
            key[k] = v
    obfsparam_base64 = key.get('obfsparam')
    protoparam_base64 = key.get('protoparam')
    if obfsparam_base64:
        obfsparam = base64decode(obfsparam_base64)
    if protoparam_base64:
        protoparam = base64decode(protoparam_base64)
    if out_date:
        password_base64 = base64.b64encode(wrong_password.encode()).decode()
    ssr = [server, server_port, protocol, method, obfs, password_base64]

    remarks_base64 = str(base64.b64encode(remarks.encode('utf-8')), "utf-8")
    group_base64 = str(base64.b64encode(group.encode('utf-8')), "utf-8")
    ssrlink = ':'.join(ssr) + '/?obfsparam={}&protoparam={}&remarks={}&group={}'.format(obfsparam_base64,
                                                                                        protoparam_base64,
                                                                                        remarks_base64, group_base64)
    ssrlink_base64 = base64.urlsafe_b64encode(ssrlink.encode())
    ssrlink_output = 'ssr://' + ssrlink_base64.decode()
    return ssrlink_output


def main():
    s = 'ssr://aGs0LnN1Yndsa2oubGluazo3MDg1OmF1dGhfYWVzMTI4X21kNTpjaGFjaGEyMC1pZXRmOnRsczEuMl90aWNrZXRfYXV0aDpZMlZXUm5wb2VqUS8_b2Jmc3BhcmFtPVpHbHpZM1Z6YzJsdmJuTXVZWEJ3YkdVdVkyOXQmcHJvdG9wYXJhbT1NVGMwTlRZNlozRjZiVGhTZFhKYVRXUjVibEZRUjNOTlMwdG1SMmxyVjBSMFRWUk9WbTAmcmVtYXJrcz01WW1wNUwyWjVyV0I2WWVQNzd5YU1qZzVMalJIUWcmZ3JvdXA9VTNCbFpXVG52WkhudTV6bnA1SG1pb0EmdWRwcG9ydD0wJnVvdD0w'
    is_ss = s.find('ss://')
    is_ssr = s.find('ssr://')
    if is_ss != -1:
        ss = s[is_ss:].strip()
        decode_ss(ss)
    elif is_ssr != -1:
        ssr = s[is_ssr:].strip()
        decode_ssr(ssr)
    else:
        print('链接格式不正确！')


# 来自url的base64 代码 直接放到这个地方来 转化为对应我们修改的数据
def base64_to_ssrs(base64_str=''):
    result_ssrs = base64decode(base64_str)
    ssrs = result_ssrs.decode().split('\n')
    result = []
    for i in ssrs:
        res = decode_ssr(i, '测试备注', '测试组')
        result.append(res)
    fsd = '\n'.join(result)

    return base64.b64encode(fsd.encode()).decode().strip()


def curl_server(server_url=''):
    response = requests.get(server_url)
    text = response.text
    code = response.status_code
    assert code == 200, print(response.text)
    return text.strip()


if __name__ == '__main__':
    result = curl_server('http://localhost:5000/')
    print(result)
    res = base64_to_ssrs(result)
    print(res)
    password_base64 = base64.b64encode(wrong_password.encode())
    print(password_base64)
