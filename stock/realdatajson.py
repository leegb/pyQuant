# -*- coding:utf-8 -*-
"""
交易数据接口 
Created on 2014/07/31
@author: Jimmy Liu
@group : waditu
@contact: jimmysoa@sina.cn
"""
from __future__ import division
import time
import datetime
import json
import lxml.html
from lxml import etree
import pandas as pd
import numpy as np
import johnson_cons as ct
import re
from pandas.compat import StringIO
# from tushare.util import dateu as du
import math
# import multiprocessing

from multiprocessing import cpu_count
from multiprocessing.dummy import Pool as ThreadPool

# import sys
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

# import tabulate as tbl
# http://stackoverflow.com/questions/18528533/pretty-print-pandas-dataframe
# tabulate([list(row) for row in df.values], headers=list(df.columns))

from prettytable import *

def set_default_encode(code='utf-8'):
        import sys
        reload(sys)
        sys.setdefaultencoding(code)
        print (sys.getdefaultencoding())
        print (sys.stdout.encoding)


# print pt.PrettyTable([''] + list(df.columns))
def format_for_print(df):
    table = PrettyTable([''] + list(df.columns))
    for row in df.itertuples():
        table.add_row(row)
    return str(table)


def format_for_print2(df):
    table = PrettyTable(list(df.columns))
    for row in df.itertuples():
        table.add_row(row[1:])
    return str(table)


# REAL_INDEX_LABELS=['sh_a','sz_a','cyb']
# DD_VOL_List={'0':'40000','1':'100000','2':'100000','3':'200000','4':'1000000'}
# DD_TYPE_List={'0':'5','1':'10','2':'20','3':'50','4':'100'}
# TICK_COLUMNS = ['time', 'price', 'change', 'volume', 'amount', 'type']
# TODAY_TICK_COLUMNS = ['time', 'price', 'pchange', 'change', 'volume', 'amount', 'type']
# DAY_TRADING_COLUMNS = ['code', 'symbol', 'name', 'changepercent',
#                        'trade', 'open', 'high', 'low', 'settlement', 'volume', 'turnoverratio']
# SINA_DATA_DETAIL_URL = '%s%s/quotes_service/api/%s/Market_Center.getHQNodeData?page=1&num=400&sort=symbol&asc=1&node=%s&symbol=&_s_r_a=page'
# SINA_DAY_PRICE_URL = '%s%s/quotes_service/api/%s/Market_Center.getHQNodeData?num=80&sort=changepercent&asc=0&node=hs_a&symbol=&_s_r_a=page&page=%s'
# SINA_REAL_PRICE_DD = '%s%s/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=%s&sort=changepercent&asc=0&node=%s&symbol=%s'
#
# DAY_REAL_COLUMNS = ['code', 'symbol', 'name', 'changepercent',
#                        'trade', 'open', 'high', 'low', 'settlement', 'volume', 'turnoverratio']

def to_mp_run(cmd, urllist):
    # n_t=time.time()
    pool = ThreadPool(cpu_count())
    # print cpu_count()
    # pool = multiprocessing.Pool(processes=8)
    # for code in codes:
    #     results=pool.apply_async(sl.get_multiday_ave_compare_silent_noreal,(code,60))
    # result=[]
    results = pool.map(cmd, urllist)
    # for code in urllist:
    # result.append(pool.apply_async(cmd,(code,)))

    pool.close()
    pool.join()
    # print "time:MP", (time.time() - n_t)
    return results


def _get_url_data(url):
    # headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Connection': 'keep-alive'}
    req = Request(url, headers=headers)
    fp = urlopen(req, timeout=5)
    data = fp.read()
    fp.close()
    return data


def _write_to_csv(df, filename,indexCode='code'):
    TODAY = datetime.date.today()
    CURRENTDAY=TODAY.strftime('%Y-%m-%d')
