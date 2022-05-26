import pandas as pd
import csv

# data1 -------------- 物件化excel資料 --------------
df_leave_left = pd.read_excel(
    "testSL.xlsx", sheet_name="ats_leaves", usecols=["staff_no", "leave_start_date", "leave_end_date"])

# data2 -------------- 物件化excel資料 --------------
df_joined_day = pd.read_excel(
    "testSL.xlsx", sheet_name="bas_staff", usecols=["staff_no", "joined_date"])



# data3 員工清單(只有號碼)
get_staff_no = df_leave_left["staff_no"]
staff_ids = []
for i in get_staff_no:
    staff_ids.append(i)
    staff_ids = list(set(staff_ids))

staff_ids = sorted(staff_ids)


# data4 -------------- 紀錄符合病假的員工 --------------
approve_leave_staffs = set()
with open('record_ok_off.csv', 'r') as f:
    rows = csv.reader(f)
    for row in rows:
        if row:
            approve_leave_staffs.add(row[0])
approve_leave_staffs = sorted(list(approve_leave_staffs))
