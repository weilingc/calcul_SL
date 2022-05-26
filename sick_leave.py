# Step2. 員工A B類的帶薪病假有多少天。
'''
1. 病假連續 >= 4天就可以有此帶薪病假
2. 到職後每滿一個月可累積2天病假
3. 到職第二年後每滿一個月可累積4天病假
4. 病假有分兩種 A,B.  A種病假先累積先用。maximum: A:36 B:84
'''
import datetime
from dateutil.relativedelta import *
import pandas as pd
import csv
from staff_data import df_leave_left, staff_ids, approve_leave_staffs, df_joined_day
from daily_update_sick_leave import final_list

# -------------- 自動化計算員工當天的剩餘病假 --------------
#TODO 抓取員工的join_day

for row in df_joined_day.itertuples():
    staff_no = row.staff_no
    # print('現在員工是:',staff_no)
    joined_day = datetime.date(row.joined_date.year, row.joined_date.month, row.joined_date.day)
    today = datetime.date.today()
    joined_period = today - joined_day
    a_sick_leave = 0
    b_sick_leave = 0
    join_calendar = []

    # 遍歷到職日到今天每一天
    for i in range(joined_period.days):
        the_day = joined_day + datetime.timedelta(days=i) #當天
        # join_calendar.append(the_day) #把當天加入員工專屬的日曆中

        # 到職未滿一年的話
        if relativedelta(the_day, joined_day).years < 1:
            if relativedelta(the_day, joined_day).days == 0: #每滿一個月帶薪病假增加2天
                a_sick_leave += 2
        # 到職滿一年的話
        else:
            #如果當天滿一個月~則+四天帶薪病假
            if relativedelta(the_day, joined_day).days == 0: #每滿一個月帶薪病假增加4天
                for i in range(4):
                    if a_sick_leave < 36:
                        a_sick_leave += 1
                    else:
                        if b_sick_leave < 84:
                            b_sick_leave += 1
        # 這邊處理使用帶薪病假
        if staff_no in approve_leave_staffs:
            if str(the_day) in final_list[staff_no]:
                if a_sick_leave >= 1:
                    a_sick_leave -= 1
                else:
                    if b_sick_leave >=1:
                        b_sick_leave -=1
                    else:
                        print('無假可扣')
    # print(f"{staff_no}目前A類病假有{a_sick_leave},B類病假有{b_sick_leave}天")


    #寫在一個表上，紀錄剩餘病假
    with open('per_staff_sick_leave.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([staff_no, a_sick_leave, b_sick_leave])
