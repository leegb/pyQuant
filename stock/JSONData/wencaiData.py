# -*- coding:utf8 -*-
"""
交易数据接口
Created on 2014/07/31
@author: Jimmy Liu
@group : waditu
@contact: jimmysoa@sina.cn
"""
from __future__ import division

import json
import math
import re
import sys
import time

import pandas as pd
sys.path.append("..")
# import JohhnsonUtil.johnson_cons as ct
from JohhnsonUtil import LoggerFactory
from JohhnsonUtil import commonTips as cct
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

log=LoggerFactory.getLogger('wencaiData')


def post_login(root='http://upass.10jqka.com.cn/login'):
    postData = {
    'act':"login_submit",
    'isiframe':"1",
    'view':"iwc_quick",
    'rsa_version':"default_2",
    'redir':"http://www.iwencai.com/user/pop-logined",
    'uname':"OuY03m5D1ojuPmpTAbgkpcm0dod5fMbU8jVOwd17WCPEW0pz52RyEcXU+2ZLiBmP+5jckGeUR5ba/fDjkUaPVaisn9Je4l7+JPv3iX/VS4erW25ueJEoVszK9kM3oF2mT3lraObawMclBteFcfwWHyWhsW7YmN19cgOdsQWWWno=",
    'passwd':"IVORnBZ0Pdi+ix+ehVqiCdYTWCkGBy/kYEeTyTmi+5QBiL8SvYZZg3LLVzzfeMbOWaR/rK4Aoc80kSpqCIETfN3EmhA1CKK9ukI0TImlm8ASlqqz/lUq0lm5LwuMRdBjcD3hoP4RnvDc+W2+ng4XA31YsG6pBo+YF5IHcIxaScU=",
    'captchaCode':"",
    'longLogin':"on",
    }

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Connection': 'keep-alive'}
    from cookielib import CookieJar
    cj = CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    data_encoded = urllib.urlencode(postData)
    url = 'http://www.iwencai.com/stockpick/search?typed=0&preParams=&ts=1&f=1&qs=result_original&selfsectsn=&querytype=&searchfilter=&tid=stockpick&w=%s'
    url = url%('国企改革')
    for ck in cj:
        print ck
    print ":"
    try:
        response = opener.open(root,data_encoded)
        content = response.read()
        # count = re.findall('\[[A-Za-z].*\]', data, re.S)
        status = response.getcode()
        # print content
        for ck in cj:
            print ck
        print ":"
        # cj["session"]["u_name_wc"] = "mx_149958484"
        if status == 200:
            response = opener.open(url)
            page =  response.read()
            print page
            for ck in cj:
                print ck
    except  urllib2.HTTPError, e:
         print e.code
    # f= response.read().decode("utf8")
    # outfile =open("rel_ip.txt","w")
    # print >> outfile , "%s"   % ( f)
    #打印响应的信息
    # info = response.info()
    # print info
    # get_wencai_Market_url(url=None)

global null
null = None
def get_wencai_Market_url(filter='国企改革',perpage=1,url=None,):
    urllist = []
    global null
    df = pd.DataFrame()
    if url == None:
        time_s = time.time()
        wencairoot = 'http://www.iwencai.com/stockpick/search?typed=0&preParams=&ts=1&f=1&qs=result_original&selfsectsn=&querytype=&searchfilter=&tid=stockpick&w=%s'
        url = wencairoot%(filter)
        log.info("url:%s"%(url))
        # url = ct.get_url_data_R % (market)
        # print url
        cache_root="http://www.iwencai.com/stockpick/cache?token=%s&p=1&perpage=%s&showType="
        cache_ends = "[%22%22,%22%22,%22onTable%22,%22onTable%22,%22onTable%22,%22onTable%22,%22onTable%22,%22onTable%22,%22onTable%22,%22onTable%22]"
        data = cct.get_url_data(url)
        # print data
        # count = re.findall('(\d+)', data, re.S)
        # "token":"dcf3d42bbeeb32718a243a19a616c217"
        # log.info("data:%s"%(data.decode('unicode-escape')))
        # log.info("data:%s"%(data))
        # count = re.findall('token":"([\D\d].*)"', data, re.S)
        count = re.findall('token":"([\D\d]+?)"', data, re.S)
        codelist = []
        grep_stock_codes = re.compile('"(\d{6})\.S')
        # response = requests.get(all_stock_codes_url)
        # stock_codes = grep_stock_codes.findall(response.text)
        # print data
        log.info( time.time()-time_s)
        # print count
        if len(count) == 1:
            cacheurl = cache_root % (count[0],perpage)
            cacheurl =  cacheurl + cache_ends
            log.info( cacheurl)
            time_s = time.time()
            html = cct.get_url_data(cacheurl)
            # count = re.findall('"(\d{6})\.S', data, re.S)
            # count = re.findall('result":(\[[\D\d]+\]),"oriColPos', data, re.S)
            # count = re.findall('result":(\[[\D\d]+\]),"oriIndexID', data, re.S)
