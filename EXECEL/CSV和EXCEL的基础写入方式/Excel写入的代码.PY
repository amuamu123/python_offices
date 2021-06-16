# Excel写入的代码：

import openpyxl 
wb = openpyxl.Workbook() 
sheet = wb.active
sheet.title ='豆瓣'
sheet['A1'] = '豆瓣读书'
rows = [['美国队长','钢铁侠','蜘蛛侠','雷神'],['是','漫威','宇宙', '经典','人物']]
for i in rows:
    sheet.append(i)
print(rows)
wb.save('Marvel.xlsx')