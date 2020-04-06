# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 15:35:04 2020

@author: carlo
"""

import requests
import hashlib
import sys


def request_api_data(query_char):
    url='https://api.pwnedpasswords.com/range/' + query_char
    res= requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(
            f'Error fetching:{res.status_code}, check the api e try again'
            )
    return res
 
    
def get_password_leaks_count(hashes,hash_to_check):
    hashes=(line.split(':') for line in hashes.text.splitlines())
    for h,count in hashes:
        if h == hash_to_check:
            return count
    return 0

def pwned_api_check(password):
    #Check password if exists in API response
    shai1password= hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char,tail=shai1password[:5],shai1password[5:]
    response=request_api_data(first5_char)
    return get_password_leaks_count(response,tail)


def check(args):
   for password in args:
       count= pwned_api_check(password)
       if count:
           print(f'{password} was {count} times...you should probably change your password')
       else:
          print(f'{password} was not found.Carry on')
       
   return 'done!'
    

if __name__=='__main__':
     print(check(sys.argv[1:]))