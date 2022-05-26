# Step1 此模組用來生成 record_ok_off.csv ----- 紀錄符合申請帶薪病假的員工 以及符合的日期。

import datetime
from dateutil.relativedelta import *
import csv
from staff_data import df_leave_left, staff_ids, approve_leave_staffs

final_list = {}
for staff in staff_ids:
    prev_date = ''
    two_date = ''
    three_date = ''
    ok_list = []
    globals()['staff_ok_list_'+str(staff)] = []
    for row in df_leave_left.itertuples():
        if row.staff_no == staff:
            if row.leave_start_date == row.leave_end_date:
                tmp1 = [i for i in str(row.leave_start_date).split()]
                tmp2 = [int(j) for j in tmp1[0].split('-')]
                this_date = datetime.date(tmp2[0], tmp2[1], tmp2[2])
                if relativedelta(this_date, three_date).months == 0 and relativedelta(this_date, three_date).days == 3:
                    globals()['staff_ok_list_'+str(staff)].append(f"{this_date.year}-{this_date.month:02d}-{this_date.day:02d}")
                    globals()['staff_ok_list_'+str(staff)].append(f"{prev_date.year}-{prev_date.month:02d}-{prev_date.day:02d}")
                    globals()['staff_ok_list_'+str(staff)].append(f"{two_date.year}-{two_date.month:02d}-{two_date.day:02d}")
                    globals()['staff_ok_list_'+str(staff)].append(f"{three_date.year}-{three_date.month:02d}-{three_date.day:02d}")
                    globals()['staff_ok_list_'+str(staff)] = sorted(list(set(globals()['staff_ok_list_'+str(staff)])))
                three_date, two_date, prev_date, this_date = two_date, prev_date, this_date, ''
            else:
                pass

    # 方法一 寫入xlsx檔的方式
    # print(globals()['staff_ok_list_'+str(staff)])
    # if globals()['staff_ok_list_'+str(staff)] != []:
    #     final_list[staff] = globals()['staff_ok_list_'+str(staff)]
    #     df_final_list = pd.DataFrame(list(final_list.items()), columns=['staff_no','ok_off'])
    #     with pd.ExcelWriter("record_ok_off.xlsx") as writer:
    #         df_final_list.to_excel(writer, sheet_name='ok')

    # 方法二 寫入csv檔的方式
    if globals()['staff_ok_list_'+str(staff)] != []:
        # final_list.append(globals()['staff_ok_list_'+str(staff)])
        final_list[staff] = globals()['staff_ok_list_'+str(staff)]
        with open('record_ok_off.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            for i in globals()['staff_ok_list_'+str(staff)]:
                writer.writerow([staff, i])
