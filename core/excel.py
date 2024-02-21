from xlsxwriter.workbook import Workbook
import datetime

def create_table(data: list):
    
    name_table = f'results/{datetime.datetime.now().strftime("%d-%m-%Y %H:%M")}.xlsx'
    workbook = Workbook(name_table)
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, 'Ссылка на профиль')
    worksheet.write(0, 1, 'Имя')
    worksheet.write(0, 2, 'Фамилия')
    worksheet.write(0, 3, 'Город')
    worksheet.write(0, 4, 'Школа')
    worksheet.write(0, 5, 'Год выпуска')
    for i, user in enumerate(data, start=1):
        worksheet.write(i, 0, user['link'])
        worksheet.write(i, 1, user['first_name'])
        worksheet.write(i, 2, user['last_name'])
        worksheet.write(i, 3, user['city'])
        worksheet.write(i, 4, user['school'])
        worksheet.write(i, 5, user['year_to_school'])
    workbook.close()

    return name_table