import base64


def encrypt_data(data):
    token = base64.urlsafe_b64encode(data.encode())
    return token.decode('ascii')


def decrypt_data(token):
    data = base64.urlsafe_b64decode(token)
    return data.decode('ascii')
