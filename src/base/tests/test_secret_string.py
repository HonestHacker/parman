from ..secret_string import *

def test_hashed_string():
    password = 'blabla'
    hashed_password = SHA256String(password)
    print(hashed_password)
    assert password == hashed_password
    assert hashed_password.secret_value == 'ccadd99b16cd3d200c22d6db45d8b6630ef3d936767127347ec8a76ab992c2ea'

def test_twofish():
    password = 'qwerty'
    encrypted_password = TwoFishEncryptedString(password, 'blabla')
    print(encrypted_password)
    assert encrypted_password.get_decrypted_value('blabla') == 'qwerty'