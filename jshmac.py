from hashlib import sha256
import hmac


def get_sha256(data):
    key = 'dc272cc640584c3eb611593bc96829c1'
    key = key.encode('utf-8')  # sha256加密的key
    message = data.encode('utf-8')  # 待sha256加密的内容
    sign = hmac.new(key, message, digestmod=sha256).digest().hex()
    return sign


