# -*- coding:utf-8 -*-
"""
Created on 2014/07/31
@author: Jimmy Liu
@group : waditu
@contact: jimmysoa@sina.cn
"""

VERSION = '0.3.6'
K_LABELS = ['D', 'W', 'M']
K_MIN_LABELS = ['5', '15', '30', '60']
K_TYPE = {'D': 'akdaily', 'W': 'akweekly', 'M': 'akmonthly'}
INDEX_LABELS = ['sh', 'sz', 'hs300', 'sz50', 'cyb', 'zxb']
REAL_INDEX_LABELS=['sh_a','sz_a','cyb']
INDEX_LIST = {'sh': 'sh000001', 'sz': 'sz399001', 'hs300': 'sz399300',
              'sz50': 'sh000016', 'zxb': 'sz399005', 'cyb': 'sz399006'}
DD_VOL_List={'0':'40000','1':'100000','2':'100000','3':'200000','4':'1000000'}
LvolumeSize = 125000
DD_TYPE_List={'0':'5','1':'10','2':'20','3':'50','4':'100'}
P_TYPE = {'http': 'http://', 'ftp': 'ftp://'}
PAGE_NUM = [38, 60, 80, 100]
FORMAT = lambda x: '%.2f' % x
DOMAINS = {'sina': 'sina.com.cn', 'sinahq': 'sinajs.cn',
           'ifeng': 'ifeng.com', 'sf': 'finance.sina.com.cn',
           'vsf': 'vip.stock.finance.sina.com.cn',
           'idx': 'www.csindex.com.cn', '163': 'money.163.com',
           'em': 'eastmoney.com', 'sseq': 'query.sse.com.cn',
           'sse': 'www.sse.com.cn', 'szse': 'www.szse.cn',
           'oss': '218.244.146.57', 'idxip':'115.29.204.48',
           'shibor': 'www.shibor.org'}
PAGES = {'fd': 'index.phtml', 'dl': 'downxls.php', 'jv': 'json_v2.php',
         'cpt': 'newFLJK.php', 'ids': 'newSinaHy.php', 'lnews':'rollnews_ch_out_interface.php',
         'ntinfo':'vCB_BulletinGather.php', 'hs300b':'000300cons.xls',
         'hs300w':'000300closeweight.xls','sz50b':'000016cons.xls',
         'dp':'all_fpya.php', '163dp':'fpyg.html',
         'emxsg':'JS.aspx', '163fh':'jjcgph.php',
         'newstock':'vRPD_NewStockIssue.php', 'zz500b':'000905cons.xls',
         'zz500wt':'000905closeweight.xls',
         't_ticks':'vMS_tradedetail.php', 'dw': 'downLoad.html',
         'qmd':'queryMargin.do', 'szsefc':'ShowReport.szse',
         'ssecq':'commonQuery.do', 'sinadd':'cn_bill_download.php','sinadd_all':'cn_bill_all.php'}
TICK_COLUMNS = ['time', 'price', 'change', 'volume', 'amount', 'type']
TODAY_TICK_COLUMNS = ['time', 'price', 'pchange', 'change', 'volume', 'amount', 'type']
DAY_TRADING_COLUMNS = ['code', 'symbol', 'name', 'changepercent',
                       'trade', 'open', 'high', 'low', 'settlement', 'volume', 'turnoverratio']
REPORT_COLS = ['code', 'name', 'eps', 'eps_yoy', 'bvps', 'roe',
               'epcf', 'net_profits', 'profits_yoy', 'distrib', 'report_date']
FORECAST_COLS = ['code', 'name', 'type', 'report_date', 'pre_eps', 'range']
PROFIT_COLS = ['code', 'name', 'roe', 'net_profit_ratio',
               'gross_profit_rate', 'net_profits', 'eps', 'business_income', 'bips']
OPERATION_COLS = ['code', 'name', 'arturnover', 'arturndays', 'inventory_turnover',
                  'inventory_days', 'currentasset_turnover', 'currentasset_days']
GROWTH_COLS = ['code', 'name', 'mbrg', 'nprg', 'nav', 'targ', 'epsg', 'seg']
DEBTPAYING_COLS = ['code', 'name', 'currentratio',
                   'quickratio', 'cashratio', 'icratio', 'sheqratio', 'adratio']
