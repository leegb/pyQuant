# -*- coding:utf-8 -*-
# !/usr/bin/env python


# import sys
#
# reload(sys)
#
# sys.setdefaultencoding('utf-8')
# url_s = "http://vip.stock.finance.sina.com.cn/quotes_service/view/cn_bill_all.php?num=100&page=1&sort=ticktime&asc=0&volume=0&type=1"
# url_b = "http://vip.stock.finance.sina.com.cn/quotes_service/view/cn_bill_all.php?num=100&page=1&sort=ticktime&asc=0&volume=100000&type=0"
# status_dict = {u"中性盘": "normal", u"买盘": "up", u"卖盘": "down"}
# url_real_sina = "http://finance.sina.com.cn/realstock/"
# url_real_sina_top = "http://vip.stock.finance.sina.com.cn/mkt/#stock_sh_up"
# url_real_east = "http://quote.eastmoney.com/sz000004.html"
from bs4 import BeautifulSoup
import urllib2
from pandas import Series, DataFrame
import re
import johnson_cons as ct
import time
import singleAnalyseUtil as sl
import realdatajson as rl
import pandas as pd
import traceback
import sys
# import numpy as np
import tdx_data_Day as tdd
from LoggerFactory import *

# from logbook import Logger,StreamHandler,SyslogHandler
# from logbook import StderrHandler


def downloadpage(url):
    fp = urllib2.urlopen(url)
    data = fp.read()
    fp.close()
    return data


def parsehtml(data):
    soup = BeautifulSoup(data)
    for x in soup.findAll('a'):
        print x.attrs['href']


def html_clean_content(soup):
    [script.extract() for script in soup.findAll('script')]
    [style.extract() for style in soup.findAll('style')]
    soup.prettify()
    reg1 = re.compile("<[^>]*>")  # 剔除空行空格
    content = reg1.sub('', soup.prettify())
    print content


def get_sina_url(vol='0', type='0', pageCount='100'):
    # if len(pageCount) >=1:
    url = ct.SINA_DD_VRatio_All % (
        ct.P_TYPE['http'], ct.DOMAINS['vsf'], ct.PAGES['sinadd_all'], pageCount, ct.DD_VOL_List[vol], type)
    # print url
    return url


