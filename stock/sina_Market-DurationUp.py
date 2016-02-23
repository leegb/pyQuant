# -*- coding:utf-8 -*-
# !/usr/bin/env python

import gc
import re
import sys
import time
import traceback

import pandas as pd

import singleAnalyseUtil as sl
from JSONData import realdatajson as rl
from JSONData import tdx_data_Day as tdd
from JohhnsonUtil import LoggerFactory as LoggerFactory
from JohhnsonUtil import commonTips as cct


# from logbook import Logger,StreamHandler,SyslogHandler
# from logbook import StderrHandler

def parseArgmain():
    # from ConfigParser import ConfigParser
    # import shlex
    import argparse
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-s', '--start', type=int, dest='start',
    # help='Start date', required=True)
    # parser.add_argument('-e', '--end', type=int, dest='end',
    # help='End date', required=True)
    # parser.add_argument('-v', '--verbose', action='store_true', dest='verbose',
    # help='Enable debug info')
    # parser.add_argument('foo', type=int, choices=xrange(5, 10))
    # args = parser.parse_args()
    # print args.square**2
    parser = argparse.ArgumentParser()
    parser.add_argument('dt', type=str, nargs='?', help='20150612')

    # parser.add_argument('dt', nargs='?', type=str, help='20150612')
    # parser.add_argument('dt', nargs='?', type=str, help='20150612')
    # parser.add_argument('-dt', action="store", dest="dtype", type=str, nargs='?',help='20150612')
    # parser.add_argument('dt', action="store", dest="dt", type=str, nargs='?',help='20150612')
    # parser.add_argument('e', nargs='?',action="store", dest="end", type=str, help='end')
    # parser.add_argument('end', nargs='?', type=str, help='20160101')
    # parser.add_argument('-d', action="store", dest="dtype", type=str, nargs='?', choices=['d', 'w', 'm'], default='d',
    # help='DateType')
    # parser.add_argument('-p', action="store", dest="ptype", type=str, choices=['f', 'b'], default='f',
    # help='Price Forward or back')
    # parser.add_argument('-help',type=str,help='Price Forward or back')
    # args = parser.parse_args()
    # args=parser.parse_args(input)
    return parser