CASHFLOW_COLS = ['code', 'name', 'cf_sales', 'rateofreturn',
                 'cf_nm', 'cf_liabilities', 'cashflowratio']
DAY_PRICE_COLUMNS = ['date', 'open', 'high', 'close', 'low', 'volume', 'price_change', 'p_change',
                     'ma5', 'ma10', 'ma20', 'v_ma5', 'v_ma10', 'v_ma20', 'turnover']
INX_DAY_PRICE_COLUMNS = ['date', 'open', 'high', 'close', 'low', 'volume', 'price_change', 'p_change',
                         'ma5', 'ma10', 'ma20', 'v_ma5', 'v_ma10', 'v_ma20']
LIVE_DATA_COLS = ['name', 'open', 'pre_close', 'price', 'high', 'low', 'bid', 'ask', 'volume', 'amount',
                  'b1_v', 'b1_p', 'b2_v', 'b2_p', 'b3_v', 'b3_p', 'b4_v', 'b4_p', 'b5_v', 'b5_p',
                  'a1_v', 'a1_p', 'a2_v', 'a2_p', 'a3_v', 'a3_p', 'a4_v', 'a4_p', 'a5_v', 'a5_p', 'date', 'time', 's']
FOR_CLASSIFY_B_COLS = ['code', 'name']
FOR_CLASSIFY_W_COLS = ['date', 'code', 'weight']
TICK_PRICE_URL = '%smarket.%s/%s?date=%s&symbol=%s'
TODAY_TICKS_PAGE_URL = '%s%s/quotes_service/api/%s/CN_Transactions.getAllPageTime?date=%s&symbol=%s'
TODAY_TICKS_URL = '%s%s/quotes_service/view/%s?symbol=%s&date=%s&page=%s'
DAY_PRICE_URL = '%sapi.finance.%s/%s/?code=%s&type=last'
LIVE_DATA_URL = '%shq.%s/rn=%s&list=%s'
DAY_PRICE_MIN_URL = '%sapi.finance.%s/akmin?scode=%s&type=%s'
SINA_DAY_PRICE_URL = '%s%s/quotes_service/api/%s/Market_Center.getHQNodeData?num=80&sort=changepercent&asc=0&node=hs_a&symbol=&_s_r_a=page&page=%s'
SINA_REAL_PRICE_CODE = '%s%s/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=%s&sort=changepercent&asc=0&node=%s&symbol=%s'
REPORT_URL = '%s%s/q/go.php/vFinanceAnalyze/kind/mainindex/%s?s_i=&s_a=&s_c=&reportdate=%s&quarter=%s&p=%s&num=%s'
FORECAST_URL = '%s%s/q/go.php/vFinanceAnalyze/kind/performance/%s?s_i=&s_a=&s_c=&s_type=&reportdate=%s&quarter=%s&p=%s&num=%s'
PROFIT_URL = '%s%s/q/go.php/vFinanceAnalyze/kind/profit/%s?s_i=&s_a=&s_c=&reportdate=%s&quarter=%s&p=%s&num=%s'
OPERATION_URL = '%s%s/q/go.php/vFinanceAnalyze/kind/operation/%s?s_i=&s_a=&s_c=&reportdate=%s&quarter=%s&p=%s&num=%s'
GROWTH_URL = '%s%s/q/go.php/vFinanceAnalyze/kind/grow/%s?s_i=&s_a=&s_c=&reportdate=%s&quarter=%s&p=%s&num=%s'
DEBTPAYING_URL = '%s%s/q/go.php/vFinanceAnalyze/kind/debtpaying/%s?s_i=&s_a=&s_c=&reportdate=%s&quarter=%s&p=%s&num=%s'
CASHFLOW_URL = '%s%s/q/go.php/vFinanceAnalyze/kind/cashflow/%s?s_i=&s_a=&s_c=&reportdate=%s&quarter=%s&p=%s&num=%s'
SHIBOR_TYPE ={'Shibor': 'Shibor数据', 'Quote': '报价数据', 'Tendency': 'Shibor均值数据',
              'LPR': 'LPR数据', 'LPR_Tendency': 'LPR均值数据'}