def get_sina_all_dd(vol='0', type='0', retry_count=3, pause=0.001):
    if len(vol) != 1 or len(type) != 1:
        return None
    else:
        print ("Vol:%s  Type:%s" % (ct.DD_VOL_List[vol], ct.DD_TYPE_List[type]))
    # symbol = _code_to_symbol(code)
    for _ in range(retry_count):
        time.sleep(pause)
        try:
            ct._write_console()
            url = get_sina_url(vol, type)
            # url= ct.SINA_DD_VRatio % (ct.P_TYPE['http'], ct.DOMAINS['vsf'], ct.PAGES['sinadd_all'],ct.DD_VOL_List[vol], ct.DD_TYPE_List[type])
            page = urllib2.urlopen(url)
            html_doc = page.read()
            # print (html_doc)
            # soup = BeautifulSoup(html_doc,fromEncoding='gb18030')
            # print html_doc
            pageCount = re.findall('fillCount\"\]\((\d+)', html_doc, re.S)
            if len(pageCount) > 0:
                start_t = time.time()
                pageCount = pageCount[0]
                if int(pageCount) > 100:
                    if int(pageCount) > 10000:
                        print "BigBig:", pageCount
                        pageCount = '10000'

                    print "AllBig:", pageCount
                    html_doc = urllib2.urlopen(get_sina_url(vol, type, pageCount=pageCount)).read()
                    print (time.time() - start_t)

            soup = BeautifulSoup(html_doc, "lxml")
            print (time.time() - start_t)
            # abc= (soup.find_all('script',type="text/javascript"))
            # print(len(abc))
            # print (abc[4].text).strip().find('window["fillCount"]')
            # print abc[4].contents


            # pageCount= soup.find_all(string=re.compile('fillCount\"\]\((\d+)'))
            # pageCount=re.findall('(\d+)',pageCount[0])

            # sys.exit(0)
            # print soup.find_all('__stringHtmlPages')

            # sys.exit(0)

            # soup = BeautifulSoup(html_doc.decode('gb2312','ignore'))
            # print soup.find_all('div', id="divListTemplate")
            # for i in soup.find_all('tr',attrs={"class": "gray"."class":""}):
            alldata = {}
            dict_data = {}
            # print soup.find_all('div',id='divListTemplate')

            row = soup.find_all('div', id='divListTemplate')
            sdata = []
            if len(row) >= 1:
                '''
                colums:CHN name

                '''
                # firstCells = row[0].find('tr')
                # th_cells = firstCells.find_all('th')
                # td_cells = firstCells.find_all('td')
                # m_name=th_cells[0].find(text=True)
                # m_code=th_cells[1].find(text=True)
                # m_time=th_cells[2].find(text=True)
                # m_status=th_cells[3].find(text=True)
                # m_detail=th_cells[4].find(text=True)
                # m_price=td_cells[0].find(text=True)
                # m_vol=td_cells[1].find(text=True)
                # m_pre_p=td_cells[2].find(text=True)
                # print "m_name:",m_name,m_pre_p
                for tag in row[0].find_all('tr', attrs={"class": True}):
                    # print tag
                    th_cells = tag.find_all('th')
                    td_cells = tag.find_all('td')
                    m_name = th_cells[0].find(text=True)
                    m_code = th_cells[1].find(text=True)
                    m_time = th_cells[2].find(text=True)
                    # m_detail=(th_cells[4]).find('a')["href"]   #detail_url
                    m_price = td_cells[0].find(text=True)
                    m_vol = float(td_cells[1].find(text=True).replace(',', '')) * 100
                    m_pre_p = td_cells[2].find(text=True)
                    m_status_t = th_cells[3].find(text=True)
                    if m_status_t in status_dict.keys():
                        m_status = status_dict[m_status_t]
                        # print m_status
                    sdata.append({'code': m_code, 'time': m_time, 'vol': m_vol, 'price': m_price, 'pre_p': m_pre_p,
                                  'status': m_status, 'name': m_name})
                    # sdata.append({'code':m_code,'time':m_time,'vol':m_vol,'price':m_price,'pre_p':m_pre_p,'detail':m_detail,'status':m_status,'name':m_name})
                    # print sdata
                    # print m_name
                    # break
            # pd = DataFrame(sdata,columns=['code','time','vol','price','pre_p','detail','status','name'])
            df = DataFrame(sdata, columns=['code', 'time', 'vol', 'price', 'pre_p', 'status', 'name'])
            # for row in soup.find_all('tr',attrs={"class":"gray","class":""}):
        except Exception as e:
            print "Except:", (e)
        else:
            return df
        raise IOError(ct.NETWORK_URL_ERROR_MSG)

def log_format(record, handler):
    handler = StderrHandler()
    # handler.format_string = '{record.channel}: {record.message}'
    handler.format_string = '{record.channel}: {record.message) [{record.extra[cwd]}]'
    return record.message

from logbook import FileHandler
log_handler = FileHandler('application.log')
log_handler.push_application()

