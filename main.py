from bot import read_token_from_config_file, parse_df, send_message, request_page, soupReq
import time
import schedule
import pandas as pd
import datetime
import numpy as np
import pytz

token = read_token_from_config_file('config.cfg')
isaktoken = read_token_from_config_file('isakconfig.cfg')
url = 'https://api.telegram.org/bot{}/'.format(token)
isakurl = 'https://api.telegram.org/bot{}/'.format(token)
local_time = pytz.timezone("Africa/Lagos")
naive_datetime = datetime.datetime.strptime ("2021-1-28 01:00:00", "%Y-%m-%d %H:%M:%S")
local_datetime = local_time.localize(naive_datetime, is_dst=None)

defi_start_time = local_datetime.astimezone(pytz.utc)
uniswap_start_time = local_datetime.astimezone(pytz.utc)
finance_start_time = local_datetime.astimezone(pytz.utc)

print('Initial defi start time:',defi_start_time,'\n','Initial uniswap start time:',uniswap_start_time,'\n','Initial finance start time:', finance_start_time)

def send_notification():
    global defi_start_time
    global uniswap_start_time
    global finance_start_time
    # Send request to the page
    try:
        defiReq = request_page('https://medium.com/tag/defi/archive/')
        uniswapReq = request_page('https://medium.com/tag/uniswap/archive/')
        financeReq = request_page('https://medium.com/tag/decentralized-finance/archive/')
        if defiReq.status_code == 200:
            sorted_defi_df = soupReq(defiReq)
            resorted_defi_df = sorted_defi_df[sorted_defi_df.time > defi_start_time]
            if len(resorted_defi_df)> 0:
                defi_start_time = resorted_defi_df.iloc[0]['time']
                print('Defi latest post:', defi_start_time)
                defi_data_list = parse_df(resorted_defi_df)
                send_message(url,isakurl, defi_data_list, 'Defi')
            else:
                print('No Defi article yet')
                print('Defi update time still', defi_start_time)
                pass
        else:
            print('defirequest.status_code not 200')
            pass

        if uniswapReq.status_code == 200:
            sorted_uniswap_df = soupReq(uniswapReq)
            resorted_uniswap_df = sorted_uniswap_df[sorted_uniswap_df.time > uniswap_start_time]
            if len(resorted_uniswap_df)> 0:
                uniswap_start_time = resorted_uniswap_df.iloc[0]['time']
                print('Uniswap lastest post:', uniswap_start_time)
                uniswap_data_list = parse_df(resorted_uniswap_df)
                send_message(url,isakurl, uniswap_data_list, 'Uniswap')
            else:
                print('No Uniswap article yet')
                print('Uniswap update time still', uniswap_start_time)
                pass
        else:
            print('uniswaprequest.status_code not 200')
            pass

        if financeReq.status_code == 200:
            sorted_finance_df = soupReq(financeReq)
            resorted_finance_df = sorted_finance_df[sorted_finance_df.time > finance_start_time]
            if len(resorted_finance_df)> 0:
                finance_start_time = resorted_finance_df.iloc[0]['time']
                print('Finance lastest post:', finance_start_time)
                finance_data_list = parse_df(resorted_finance_df)
                send_message(url,isakurl, finance_data_list, 'De-Finance')
            else:
                print('No Finance article yet')
                print('Finance update time still', finance_start_time)
                pass
        else:
            print('financerequest.status_code not 200')
            pass
    except:
        print('Connection error')
        pass
    

#send_notification()
schedule.every(1).minutes.do(send_notification)

while True:
    schedule.run_pending()
    time.sleep(1)