#     reload(sys)
#     sys.setdefaultencoding( "gbk" )
    df=df.drop_duplicates(indexCode)
    df=df.set_index(indexCode)
    df.to_csv(CURRENTDAY+'-'+filename+'.csv',encoding='gbk',index=False)#选择保存
    print ("write csv")
    # df.to_csv(filename, encoding='gbk', index=False)


def _get_code_count(type):
    pass


def _parsing_Market_price_json(url):
    """
           处理当日行情分页数据，格式为json
     Parameters
     ------
        pageNum:页码
     return
     -------
        DataFrame 当日所有股票交易数据(DataFrame)
    """
    # ct._write_console()
    # url="http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=50&sort=changepercent&asc=0&node=sh_a&symbol="
    # request = Request(ct.SINA_DAY_PRICE_URL%(ct.P_TYPE['http'], ct.DOMAINS['vsf'],
    #                              ct.PAGES['jv'], pageNum))
    request = Request(url)
    text = urlopen(request, timeout=10).read()
    if text == 'null':
        return None
    reg = re.compile(r'\,(.*?)\:')
    text = reg.sub(r',"\1":', text.decode('gbk') if ct.PY3 else text)
    text = text.replace('"{symbol', '{"symbol')
    text = text.replace('{symbol', '{"symbol"')
    text = text.replace('changepercent', 'percent')
    text = text.replace('turnoverratio', 'ratio')
    # print text
    if ct.PY3:
        jstr = json.dumps(text)
    else:
        jstr = json.dumps(text, encoding='GBK')
    js = json.loads(jstr)
    # print js
    # df = pd.DataFrame(pd.read_json(js, dtype={'code':object}),columns=ct.MARKET_COLUMNS)
    df = pd.DataFrame(pd.read_json(js, dtype={'code': object}),
                      columns=ct.SINA_Market_COLUMNS)
    # print df[:1]
    # df = df.drop('symbol', axis=1)
    df = df.ix[df.volume > 0]
    # print ""
    # print df[:1],len(df.index)
    return df


def _get_sina_Market_url(market='sh_a', count=None, num='1000'):
    if count == None:
        url = ct.JSON_Market_Center_CountURL % (market)
        # print url
        data = _get_url_data(url)
        # print data
        count = re.findall('(\d+)', data, re.S)
        urllist = []

        if len(count) > 0:
            count = count[0]
            if int(count) >= int(num):
                page_count = int(math.ceil(int(count) / int(num)))
                for page in range(1, page_count + 1):
                    # print page
                    url = ct.JSON_Market_Center_RealURL % (page, num, market)
                    # print "url",url
                    urllist.append(url)

            else:
                url = ct.JSON_Market_Center_RealURL % ('1', count, market)
                urllist.append(url)
    # print "%s count: %s"%(market,count),

    # print urllist[0],
    return urllist


def get_sina_Market_json(market='sh_a', num='2000', retry_count=3, pause=0.001):
    start_t = time.time()
    # url="http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=50&sort=changepercent&asc=0&node=sh_a&symbol="
    # SINA_REAL_PRICE_DD = '%s%s/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=%s&sort=changepercent&asc=0&node=%s&symbol=%s'
    """
        一次性获取最近一个日交易日所有股票的交易数据
    return
    -------
      DataFrame
           属性：代码，名称，涨跌幅，现价，开盘价，最高价，最低价，最日收盘价，成交量，换手率
    """
    # ct._write_head()
    if market=='all':
        url_list=[]
        for m in ct.SINA_Market_KEY:
            list=_get_sina_Market_url(m, num=num)
            for l in list:url_list.append(l)
        # print url_list
    else:
        url_list=_get_sina_Market_url(market, num=num)
    # print "url:",url_list
    df = pd.DataFrame()
    # data['code'] = symbol
    # df = df.append(data, ignore_index=True)

    results=to_mp_run(_parsing_Market_price_json,url_list)

    if len(results)>0:
        df = df.append(results, ignore_index=True)
    # for url in url_list:
    #     # print url
    #     data = _parsing_Market_price_json(url)
    #     # print data[:1]
    #     df = df.append(data, ignore_index=True)
    #     # break

    if df is not None:
        # for i in range(2, ct.PAGE_NUM[0]):
        #     newdf = _parsing_dayprice_json(i)
        #     df = df.append(newdf, ignore_index=True)
        # print len(df.index)
        print ("interval:%s" % (format((time.time() - start_t), '.2f')))
        return df
    else:
        print ("no data")
        print ("interval:%s" % (format((time.time() - start_t), '.2f')))
        return []