if __name__ == "__main__":
    # parsehtml(downloadpage(url_s))
    # StreamHandler(sys.stdout).push_application()
    log=getLogger('SinaMarket')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    # handler=StderrHandler(format_string='{record.channel}: {record.message) [{record.extra[cwd]}]')
    # log.level=log.debug
    # error_handler = SyslogHandler('Sina-M-Log', level='ERROR')
    status = False
    vol = '0'
    type = '2'
    # cut_num=10000
    success = 0
    top_all = pd.DataFrame()
    time_s = time.time()
    delay_time = 1800
    base_path=r"E:\DOC\Parallels\WinTools\zd_pazq\T0002\blocknew\\"
    block_path=base_path+'063.blk'
    all_diffpath=base_path+'062.blk'
    while 1:
        try:
            df = rl.get_sina_Market_json('all')
            top_now = rl.get_market_price_sina_dd_realTime(df, vol, type)
            time_Rt = time.time()
            if len(top_now) > 10 and not top_now[:1].buy.values==0:
                time_d = time.time()
                #     top_now=top_now[top_now['percent']>=0]
                if len(top_all) == 0:
                    top_all = top_now
                    # top_all['llow'] = 0
                    # top_all['lastp'] = 0
                    top_all=top_all[top_all.buy>0]
                    codelist = top_all.index.tolist()
                    log.info('toTDXlist:%s'%len(codelist))
                    data=tdd.get_tdx_all_day_LastDF(codelist)
                    log.info("TdxLastP: %s %s"%(len(data),data.columns.values))
                    data.rename(columns={'low':'llow'}, inplace=True)
                    data.rename(columns={'high':'lhigh'}, inplace=True)
                    data.rename(columns={'close':'lastp'}, inplace=True)
                    data.rename(columns={'vol':'lvol'}, inplace=True)
                    data=data.loc[:,['llow','lhigh','lastp','lvol','date']]
                    # data.drop('amount',axis=0,inplace=True)
                    log.info("TDX Col:%s"%data.columns.values)
                    # df_now=top_all.merge(data,on='code',how='left')
                    # df_now=pd.merge(top_all,data,left_index=True,right_index=True,how='left')
                    top_all=top_all.merge(data,left_index=True,right_index=True,how='left')
                    log.info('Top-merge_now:%s'%(top_all[:1]))
                    # import sys
                    # sys.exit(0)
                    # # top_all['llow'] = 0
                    # top_all['lastp'] = 0
                    # codelist = top_all.index.tolist()
                    # # print type(codelist)
                    # lastp_d = rl.get_market_LastPrice_sina_js(codelist)
                    # # lp_dict={}
                    # # print repr(lastp_d)s
                    # i = 0
                    # for w_dict in lastp_d:
                    #     for code in w_dict:
                    #         i += 1
                    #         # print code,w_dict[code]
                    #         # print (w_dict[code])
                    #         top_all.loc[code, 'lastp'] = w_dict[code]
                    #         # top_all.loc[code, 'llow'] = w_dict[code][1]
                    # # print i, len(codelist)
                    time_s = time.time()
                else:
                    if 'counts' in top_now.columns.values:
                        if not 'counts' in top_all.columns.values:
                            top_all['counts'] = 0
                    if time_d - time_s > delay_time:
                        status_change = True
                    else:
                        status_change = False

                    for symbol in top_now.index:
                        # code = rl._symbol_to_code(symbol)
                        if symbol in top_all.index and top_all.loc[symbol, 'buy']<>0:
                            # if top_all.loc[symbol,'diff'] == 0:
                            # print "code:",symbol
                            count_n = top_now.loc[symbol, 'buy']
                            count_a = top_all.loc[symbol, 'buy']
                            # print count_a,count_n
                            # print count_n,count_a
                            if not count_n == count_a:
                                top_now.loc[symbol, 'diff'] = round(((float(count_n) - float(count_a)) / float(count_a) * 100), 1)
                                if status_change and 'counts' in top_now.columns.values:
                                    # print "change:",time.time()-time_s
                                    # top_now.loc[symbol,'lastp']=top_all.loc[symbol,'lastp']
                                    top_all.loc[symbol, 'buy':'counts'] = top_now.loc[symbol,'buy':'counts']
                                else:
                                    # top_now.loc[symbol,'lastp']=top_all.loc[symbol,'lastp']
                                    top_all.loc[symbol, 'diff':'low'] = top_now.loc[symbol, 'diff':'low']
                            elif 'counts' in top_now.columns.values:
                                top_all.loc[symbol, 'percent':'counts'] = top_now.loc[symbol, 'percent':'counts']
                            else:
                                top_all.loc[symbol, 'percent':'low'] = top_now.loc[symbol, 'percent':'low']

                                # top_all.loc[symbol]=top_now.loc[symbol]?
                                # top_all.loc[symbol,'diff']=top_now.loc[symbol,'counts']-top_all.loc[symbol,'counts']

                                # else:
                                # value=top_all.loc[symbol,'diff']

                                # else:
                                #     if float(top_now.loc[symbol,'low'])>float(top_all.loc[symbol,'lastp']):
                                #         # top_all.append(top_now.loc[symbol])
                                #         print "not all ???"

                # top_all=top_all.sort_values(by=['diff','percent','counts'],ascending=[0,0,1])
                # top_all=top_all.sort_values(by=['diff','ratio','percent','counts'],ascending=[0,1,0,1])

                # top_all = top_all[top_all.open>=top_all.low*0.99]
                # top_all = top_all[top_all.buy >= top_all.open*0.99]
                # top_all = top_all[top_all.trade >= top_all.low*0.99]
                # top_all = top_all[top_all.trade >= top_all.high*0.99]
                # top_all = top_all[top_all.buy >= top_all.lastp]
                # top_all = top_all[top_all.percent >= 0]

                top_dif = top_all
                log.info('dif1:%s'%len(top_dif))
                print top_dif[:3]
                top_dif = top_dif[top_dif.buy > top_dif.lastp]
                log.info('dif2:%s'%len(top_dif))


                if not top_dif[:1].low.values==0:
                    top_dif = top_dif[top_dif.low > top_dif.lastp]
                    log.info('dif3 low<>0 :%s'%len(top_dif))


                    top_dif = top_dif[top_dif.open > top_dif.lastp]
                    log.info('dif4 open>lastp:%s'%len(top_dif))

                    top_dif = top_dif[top_dif.buy >= top_dif.open*0.99]
                    log.info('dif5 buy>open:%s'%len(top_dif))

                    # top_dif = top_dif[top_dif.trade >= top_dif.buy]
                    top_dif = top_dif[top_dif.buy >= top_dif.high * 0.99]
                    log.info('dif6 buy>high:%s'%len(top_dif))

                    top_dif = top_dif[top_dif.percent >= 0]
                # print len(top_dif),top_dif[:1]
                print ("A:%s N:%s K:%s %s G:%s"%(len(df), len(top_now), len(top_all)-len(top_all[top_all.low.values==0]),len(top_all[top_all.low.values==0]),len(top_dif))),
                print "Rt:%0.3f"%(float(time.time() - time_Rt))
                if 'counts' in top_dif.columns.values:
                    top_dif = top_dif.sort_values(by=['diff', 'percent', 'counts', 'ratio'], ascending=[0, 0, 1, 1])
                else:
                    print "Good Morning!!!"
                    top_dif = top_dif.sort_values(by=['diff', 'percent', 'ratio'], ascending=[0, 0, 1])
                if time_d - time_s > delay_time:
                    time_s = time.time()
                # top_all=top_all.sort_values(by=['percent','diff','counts','ratio'],ascending=[0,0,1,1])
                print rl.format_for_print(top_dif[:10])
                # print rl.format_for_print(top_dif[-1:])
                # print "staus",status
                if status:
                    for code in top_dif[:10].index:
                        code = re.findall('(\d+)', code)
                        if len(code) > 0:
                            code = code[0]
                            kind = sl.get_multiday_ave_compare_silent(code)
                # print top_all[top_all.low.values==0]

                # else:
                #     print "\t No RealTime Data"
            else:
                print "\tNo Data"
            time.sleep(60)

        except (KeyboardInterrupt) as e:
            # print "key"
            print "KeyboardInterrupt:", e
            # time.sleep(1)
            # if success > 3:
            #     raw_input("Except")
            #     sys.exit(0)
            st = raw_input("status:[go(g),clear(c),quit(q,e),W(w),Wa(a)]:")
            if len(st) == 0:
                status = False
            elif st == 'g' or st == 'go':
                status = True
                for code in top_dif[:10].index:
                    code = re.findall('(\d+)', code)
                    if len(code) > 0:
                        code = code[0]
                        kind = sl.get_multiday_ave_compare_silent(code)
            elif st == 'clear' or st == 'c':
                top_all = pd.DataFrame()
                status = False
            elif st == 'w' or st == 'a':
                codew=(top_dif.index).tolist()
                if st=='a':
                    sl.write_to_blocknew(block_path,codew[:10])
                    sl.write_to_blocknew(all_diffpath,codew)
                else:
                    sl.write_to_blocknew(block_path,codew[:10],False)
                    sl.write_to_blocknew(all_diffpath,codew,False)
                print "wri ok"
                # time.sleep(2)

            else:
                sys.exit(0)
        except (IOError, EOFError, Exception) as e:
            print "Error", e

            traceback.print_exc()
            # raw_input("Except")


            # sl.get_code_search_loop()
            # print data.describe()
            # while 1:
            #     intput=raw_input("code")
            #     print
            # pd = DataFrame(data)
            # print pd
            # parsehtml("""
            # <a href="www.google.com"> google.com</a>
            # <A Href="www.pythonclub.org"> PythonClub </a>
            # <A HREF = "www.sina.com.cn"> Sina </a>
            # """)
'''
{symbol:"sz000001",code:"000001",name:"平安银行",trade:"0.00",pricechange:"0.000",changepercent:"0.000",buy:"12.36",sell:"12.36",settlement:"12.34",open:"0.00",high:"0.00",low:"0",volume:0,amount:0,ticktime:"09:17:55",per:7.133,pb:1.124,mktcap:17656906.355526,nmc:14566203.350486,turnoverratio:0},
{symbol:"sz000002",code:"000002",name:"万  科Ａ",trade:"0.00",pricechange:"0.000",changepercent:"0.000",buy:"0.00",sell:"0.00",settlement:"24.43",open:"0.00",high:"0.00",low:"0",volume:0,amount:0,ticktime:"09:17:55",per:17.084,pb:3.035,mktcap:26996432.575,nmc:23746405.928119,turnoverratio:0},

python -m cProfile -s cumulative timing_functions.py
http://www.jb51.net/article/63244.htm

'''