SHIBOR_DATA_URL = '%s%s/shibor/web/html/%s?nameNew=Historical_%s_Data_%s.xls&downLoadPath=data&nameOld=%s%s.xls&shiborSrc=http://www.shibor.org/shibor/'
ALL_STOCK_BASICS_FILE = '%s%s/static/all.csv'%(P_TYPE['http'], DOMAINS['oss'])
SINA_CONCEPTS_INDEX_URL = '%smoney.%s/q/view/%s?param=class'
SINA_INDUSTRY_INDEX_URL = '%s%s/q/view/%s'
SINA_DATA_DETAIL_URL = '%s%s/quotes_service/api/%s/Market_Center.getHQNodeData?page=1&num=400&sort=symbol&asc=1&node=%s&symbol=&_s_r_a=page'
INDEX_C_COMM = 'sseportal/ps/zhs/hqjt/csi'
HS300_CLASSIFY_URL_FTP = '%s%s/webdata/%s'
HS300_CLASSIFY_URL_HTTP = '%s%s/%s/%s'
HIST_FQ_URL = '%s%s/corp/go.php/vMS_FuQuanMarketHistory/stockid/%s.phtml?year=%s&jidu=%s'
HIST_INDEX_URL = '%s%s/corp/go.php/vMS_MarketHistory/stockid/%s/type/S.phtml?year=%s&jidu=%s'
HIST_FQ_FACTOR_URL = '%s%s/api/json.php/BasicStockSrv.getStockFuQuanData?symbol=%s&type=hfq'
INDEX_HQ_URL = '''%shq.%s/rn=xppzh&list=sh000001,sh000002,sh000003,sh000008,sh000009,sh000010,sh000011,sh000012,sh000016,sh000017,sh000300,sz399001,sz399002,sz399003,sz399004,sz399005,sz399006,sz399100,sz399101,sz399106,sz399107,sz399108,sz399333,sz399606'''
SSEQ_CQ_REF_URL = '%s%s/assortment/stock/list/name'
ALL_STK_URL = '%s%s/all.csv'
SINA_DD = '%s%s/quotes_service/view/%s?symbol=%s&num=60&page=1&sort=ticktime&asc=0&volume=40000&amount=0&type=0&day=%s'


'''
Johnson Add
'''

PowerCount = 30
PowerCountdl = 10
SINA_DD_Now = '%s%s/quotes_service/view/%s?symbol=%s&num=60&page=1&sort=ticktime&asc=0&volume=40000&amount=0&type=0'
SINA_DD_VRatio_10 = '%s%s/quotes_service/view/%s?num=100&page=1&sort=ticktime&asc=0&volume=%s&type=%s'
SINA_DD_VRatio = '%s%s/quotes_service/view/%s?num=100&page=1&sort=ticktime&asc=0&volume=%s&type=%s'
SINA_DD_VRatio_All = '%s%s/quotes_service/view/%s?num=%s&page=1&sort=ticktime&asc=0&volume=%s&type=%s'


JSON_DD_CountURL="http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_Bill.GetBillListCount?num=100&page=1&sort=ticktime&asc=0&volume=%s&type=%s"
JSON_DD_Data_URL="http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_Bill.GetBillList?num=%s&page=1&sort=ticktime&asc=0&volume=%s&type=%s"
JSON_DD_Data_URL_Page="http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_Bill.GetBillList?num=%s&page=%s&sort=ticktime&asc=0&volume=%s&type=%s"

JSON_Market_Center_RealURL="http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=%s&num=%s&sort=changepercent&asc=0&node=%s&symbol="
JSON_Market_Center_CountURL="http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeStockCount?node=%s"
# SINA_DAY_PRICE_URL =                                      '%s%s/quotes_service/api/%s/Market_Center.getHQNodeData?num=80&sort=changepercent&asc=0&node=hs_a&symbol=&_s_r_a=page&page=%s'
# http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?num=80&sort=changepercent&asc=0&node=hs_a&symbol=&_s_r_a=page&page=1
SINA_Market_KEY={'sh':'sh_a','sz':'sz_a','cyb':'cyb'}
SINA_Market_COLUMNS = ['code', 'name', 'trade', 'buy', 'percent', 'open', 'high', 'low', 'volume', 'ticktime', 'ratio']
# SINA_Total_Columns_Clean = ['code', 'name', 'trade', 'buy','bid1','bid1_volume','ask1',
                      # 'ask1_volume', 'percent', 'open', 'close', 'high', 'low', 'volume',
                            # 'ratio']
                           