def _get_sina_json_dd_url(vol='0', type='3', num='10000', count=None):
    urllist = []
    if count == None:
        url = ct.JSON_DD_CountURL % (ct.DD_VOL_List[vol], type)
        # print url
        data = _get_url_data(url)
        # return []
        # print data.find('abc')
        count = re.findall('(\d+)', data, re.S)
        if len(count) > 0:
            count = count[0]
            print ("Big:%s"%(count)),
            if int(count) >= int(num):
                page_count = int(math.ceil(int(count) / int(num)))
                for page in range(1, page_count + 1):
                    # print page
                    url = ct.JSON_DD_Data_URL_Page % ('10000', page, ct.DD_VOL_List[vol], type)
                    urllist.append(url)
            else:
                url = ct.JSON_DD_Data_URL_Page % (count, '1', ct.DD_VOL_List[vol], type)
                urllist.append(url)
    else:
        url = ct.JSON_DD_CountURL % (ct.DD_VOL_List[vol], type)
        # print url
        data = _get_url_data(url)
        # print data
        count_now = re.findall('(\d+)', data, re.S)
        urllist = []
        if count < count_now:
            count_diff = int(count_now) - int(count)
            if int(math.ceil(int(count_diff) / 10000)) >= 1:
                page_start = int(math.ceil(int(count) / 10000))
                page_end = int(math.ceil(int(count_now) / 10000))
                for page in range(page_start, page_end + 1):
                    # print page
                    url = ct.JSON_DD_Data_URL_Page % ('10000', page, ct.DD_VOL_List[vol], type)
                    urllist.append(url)
            else:
                page = int(math.ceil(int(count_now) / 10000))
                url = ct.JSON_DD_Data_URL_Page % ('10000', page, ct.DD_VOL_List[vol], type)
                urllist.append(url)
    # print "url:",urllist[:0]
    return urllist


def _code_to_symbol(code):
    """
        生成symbol代码标志
    """
    if code in ct.INDEX_LABELS:
        return ct.INDEX_LIST[code]
    else:
        if len(code) != 6:
            return ''
        else:
            return 'sh%s' % code if code[:1] in ['5', '6'] else 'sz%s' % code


def _symbol_to_code(symbol):
    """
        生成symbol代码标志
    """
    if code in ct.INDEX_LABELS:
        return ct.INDEX_LIST[code]
    else:
        if len(symbol) != 8:
            return ''
        else:
            return re.findall('(\d+)', symbol)[0]


def _parsing_sina_dd_price_json(url):
    """
           处理当日行情分页数据，格式为json
     Parameters
     ------
        pageNum:页码
     return
     -------
        DataFrame 当日所有股票交易数据(DataFrame)
    """
    ct._write_console()
    # request = Request(ct.SINA_DAY_PRICE_URL%(ct.P_TYPE['http'], ct.DOMAINS['vsf'],
    #                              ct.PAGES['jv'], pageNum))
    # request = Request(url)
    # text = urlopen(request, timeout=10).read()
    text = _get_url_data(url)
    if len(text) < 10:
        return ''
    reg = re.compile(r'\,(.*?)\:')
    text = reg.sub(r',"\1":', text.decode('gbk') if ct.PY3 else text)
    text = text.replace('"{symbol', '{"code')
    text = text.replace('{symbol', '{"code"')

    if ct.PY3:
        jstr = json.dumps(text)
    else:
        jstr = json.dumps(text, encoding='GBK')
    js = json.loads(jstr)
    df = pd.DataFrame(pd.read_json(js, dtype={'code': object}),
                      columns=ct.DAY_REAL_DD_COLUMNS)
    df = df.drop('symbol', axis=1)
    df = df.ix[df.volume > 0]
    # print ""
    # print df['name'][len(df.index)-1:],len(df.index)
    return df