#            html = data.decode('unicode-escape')
#            html = data.decode('unicode-escape')
            count = re.findall('(\[\["[0-9]{6}\.S[HZ][\D\d]+\]\]),"oriIndexID', html, re.S)
            # count = grep_stock_codes.findall(data,re.S)
            log.info("count:%s len:%s"%(count,len(count)))
            # print html

            log.info( time.time()-time_s)
            if len(count) > 0:
                # import ast
                # result = eval(count[0].replace('null','None'))
                result = eval(count[0])
                # result = ast.literal_eval(count[0])
                # import json
                # obj = json.loads(data)
                # print "obj:",obj
                # print result,len(result)
                # print result[1]
                urllist = []
                dlist = []
                key_t=[]
                for xcode in result:
                    # print xcode
                    code_t =[]
                    for x in xcode:
                        # print x
                        if isinstance(x, list):
                            # print "list:",x
                            key_t=[]
                            for y in x:
                                if isinstance(y, dict):
                                    # pass
                                    keylist=['URL','PageRawTitle']
                                    for key in y.keys():
                                        if key in keylist:
                                            if key == 'URL':
                                                urls = str(y[key]).replace('\\','').strip().decode('unicode-escape')
                                                if urls[-20] not in urllist:
                                                    urllist.append(urls[-20])
                                                    log.info( urls),
#                                                    log.info( urls)
                                                else:
                                                    break
                                            else:
                                                urls = str(y[key]).decode('unicode-escape')
                                                key_t.append(urls)
#                                                key_t.append(urls)
                                                log.info( urls),
                                # else:
                                    # print str(y).decode('unicode-escape'),
                        else:
                            code_t.append(str(x).decode('unicode-escape'))
#                            code_t.append(str(x))
                            log.info(str(x).decode('unicode-escape')),
#                            log.info(str(x)),
#                    log.info( key_t)
                    if len(code_t) > 4:
                        code = code_t[0]
                        name = code_t[1]
                        trade = code_t[2]
                        trade = '0' if trade == '--' else trade
                        percent = code_t[3]
                        percent = '0' if percent == '--' else percent

                        # index = code_t[4]
                        index = ";".join(x for x in code_t[4].split(';')[:3])
                        index = index[:20] if len(index) > 20 else index
                        if len(key_t) > 0:
                            # print key_t[0]
                            title1 = key_t[0]
                            if len(key_t) > 1:
                                title2 = key_t[1]
                            else:
                                title2 = None
                            dlist.append({'code': code, 'name': name, 'trade': trade, 'percent': percent, 'index': index, 'tilte1': title1,'tilte2': title2})
                        else:
                            dlist.append({'code': code, 'name': name, 'trade': trade, 'percent': percent, 'index': index})
                    # print ''
                # df = pd.DataFrame(dt_list, columns=ct.TDX_Day_columns)
                # df = pd.DataFrame(dlist, columns=['index','code','name','trade','percent','tilte1','tilte2'])
                if len(dlist) > 0 and 'tilte1' in (dlist[0].keys()) :
                    df = pd.DataFrame(dlist, columns=['code','name','trade','percent','index','tilte1','tilte2'])
                else:
                    df = pd.DataFrame(dlist, columns=['code','name','trade','percent','index'])
                df['code'] = (map(lambda x: x[:6],df['code']))
                df = df.set_index('code')
            # print type(count[0])
            # print type(list(count[0]))
            # print count[0].decode('unicode-escape')
    return df

def get_codelist_df(codelist):
    wcdf = pd.DataFrame()
    time_s = time.time()
    if len(codelist)>30:
        # num=int(len(codeList)/cpu_count())
        div_list = cct.get_div_list(codelist, int(len(codelist)/30+1))
        # print "ti:",time.time()-time_s
#        cnamelist =[]
        for li in div_list:
            cname = ",".join(x for x in li)
#            cnamelist.append(cname)
            wcdf_t = get_wencai_Market_url(cname,len(li))
            wcdf = wcdf.append(wcdf_t)
#        results = cct.to_mp_run_async(get_wencai_Market_url, cnamelist,30)
#        for res in results:
#            wcdf = wcdf.append(res)
        print ("w:%.2f"%(time.time()-time_s)),
        # print results
    else:
        cname = ",".join(x for x in codelist)
        wcdf = get_wencai_Market_url(cname,len(codelist))
#        wcdf = wcdf.append(wcdf_t)
    if len(wcdf) != len(codelist):
        log.warn("wcdf:%s"%(len(wcdf)))
    return wcdf
if __name__ == '__main__':
    # df = get_sina_all_json_dd('0', '3')
    # df=get_sina_Market_json('cyb')
    # _get_sina_json_dd_url()
    # print sina_json_Big_Count()
    # print getconfigBigCount(write=True)
    # sys.exit(0)
    # post_login()
#    log.setLevel(LoggerFactory.INFO)
#    df = get_wencai_Market_url(filter='国企改革',perpage=1000)
#    df = get_wencai_Market_url('湖南发展,天龙集团,浙报传媒,中珠医疗,多喜爱',500)
    df = get_wencai_Market_url('湖南发展',500)
    # df = get_codelist_df(['天龙集团','太阳电缆','杭州解百'])
    # df = get_codelist_df([u'\u7ef4\u5b8f\u80a1\u4efd', u'\u6d77\u987a\u65b0\u6750', u'\u6da6\u6b23\u79d1\u6280', u'\u84dd\u6d77\u534e\u817e', u'\u5149\u529b\u79d1\u6280'])
    df = df.sort_values(by='percent',ascending=[0])
    print df[:10],len(df)
    # get_wencai_Market_url()
    sys.exit()