# SINA_Total_Columns = ['code', 'name', 'open','now','close', 'trade', 'high', 'low', 'buy', 'sell', 'volume',
                      # 'turnover', 'bid1_volume', 'bid1', 'bid2_volume', 'bid2', 'bid3_volume',
                      # 'bid3', 'bid4_volume', 'bid4', 'bid5_volume', 'bid5', 'ask1_volume',
                      # 'ask1', 'ask2_volume', 'ask2', 'ask3_volume', 'ask3', 'ask4_volume',
                      # 'ask4', 'ask5_volume', 'ask5']

SINA_Total_Columns_Clean = ['code', 'name', 'buy','sell','b1','b1_v','a1',
                      'a1_v', 'open', 'close', 'high', 'low', 'volume',
                            'turnover']                           
SINA_Total_Columns = ['code', 'name', 'open', 'close','now', 'trade', 'high', 'low', 'buy', 'sell', 'volume',
                      'turnover', 'b1_v', 'b1', 'b2_v', 'b2', 'b3_v',
                      'b3', 'b4_v', 'b4', 'b5_v', 'b5', 'a1_v',
                      'a1', 'a2_v', 'a2', 'a3_v', 'a3', 'a4_v',
                      'a4', 'a5_v', 'a5']

SINA_DD_Clean_Count_Columns = ['name', 'percent', 'diff', 'counts', 'trade', 'high', 'open', 'low', 'ratio', 'volume',
                               'prev_price']
SINA_Market_Clean_UP_Columns = ['name', 'buy','trade','diff', 'volume', 'percent', 'ratio', 'high', 'open', 'low', 'counts',
                                'prev_p']
SINA_Market_Clean_UP_ColumnsTrade = ['name', 'trade', 'diff', 'volume', 'percent', 'ratio', 'high', 'open', 'low', 'counts',
                                'prev_p']                               
SINA_Market_Clean_Columns=['name','buy','diff','volume','percent','ratio','high','open','low']
# SINA_Market_Clean_UP_Columns=['name','buy','diff','percent','trade','high','ratio','open','low','counts']

THE_FIELDS = ['code', 'symbol', 'name', 'changepercent', 'trade', 'open', 'high', 'low', 'settlement', 'volume', 'turnoverratio']
# Market_Center_COLUMNS = ['code','name','trade','changepercent','buy','sell','settlement','open','high','low','volume','ticktime','turnoverratio']
DAY_REAL_DD_COLUMNS = ['code','symbol','name','ticktime','price','volume','prev_price','kind']
Status_DD={u"中性盘": "normal", u"买盘": "up", u"卖盘": "down"}
Status_KIND=['U','D','E']

SINA_JSON_API_URL="http://hq.sinajs.cn/list=%s"
SINA_Market_KEY_TO_DFCFW={'sh':'zs000001','sz':'zs399001','cyb':'zs399006','zxb':'zs399005'}
DFCFW_FUND_FLOW_URL="http://s1.dfcfw.com/js/%s.js?rt=0.3585179701661414"
DFCFW_FUND_FLOW_ALL="http://s1.dfcfw.com/js/index.js?rt=0.3585179701661414"
TDX_Day_columns=['code','date','open','high','low','close','vol','amount']

DFCFW_FUND_FLOW_HGT="http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=0000011&sty=SHSTD&st=z&sr=&p=&ps=&cb=&js=var%20quote_zjl%3d{rank:[%28x%29],pages:%28pc%29}&token=beb0a0047196124721f56b0f0ff5a27c&jsName=quote_zjl&dt=1452070103085"
DFCFW_ZS_SHSZ="http://nufm2.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=0000011,3990012&sty=DFPIU&st=z&sr=&p=&ps=&cb=&js=var%20C1Cache={quotation:[(x)]}&token=44c9d251add88e27b65ed86506f6e5da&0.6733153457793924"
DFCFW_RZRQ_SHSZ="http://datainterface.eastmoney.com/EM_DataCenter/js.aspx?type=FD&sty=SHSZSUM&fd=%s"
# DFCFW_RZRQ_SHSZ="http://datainterface.eastmoney.com/EM_DataCenter/js.aspx?type=FD&sty=SHSZSUM&fd=%s&js=var%20rzrqhuizong=[%28x%29]"DFCFW_RZRQ_SHSZ="http://datainterface.eastmoney.com/EM_DataCenter/js.aspx?type=FD&sty=SHSZSUM&fd=%s&js=var%20rzrqhuizong=[%28x%29]"