def get_sina_all_json_dd(vol='0', type='3', num='10000', retry_count=3, pause=0.001):
    start_t = time.time()
    # url="http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=50&sort=changepercent&asc=0&node=sh_a&symbol="
    # SINA_REAL_PRICE_DD = '%s%s/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=%s&sort=changepercent&asc=0&node=%s&symbol=%s'
    """
        一次性获取最近一个日交易日所有股票的交易数据
    return
    -------
      DataFrame
           属性：代码，名称，涨跌幅，现价，开盘价，最高价，最低价，最日收盘价，成交量，换手率
    """
    # ct._write_head()
    url_list = _get_sina_json_dd_url(vol, type, num)
    df = pd.DataFrame()
    # data['code'] = symbol
    # df = df.append(data, ignore_index=True)

    data = to_mp_run(_parsing_sina_dd_price_json, url_list)
    # data='null'
    # print len('null')
    # print len(data)
    if len(data)>0:
        df = df.append(data, ignore_index=True)
    # print "df",df.empty
    # for url in url_list:
    #     # print url
    #     data = _parsing_sina_dd_price_json(url)
    #     df=df.append(data,ignore_index=True)

    if not df.empty:
        # for i in range(2, ct.PAGE_NUM[0]):
        #     newdf = _parsing_dayprice_json(i)
        #     df = df.append(newdf, ignore_index=True)
        # print len(df.index)
        print "intervaldf:", (time.time() - start_t),
        return df
    else:
        print "no data"
        print "interval-none:", (time.time() - start_t)
        return ''


def _today_ticks(symbol, tdate, pageNo, retry_count, pause):
    ct._write_console()
    for _ in range(retry_count):
        time.sleep(pause)
        try:
            html = lxml.html.parse(ct.TODAY_TICKS_URL % (ct.P_TYPE['http'],
                                                         ct.DOMAINS['vsf'], ct.PAGES['t_ticks'],
                                                         symbol, tdate, pageNo
                                                         ))
            res = html.xpath('//table[@id=\"datatbl\"]/tbody/tr')
            if ct.PY3:
                sarr = [etree.tostring(node).decode('utf-8') for node in res]
            else:
                sarr = [etree.tostring(node) for node in res]
            sarr = ''.join(sarr)
            sarr = '<table>%s</table>' % sarr
            sarr = sarr.replace('--', '0')
            df = pd.read_html(StringIO(sarr), parse_dates=False)[0]
            df.columns = ct.TODAY_TICK_COLUMNS
            df['pchange'] = df['pchange'].map(lambda x: x.replace('%', ''))
        except Exception as e:
            print(e)
        else:
            return df
    raise IOError(ct.NETWORK_URL_ERROR_MSG)


def _get_today_all():
    """
        一次性获取最近一个日交易日所有股票的交易数据
    return
    -------
      DataFrame
           属性：代码，名称，涨跌幅，现价，开盘价，最高价，最低价，最日收盘价，成交量，换手率
    """
    ct._write_head()
    df = _parsing_dayprice_json(1)
    if df is not None:
        for i in range(2, ct.PAGE_NUM[0]):
            newdf = _parsing_dayprice_json(i)
            df = df.append(newdf, ignore_index=True)
        return df
    else:
        return None


