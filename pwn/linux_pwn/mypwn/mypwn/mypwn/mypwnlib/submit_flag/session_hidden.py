import requests
from .cookies import *

session=requests.session()

session_url1=''
session_url2=''
session_headers={
}
sessoin_cookies=0

def sessoin_request(url='',headers={},data={},params={},cookies=0):
    try:
        if (data and params) or ((not data) and (not params) ) :
            raise ArgumentError('\n\nnot know the request is get or post!\n\n')
        # the func not set cookies, use global cookies        
        if not cookies:
            if sessoin_cookies:
                if data:
                    if header:
                        return sessoin.post(url,cookies=sessoin_cookies,headers=headers,data=data)
                    else:
                        return sessoin.post(url,cookies=sessoin_cookies,data=data)

                elif params:
                    if header:
                        return sessoin.get(url,cookies=sessoin_cookies,headers=headers,params=params)
                    else:
                        return sessoin.get(url,cookies=sessoin_cookies,params=params)
            else:
                if data:
                    if header:
                        return sessoin.post(url,headers=headers,data=data)
                    else:
                        return sessoin.post(url,data=data)
                elif params:
                    if header:
                        return sessoin.get(url,headers=headers,params=params)
                    else:
                        return sessoin.get(url,params=params)
            raise RequestTypeError("\n\nthe request is not get and post!\n\n")
        # the func set cookies, use argument cookies
        else:
            if data:
                if header:
                    return sessoin.post(url,cookies=cookies,headers=headers,data=data)
                else:
                    return sessoin.post(url,cookies=cookies,data=data)
            elif params:
                if header:
                    return sessoin.get(url,cookies=cookies,headers=headers,params=params)
                else:
                    return sessoin.get(url,cookies=cookies,params=params)
            raise RequestTypeError("\n\nthe request is not get and post!\n\n")
                
    except ArgumentError as except1:
        print(except1)
        exit()
    except RequestTypeError as except2:
        print(except2)
        exit()
def session_cre(url,cookies,headers={},data={},params={}):
    session_url1=url
    sessoin_cookies=cookies.all2jar(cookies)
    if headers:
        session_headers=headers
    return sessoin_request(url=url,cookies=cookies,headers=headers,data={},params=params)

def sessoin_set_headers(arg_headers):
    session_headers=arg_headers

def sessoin_set_cookies(arg_cookies):
    sessoin_cookies=cookies.all2jar(arg_cookies)

def session_set_url2(url2):
    session_url2=url2

def session_submit_flag(url2='',headers={},data={},params={},cookies=0):
    if url2 and (url2!=session_url2):
        session_url2=url2
    sessoin_request(url=session_url2,headers=headers,data=data,params=params,cookies=cookies)