DF_BK0707='http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=BK07071&sty=DCFF&st=z&sr=&p=&ps=&lvl=&cb=&js=var%20zjlx_detail=%28x%29&token=894050c76af8597a853f5b408b759f5d&rt=0.6872510515345984'





SHIBOR_COLS = ['date', 'ON', '1W', '2W', '1M', '3M', '6M', '9M', '1Y']
QUOTE_COLS = ['date', 'bank', 'ON_B', 'ON_A', '1W_B', '1W_A', '2W_B', '2W_A', '1M_B', '1M_A',
                    '3M_B', '3M_A', '6M_B', '6M_A', '9M_B', '9M_A', '1Y_B', '1Y_A']
SHIBOR_MA_COLS = ['date', 'ON_5', 'ON_10', 'ON_20', '1W_5', '1W_10', '1W_20','2W_5', '2W_10', '2W_20',
                  '1M_5', '1M_10', '1M_20', '3M_5', '3M_10', '3M_20', '6M_5', '6M_10', '6M_20',
                  '9M_5', '9M_10', '9M_20','1Y_5', '1Y_10', '1Y_20']
LPR_COLS = ['date', '1Y']
LPR_MA_COLS = ['date', '1Y_5', '1Y_10', '1Y_20']
INDEX_HEADER = 'code,name,open,preclose,close,high,low,0,0,volume,amount,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,d,c,3\n'
INDEX_COLS = ['code', 'name', 'change', 'open', 'preclose', 'close', 'high', 'low', 'volume', 'amount']
HIST_FQ_COLS = ['date', 'open', 'high', 'close', 'low', 'volume', 'amount', 'factor']
SINA_DD_COLS = ['code', 'name', 'time', 'price', 'volume', 'preprice', 'type']
HIST_FQ_FACTOR_COLS = ['code','value']
DATA_GETTING_TIPS = '[Getting data:]'
DATA_GETTING_FLAG = '#'
DATA_ROWS_TIPS = '%s rows data found.Please wait for a moment.'
DATA_INPUT_ERROR_MSG = 'date input error.'
NETWORK_URL_ERROR_MSG = '获取失败，请检查网络和URL'
DATE_CHK_MSG = '年度输入错误：请输入1989年以后的年份数字，格式：YYYY'
DATE_CHK_Q_MSG = '季度输入错误：请输入1、2、3或4数字'
TOP_PARAS_MSG = 'top有误，请输入整数或all.'
LHB_MSG = '周期输入有误，请输入数字5、10、30或60'
TOKEN_F_P = 'tk.csv'
TOKEN_ERR_MSG = '请设置通联数据接口的token凭证码'

import sys
PY3 = (sys.version_info[0] >= 3)
def _write_head():
    sys.stdout.write(DATA_GETTING_TIPS)
    sys.stdout.flush()

def _write_console():
    sys.stdout.write(DATA_GETTING_FLAG)
    sys.stdout.flush()

def _write_tips(tip):
    sys.stdout.write(DATA_ROWS_TIPS%tip)
    sys.stdout.flush()

def _write_msg(msg):
    sys.stdout.write(msg)
    sys.stdout.flush()

def _check_input(year, quarter):
    if isinstance(year, str) or year < 1989 :
        raise TypeError(DATE_CHK_MSG)
    elif quarter is None or isinstance(quarter, str) or quarter not in [1, 2, 3, 4]:
        raise TypeError(DATE_CHK_Q_MSG)
    else:
        return True

def _check_lhb_input(last):
    if last not in [5, 10, 30, 60]:
        raise TypeError(LHB_MSG)
    else:
        return True