def _get_realtime_quotes(symbols=None):
    """
        获取实时交易数据 getting real time quotes data
       用于跟踪交易情况（本次执行的结果-上一次执行的数据）
    Parameters
    ------
        symbols : string, array-like object (list, tuple, Series).
        
    return
    -------
        DataFrame 实时交易数据
              属性:0：name，股票名字
            1：open，今日开盘价
            2：pre_close，昨日收盘价
            3：price，当前价格
            4：high，今日最高价
            5：low，今日最低价
            6：bid，竞买价，即“买一”报价
            7：ask，竞卖价，即“卖一”报价
            8：volumn，成交量 maybe you need do volumn/100
            9：amount，成交金额（元 CNY）
            10：b1_v，委买一（笔数 bid volume）
            11：b1_p，委买一（价格 bid price）
            12：b2_v，“买二”
            13：b2_p，“买二”
            14：b3_v，“买三”
            15：b3_p，“买三”
            16：b4_v，“买四”
            17：b4_p，“买四”
            18：b5_v，“买五”
            19：b5_p，“买五”
            20：a1_v，委卖一（笔数 ask volume）
            21：a1_p，委卖一（价格 ask price）
            ...
            30：date，日期；
            31：time，时间；
    """
    symbols_list = ''
    if isinstance(symbols, list) or isinstance(symbols, set) or isinstance(symbols, tuple) or isinstance(symbols,
                                                                                                         pd.Series):
        for code in symbols:
            symbols_list += _code_to_symbol(code) + ','
    else:
        symbols_list = _code_to_symbol(symbols)

    symbols_list = symbols_list[:-1] if len(symbols_list) > 8 else symbols_list
    request = Request(ct.LIVE_DATA_URL % (ct.P_TYPE['http'], ct.DOMAINS['sinahq'],
                                          _random(), symbols_list))
    text = urlopen(request, timeout=10).read()
    text = text.decode('GBK')
    reg = re.compile(r'\="(.*?)\";')
    data = reg.findall(text)
    regSym = re.compile(r'(?:sh|sz)(.*?)\=')
    syms = regSym.findall(text)
    data_list = []
    syms_list = []
    for index, row in enumerate(data):
        if len(row) > 1:
            data_list.append([astr for astr in row.split(',')])
            syms_list.append(syms[index])
    if len(syms_list) == 0:
        return None
    df = pd.DataFrame(data_list, columns=ct.LIVE_DATA_COLS)
    df = df.drop('s', axis=1)
    df['code'] = syms_list
    ls = [cls for cls in df.columns if '_v' in cls]
    for txt in ls:
        df[txt] = df[txt].map(lambda x: x[:-2])
    return df


def _fun_except(x):
    if len(x) > 10:
        return x[-10:]
    else:
        return x


def _get_index():
    """
    获取大盘指数行情
    return
    -------
      DataFrame
          code:指数代码
          name:指数名称
          change:涨跌幅
          open:开盘价
          preclose:昨日收盘价
          close:收盘价
          high:最高价
          low:最低价
          volume:成交量(手)
          amount:成交金额（亿元）
    """
    request = Request(ct.INDEX_HQ_URL % (ct.P_TYPE['http'],
                                         ct.DOMAINS['sinahq']))
    text = urlopen(request, timeout=10).read()
    text = text.decode('GBK')
    text = text.replace('var hq_str_sh', '').replace('var hq_str_sz', '')
    text = text.replace('";', '').replace('"', '').replace('=', ',')
    text = '%s%s' % (ct.INDEX_HEADER, text)
    df = pd.read_csv(StringIO(text), sep=',', thousands=',')
    df['change'] = (df['close'] / df['preclose'] - 1) * 100
    df['amount'] = df['amount'] / 100000000
    df['change'] = df['change'].map(ct.FORMAT)
    df['amount'] = df['amount'].map(ct.FORMAT)
    df = df[ct.INDEX_COLS]
    df['code'] = df['code'].map(lambda x: str(x).zfill(6))
    df['change'] = df['change'].astype(float)
    df['amount'] = df['amount'].astype(float)
    return df