if __name__ == "__main__":
    # parsehtml(downloadpage(url_s))
    # StreamHandler(sys.stdout).push_application()
    log = LoggerFactory.getLogger('SinaMarketNew')
    # log.setLevel(LoggerFactory.DEBUG)
    # handler=StderrHandler(format_string='{record.channel}: {record.message) [{record.extra[cwd]}]')
    # log.level = log.debug
    # error_handler = SyslogHandler('Sina-M-Log', level='ERROR')
    if cct.isMac():
        cct.set_console(105, 21)
    else:
        cct.set_console(106, 21)
    status = False
    vol = '0'
    type = '2'
    success = 0
    top_all = pd.DataFrame()
    time_s = time.time()
    delay_time = 720000
    # delay_time = cct.get_delay_time()
    First = True
    base_path = tdd.get_tdx_dir()
    block_path = tdd.get_tdx_dir_blocknew() + '061.blk'
    status_change = False
    lastpTDX_DF = ''
    duration_date = 20160101
    ptype = 'low'
    filter='y'
    # all_diffpath = tdd.get_tdx_dir_blocknew() + '062.blk'
    while 1:
        try:
            # df = sina_data.Sina().all
            df = rl.get_sina_Market_json('all')
            top_now = rl.get_market_price_sina_dd_realTime(df, vol, type)
            top_dif = top_now
            # top_now.to_hdf("testhdf5", 'marketDD', format='table', complevel=9)
            now_count = len(top_now)
            del df
            gc.collect()
            radio_t = cct.get_work_time_ratio()
            # top_now = top_now[top_now.buy > 0]
            time_Rt = time.time()
            time_d = time.time()
            if time_d - time_s > delay_time:
                status_change = True
                time_s = time.time()
                top_all = pd.DataFrame()
            else:
                status_change = False
            # print ("Buy>0:%s" % len(top_now[top_now['buy'] > 0])),
            if len(top_now) > 10 or cct.get_work_time():
                time_Rt = time.time()
                if len(top_all) == 0 and len(lastpTDX_DF) == 0:
                    top_all = top_now
                    codelist = top_all.index.tolist()
                    log.info('toTDXlist:%s' % len(codelist))
                    # tdxdata = tdd.get_tdx_all_day_LastDF(codelist,dt=duration_date,ptype=ptype)
                    tdxdata = tdd.get_tdx_exp_all_LastDF(codelist, dt=duration_date, ptype=ptype)
                    log.debug("TdxLastP: %s %s" % (len(tdxdata), tdxdata.columns.values))
                    tdxdata.rename(columns={'low': 'llow'}, inplace=True)
                    tdxdata.rename(columns={'high': 'lhigh'}, inplace=True)
                    tdxdata.rename(columns={'close': 'lastp'}, inplace=True)
                    tdxdata.rename(columns={'vol': 'lvol'}, inplace=True)
                    tdxdata = tdxdata.loc[:, ['llow', 'lhigh', 'lastp', 'lvol', 'date']]
                    log.debug("TDX Col:%s" % tdxdata.columns.values)
                    top_all = top_all.merge(tdxdata, left_index=True, right_index=True, how='left')
                    lastpTDX_DF = tdxdata
                    log.info('Top-merge_now:%s' % (top_all[:1]))
                    top_all = top_all[top_all['llow'] > 0]
                    time_Rt = time.time()
                elif len(top_all) == 0 and len(lastpTDX_DF) > 0:
                    top_all = top_now
                    top_all = top_all.merge(lastpTDX_DF, left_index=True, right_index=True, how='left')
                    # lastpTDX_DF=tdxdata
                    log.info('Top-merge_now:%s' % (top_all[:1]))
                    top_all = top_all[top_all['llow'] > 0]

                else:
                    if 'counts' in top_now.columns.values:
                        if not 'counts' in top_all.columns.values:
                            top_all['counts'] = 0
                            top_all['prev_p'] = 0
                    for symbol in top_now.index:
                        if 'counts' in top_now.columns.values:
                            top_all.loc[symbol, 'buy':'prev_p'] = top_now.loc[symbol, 'buy':'prev_p']
                        else:
                            # top_now.loc[symbol, 'diff'] = round(
                            # ((float(top_now.loc[symbol, 'buy']) - float(
                            # top_all.loc[symbol, 'lastp'])) / float(top_all.loc[symbol, 'lastp']) * 100),
                            # 1)
                            top_all.loc[symbol, 'buy':'low'] = top_now.loc[symbol, 'buy':'low']
                            # top_all.loc[symbol, 'buy'] = top_now.loc[symbol, 'buy']
                # top_all = top_all[top_all.buy > 0]
                top_dif = top_all
                if cct.get_now_time_int() < 935:
                    top_dif['diff'] = (
                        map(lambda x, y: round((x - y) / y * 100, 1), top_dif['buy'].values, top_dif['lastp'].values))
                    top_dif = top_dif[top_dif.buy > 0]
                else:
                    top_dif['diff'] = (
                        map(lambda x, y: round((x - y) / y * 100, 1), top_dif['trade'].values, top_dif['lastp'].values))
                    # print top_dif.loc['600610',:]
                    top_dif=top_dif[top_dif.low > 0]
                    top_dif = top_dif[top_dif.trade > 0]
                    # top_dif.loc['600610','volume':'lvol']

                top_dif=top_dif[top_dif.lvol > 50000]
                top_dif['volume'] = (
                    map(lambda x, y: round(x / y / radio_t, 1), top_dif.volume.values, top_dif.lvol.values))
                # top_dif = top_dif[top_dif.volume < 100]
                # print top_dif.loc['002504',:]
                if filter == 'y':
                    top_dif = top_dif[top_dif.date > cct.day8_to_day10(duration_date)]

                log.info('dif1:%s' % len(top_dif))
                log.info(top_dif[:1])
                # top_dif = top_dif[top_dif.buy > top_dif.lastp]
                # top_dif = top_dif[top_dif.buy > top_dif.lhigh]
                # log.debug('dif2:%s' % len(top_dif))
                # top_dif['volume'] = top_dif['volume'].apply(lambda x: round(x / radio_t, 1))
                # log.debug("top_diff:vol")
                # top_dif = top_dif[top_dif.volume > 1]
                if len(top_dif) == 0:
                    print "No G,DataFrame is Empty!!!!!!"
                log.debug('dif6 vol:%s' % (top_dif[:1].volume))
                log.debug('dif6 vol>lvol:%s' % len(top_dif))

                # top_dif = top_dif[top_dif.buy >= top_dif.open*0.99]
                # log.debug('dif5 buy>open:%s'%len(top_dif))
                # top_dif = top_dif[top_dif.trade >= top_dif.buy]
                # df['volume']= df['volume'].apply(lambda x:x/100)

                goldstock = len(top_dif[top_dif.buy >= top_dif.high * 0.99])
                # goldstock=len(top_dif[top_dif.buy >(top_dif.high-top_dif.low)/2])
                print ("N:%s K:%s %s G:%s" % (
                    now_count, len(top_all[top_all['buy'] > 0]),
                    len(top_now[top_now['volume'] <= 0]), goldstock)),
                print "Rt:%0.1f dT:%s" % (float(time.time() - time_Rt), cct.get_time_to_date(time_s))
                if ptype == 'low':
                    if 'counts' in top_dif.columns.values:
                        top_dif = top_dif.sort_values(by=['diff', 'percent', 'volume', 'counts', 'ratio'],
                                                      ascending=[0, 0, 0, 1, 1])
                    else:
                        top_dif = top_dif.sort_values(by=['diff', 'percent', 'ratio'], ascending=[0, 0, 1])
                else:
                    top_dif['diff']=top_dif['diff'].apply(lambda x:x*2 if x > 0 else x )
                    if 'counts' in top_dif.columns.values:
                        top_dif = top_dif.sort_values(by=['diff', 'percent', 'volume', 'counts', 'ratio'],
                                                      ascending=[1, 0, 0, 1, 1])
                    else:
                        top_dif = top_dif.sort_values(by=['diff', 'percent', 'ratio'], ascending=[1, 0, 1])

                # top_all=top_all.sort_values(by=['percent','diff','counts','ratio'],ascending=[0,0,1,1])
                # print rl.format_for_print(top_dif[:10])
                # top_dd = pd.concat([top_dif[:5],top_temp[:3],top_dif[-3:],top_temp[-3:]], axis=0)
                top_dd = pd.concat([top_dif[:10], top_dif[-5:]], axis=0)
                if cct.get_now_time_int() < 935:
                    top_dd = top_dd.loc[:,
                             ['name', 'buy', 'diff', 'volume', 'percent', 'ratio', 'counts', 'high', 'lastp', 'date']]
                else:
                    top_dd = top_dd.loc[:,
                             ['name', 'trade', 'diff', 'volume', 'percent', 'ratio', 'counts', 'high', 'lastp', 'date']]
                print rl.format_for_print(top_dd)
                # if cct.get_now_time_int() < 930 or cct.get_now_time_int() > 1505 or (cct.get_now_time_int() > 1125 and cct.get_now_time_int() < 1505):
                # print rl.format_for_print(top_dif[-10:])
                # print top_all.loc['000025',:]
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
            int_time = cct.get_now_time_int()
            if cct.get_work_time():
                if int_time < 925:
                    time.sleep(120)
                elif int_time < 930:
                    time.sleep((930 - int_time) * 60)
                    # top_all = pd.DataFrame()
                    time_s = time.time()
                else:
                    time.sleep(120)
            elif cct.get_work_duration():
                while 1:
                    time.sleep(120)
                    if cct.get_work_duration():
                        print ".",
                        time.sleep(120)
                    else:
                        # top_all = pd.DataFrame()
                        time_s = time.time()
                        print "."
                        break
            else:
                raise KeyboardInterrupt("StopTime")
        except (KeyboardInterrupt) as e:
            st = raw_input("status:[go(g),clear(c),[d 20150101 low|high],quit(q,e),W(w),Wa(a)]:")
            if len(st) == 0:
                status = False
            elif st == 'r':
                end = True
                while end:
                    cmd=(raw_input('DEBUG[top_dif,top_now,e|q]:'))
                    if cmd =='e' or cmd=='q' or len(cmd)==0:
                        break
                    else:
                        print eval(cmd)
                # raise KeyboardInterrupt("StopTime")
            elif st == 'g' or st == 'go':
                status = True
                for code in top_dif[:10].index:
                    code = re.findall('(\d+)', code)
                    if len(code) > 0:
                        code = code[0]
                        kind = sl.get_multiday_ave_compare_silent(code)
            elif st == 'clear' or st == 'c':
                top_all = pd.DataFrame()
                time_s = time.time()
                status = False
            elif st.startswith('d') or st.startswith('dt'):
                dl = st.split()
                if len(dl) == 2:
                    dt = dl[1]
                elif len(dl) == 3:
                    dt = dl[1]
                    p_t = dl[2]
                    if p_t == 'l':
                        ptype = 'low'
                    elif p_t == 'h':
                        ptype = 'high'
                    elif p_t == 'y':
                        filter = 'y'
                    elif p_t == 'n':
                        filter = 'n'
                    else:
                        print ("arg error:%s"%p_t)
                elif len(dl) == 4:
                    dt = dl[1]
                    ptype = dl[2]
                    filter = dl[3]                  
                else:
                    dt = ''
                if len(str(dt)) > 0:
                    if len(str(dt)) < 8:
                        duration_date=tdd.get_duration_price_date('999999', dl=dt,ptype=ptype)
                    else:
                        duration_date = dt
                    top_all = pd.DataFrame()
                    time_s = time.time()
                    status = False
                    lastpTDX_DF = ''
            elif st == 'w' or st == 'a':
                codew = (top_dd.index).tolist()
                if st == 'a':
                    cct.write_to_blocknew(block_path, codew)
                    # sl.write_to_blocknew(all_diffpath, codew)
                else:
                    cct.write_to_blocknew(block_path, codew, False)
                    # sl.write_to_blocknew(all_diffpath, codew, False)
                print "wri ok:%s" % block_path

                # time.sleep(2)
            else:
                sys.exit(0)
        except (IOError, EOFError, Exception) as e:
            print "Error", e
            traceback.print_exc()
          
'''
{symbol:"sz000001",code:"000001",name:"平安银行",trade:"0.00",pricechange:"0.000",changepercent:"0.000",buy:"12.36",sell:"12.36",settlement:"12.34",open:"0.00",high:"0.00",low:"0",volume:0,amount:0,ticktime:"09:17:55",per:7.133,pb:1.124,mktcap:17656906.355526,nmc:14566203.350486,turnoverratio:0},
{symbol:"sz000002",code:"000002",name:"万  科Ａ",trade:"0.00",pricechange:"0.000",changepercent:"0.000",buy:"0.00",sell:"0.00",settlement:"24.43",open:"0.00",high:"0.00",low:"0",volume:0,amount:0,ticktime:"09:17:55",per:17.084,pb:3.035,mktcap:26996432.575,nmc:23746405.928119,turnoverratio:0},

python -m cProfile -s cumulative timing_functions.py
http://www.jb51.net/article/63244.htm

'''