#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/7/19 下午3:55
@Author  : Bill Fang
@File    : ExcelDeal.py
@Desc    : 
"""
import Crypto.Util.number
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Cipher import AES
import base64
import os
import sys


def rsa_private_key_decrypt(cipher_text, rsa_private_key):
    private_key = RSA.importKey(base64.b64decode(rsa_private_key))
    cipher = Cipher_pkcs1_v1_5.new(private_key)

    block_size = int(Crypto.Util.number.size(private_key.n) / 8)
    cipher_text_bytes = base64.b64decode(cipher_text)
    length = len(cipher_text_bytes)
    offset = 0
    res = []

    while length - offset > 0:
        if length - offset > block_size:
            res.append(cipher.decrypt(cipher_text_bytes[offset: offset + block_size], "ERROR"))
        else:
            res.append(cipher.decrypt(cipher_text_bytes[offset:], "ERROR"))
        offset += block_size

    plaintext = b''.join(res)
    return plaintext.decode(encoding_utf8)


if __name__ == '__main__':
    sign = 'Arae2mo8iKzdILicBVKHpALkQ4ovozW6hNg+Xd9J/Er4HdQ9ilts3YuolZn4OV/JDCDDpF2ps16r9a2GbagzehSiKyDnEBtpYwLXpf6Y5vTKuj3fSSzwdGGemGZolhqQVsVV92V8CioG4Tut64nE/sC/51iCJnZaY+Wnnop7pQAPeHgR3KxJZldg/mrL3AfHQS1jiHxKuSybdZgSqIpae/QaQ4lqVZp4M1lEbyMCiUEhNUlTZIbc+NYYJvtecvaCsSTSl20fGSK9XVwwWcuToJXN3Ca8BUlXiRofc3MzLyDqSz57HKSWp5BYbaz/q06NVQbmPKxWqigFWG23CPi9GQ=='
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = gmpy2.invert(e, phi)

    decrypt(d, n, sign)