def _get_index_url(index, code, qt):
    if index:
        url = ct.HIST_INDEX_URL % (ct.P_TYPE['http'], ct.DOMAINS['vsf'],
                                   code, qt[0], qt[1])
    else:
        url = ct.HIST_FQ_URL % (ct.P_TYPE['http'], ct.DOMAINS['vsf'],
                                code, qt[0], qt[1])
    return url


def _get_hists(symbols, start=None, end=None,
               ktype='D', retry_count=3,
               pause=0.001):
    """
    批量获取历史行情数据，具体参数和返回数据类型请参考get_hist_data接口
    """
    df = pd.DataFrame()
    if isinstance(symbols, list) or isinstance(symbols, set) or isinstance(symbols, tuple) or isinstance(symbols,
                                                                                                         pd.Series):
        for symbol in symbols:
            data = get_hist_data(symbol, start=start, end=end,
                                 ktype=ktype, retry_count=retry_count,
                                 pause=pause)
            data['code'] = symbol
            df = df.append(data, ignore_index=True)
        return df
    else:
        return None

def get_sina_dd_count_price_realTime(df='',mtype='all'):
    '''
    input df count and merge price to df
    '''
    if len(df)==0:
        df = get_sina_all_json_dd('0','4')
    if len(df)>0:
        df['counts']=df.groupby(['code'])['code'].transform('count')
        df=df[(df['kind'] == 'U')]
        df=df.sort_values(by='counts',ascending=0)
        df=df.drop_duplicates('code')
        df=df.loc[:,['code','name','counts']]
        # dz.loc['sh600110','counts']=dz.loc['sh600110'].values[1]+3
        df=df.set_index('code')
        df=df.iloc[0:,0:2]
        df['diff']=0
        dp=get_sina_Market_json(mtype)
        # dp.rename(columns={'close':'Close'},inplace=True)
        if len(dp)>10:
            dp=dp.drop_duplicates()
            dp=dp.dropna('index')
            # print dp[:2]
            dm=pd.merge(df,dp,on='name',how='left').set_index('code')
            dm=dm.dropna('index')
            dm=dm.loc[:,ct.SINA_DD_Clean_Count_Coluns]
        else:
            dm=df
    else:
        dm=''
    return dm

def _code_to_symbol(code):
    """
        生成symbol代码标志
    """
    if code in ct.INDEX_LABELS:
        return ct.INDEX_LIST[code]
    else:
        if len(code) != 6:
            return ''
        else:
            return 'sh%s' % code if code[:1] in ['5', '6', '9'] else 'sz%s' % code


if __name__ == '__main__':
    # df = get_sina_all_json_dd('0', '3')
    df=get_sina_dd_count_price_realTime()
    # df=df.drop_duplicates('code')
    # df=df.set_index('code')
    # _write_to_csv(df,'readdata3')
    print format_for_print(df[:2])
    print len(df)
    import sys

    sys.exit(0)
    # up= df[df['trade']>df['settlement']]
    # print up[:2]
    # df=get_sina_all_json_dd(type='3')
    # print df[:10]
    # df=get_sina_Market_url()
    # for x in df:print ":",x
    df = pd.DataFrame()
    # dz=get_sina_Market_json('sz_a')
    # ds=get_sina_Market_json('sh_a')
    dc = get_sina_Market_json('all')
    # df=df.append(dz,ignore_index=True)
    # df=df.append(ds,ignore_index=True)
    df = df.append(dc, ignore_index=True)
    # df=df[df['changepercent']<5]
    # df = df[df['changepercent'] > 0.2]

    # dd=df[(df['open'] <= df['low']) ]
    # dd=df[(df['open'] <= df['low']) ]
    print df[:2], len(df.index)
    # da[da['changepercent']<9.9].
    # dd=df[(df['open'] <= df['low']) ]
    # dd=df[(df['open'] <= df['low']) ]
    # dd[dd['trade'] >= dd['high']*0.99]
    # sys.exit(0)
