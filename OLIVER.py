import pandas as pd

# reorder columns
def column_reorder(list,order):
    old_order = list.columns
    new_order = []
    for i in order:
        new_order.append(old_order[i])
    return new_order

# return sheets with on number
def sheets_request(list):
    new_list = []
    for i in list:
        try:
            int(i)
            new_list.append(i)
        except:
            continue
    return new_list


# 自己检查文件路径是否正确
excel_file = "C:\\Users\\NUC Accounting\\Desktop\\Product\\Product_lIST.xlsm"

excel = pd.ExcelFile(excel_file)

list_of_Sheets = excel.sheet_names

list_of_Sheets = sheets_request(list_of_Sheets)

creditor_ref = pd.read_excel(excel_file,sheet_name='BALANCE')
creditor_ref = creditor_ref.iloc[:,1:3].set_index(creditor_ref['A/c No'])

sheet_name = list_of_Sheets

for i in range(len(sheet_name)):

    report = pd.read_excel(excel_file,sheet_name=sheet_name[i],skiprows=2)

    report = report.dropna(how='all',subset=['Invoice/Receipt No.'])

    report = report.set_index('Invoice/Receipt No.')

    need_to_apply = report[report['cross-check']==0]

    need_to_apply = need_to_apply.loc[:,['Date','Remaining Balance']]

    need_to_apply['CREDITER'] = creditor_ref.loc[int(sheet_name[i]),'Name']

    need_to_apply.reset_index(inplace=True)

    new_col = column_reorder(need_to_apply,[3,0,2,1])
    need_to_apply = need_to_apply[new_col]

    if i == 0 :
        final_report = need_to_apply
    else:
        final_report = pd.concat([final_report,need_to_apply])
        
    print(f"{sheet_name[i]} DONE")

final_report.reset_index(drop=True)

# 文件输出路径
final_report.to_csv("C:\\Users\\NUC Accounting\\Desktop\\Product\\invoice_request.csv")
