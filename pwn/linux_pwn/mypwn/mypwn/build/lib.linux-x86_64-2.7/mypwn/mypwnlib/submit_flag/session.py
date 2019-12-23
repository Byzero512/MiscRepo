import requests
from .cookies import *


class sessionCreFalse(Exception):
    pass

class urlNotDefine(Exception):
    pass

class urlNoCookies(Exception):
    pass

class urlNoHeaders(Exception):
    pass

class sessionPost(Exception):
    pass

class GetReqError(Exception):
    pass


class session():
    class_cookies=0
    class_headers={}
    class_url1=''
    class_url2=''
    class_session=requests.session()

    def __init__(self,url='',cookies=0,headers={}):

        try:
            if url and cookies and headers:
                ret_obj=class_session.get(url,cookies=cookies,headers=headers)
            elif url and cookies and not headers:
                ret_obj=class_session.get(url,cookies=cookies)
            else:
                ret_obj=0
            if ret_obj!=0:
                if(ret_obj.status_code!=200):
                    raise sessionCreFalse('\n\nsession not create successfully\n\n')
                self.set_url1(url)
                self.set_cookies(ret_obj.cookies)
                self.set_headers(headers)           

        except sessionCreFalse as except0:
            print(except0)
            quit()

    def set_cookies(self,arg_cookies):
        self.class_cookies=cookies.all2jar(arg_cookies)
    def set_headers(self,headers):
        self.class_headers=headers
    def set_url1(self,url):
        self.class_url1=url
    def set_url2(self,url):
        self.class_url2=url

    def sessionCre(self,url='',cookies=0,headers={}):
            try:
                if url:
                    self.set_url1(url)
                if cookies:
                    self.set_cookies(cookies)
                if headers:
                    self.set_headers(headers)
                if not self.class_url1:
                    raise urlNotDefine('\n\nnot set request url\n\n')
                if not self.class_cookies:
                    raise urlNoCookies('\n\nnot set requests cookies\n\n')
            except urlNotDefine as except1:
                print(except1)
                quit()
            except urlNoCookies as except2:
                print(except2)
                quit()

            try:
                if self.class_headers:
                    ret_obj=class_session.get(self.class_url1,cookies=self.class_cookies,headers=self.class_headers)
                elif not self.class_headers:
                    ret_obj=class_session.get(self.class_url,cookies=self.class_cookies)
                else:
                    raise sessionCreFalse('\n\nnot set url, cookies, headers\n\n')
                if(ret_obj.status_code!=200):
                    raise sessionCreFalse('\n\nsession not create successfully\n\n')
                self.set_cookies(ret_obj.cookies)            
                return ret_obj                    

            except sessionCreFalse as except0:
                print(except0)
                quit()
                          
        

    def post(self,url='',cookies={},data={},headers={}):
        try:
            if url:
                self.set_url2(url)
            if cookies:
                self.set_cookies(cookies)
            if headers:
                self.set_headers(headers)
            if not self.class_url2:
                raise urlNotDefine('\n\nnot set request obj\n\n')
            if not self.class_cookies:
                raise urlNoCookies('\n\nnot set requests cookies\n\n')
            if not self.class_headers:
                raise urlNoHeaders('\n\nnot set requests headers\n\n')
        except urlNotDefine as except1:
            print(except1)
            quit()
        except urlNoCookies as except2:
            print(except2)
            quit()
        except urlNoHeaders as except3:
            print(except3)
            quit()
        try:
            ret_obj=class_session.request.post(self.class_url2,cookies=self.class_cookies,headers=self.class_headers,data=data)
            if ret_obj.status_code!=200:
                raise sessionPost('\n\nsession post request error\n\n')
            self.set_cookies(ret_obj.cookies)
            return ret_obj
        except sessionPost as except4:
            print(except4)
            quit()


    def get(url='',cookies=0,headers={},params={}):
        try:
            if url:
                self.set_url2(url)
            if cookies:
                self.set_cookies(cookies)
            if headers:
                self.set_headers(headers)
            if (not self.class_url2):
                raise urlNotDefine('\n\nnot set request obj\n\n')
            if (not self.class_cookies):
                raise urlNoCookies('\n\nnot set requests cookies\n\n')
            if (not self.class_headers):
                raise urlNoHeaders('\n\nnot set requests headers\n\n')
        except urlNotDefine as except1:
            print(except1)
            quit()
        except urlNoCookies as except2:
            print(except2)
            quit()
        except urlNoHeaders as except3:
            print(except3)
            quit()
        try:
            ret_obj=class_session.request.get(self.class_url2,cookies=self.class_cookies,headers=self.class_headers,params=params)
            if ret_obj.status_code!=200:
                raise GetReqError('\n\nsession get request error\n\n')
            self.set_cookies(ret_obj.cookies)
            return ret_obj

        except GetReqError as except4:
            print(except4)
            quit()
