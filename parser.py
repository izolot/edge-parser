
import json
import os
import xlsxwriter
import time
import glob


class Parser:
    def __init__(self, root_path:str):
        self.root_path = root_path

    def search_by_time(self, start: str, end: str) -> dict:
        start_time = format_date(start)
        end_time = format_date(end)
        path = self.root_path + start_time['day_path']
        args_dicts = []
        for directory in sorted(os.listdir(path)):
            if start_time['hour'] <= int(directory) and int(directory) <= end_time['hour']:
                pattern = directory + '/*/*/*.json'
                filenames = glob.glob(os.path.join(path, pattern))
                for filename in filenames:
                    with open(filename) as args:
                        json_dict = json.load(args)
                        args_dict = dict()
                        args_dict['path'] = filename[:-9]
                        args_dict['uuid'] = json_dict['uuid']
                        args_dict['time'] = json_dict['time']
                        args_dict['location'] = json_dict['origin']['location']['place']
                        args_dict['images'] = json_dict['measurements'][0]['waypoints']['best']['images']
                        args_dict['plate_text'] = json_dict['measurements'][0]['waypoints']['best']['vehicle']['license-plates'][0]['text']['ucode']
                        args_dicts.append(args_dict)
        print("count json events: ", len(args_dicts))
        return args_dicts
    
    def format_date(self,date: str) -> dict:
        datestr = date.split('.')[0]
        tmp = datetime.datetime.strptime(datestr, "%Y-%m-%dT%H:%M:%S")
        day_path = "{:4d}/{:02d}/{:02d}".format(tmp.year, tmp.month, tmp.day)
        dict_date = {
            "day_path": day_path,
            "hour": tmp.hour,
            "minute": tmp.minute
        }
        return dict_date

def create_excel(data: dict) -> int:
    workbook = xlsxwriter.Workbook('otchet.xlsx')
    worksheet = workbook.add_worksheet()
    excel_format = workbook.add_format(
        {'align': 'center', 'valign': 'vcenter', 'text_wrap': True})

    worksheet.set_column('A:E', 31, excel_format)
    worksheet.write('A1', 'Фото машины')
    worksheet.write('B1', 'Фото ГРЗ')
    worksheet.write('C1', 'Камера')
    worksheet.write('D1', 'Дата и время события')
    worksheet.write('E1', 'Распознанный номер')

    row = 1
    for el in data:
        worksheet.set_row(row, 170, excel_format)
        worksheet.insert_image(
            row, 0, os.path.join(el['path'], el['images']['thumb']['name']),
            {'object_position': 3})
        worksheet.insert_image(
            row, 1, os.path.join(
                el['path'], el['images']['license-plates'][0]['name']),
            {'object_position': 3, 'x_offset': 20, 'y_offset': 20,
                'x_scale': 1.5, 'y_scale': 1.5})
        worksheet.write(row, 2, el['location'])
        worksheet.write(row, 3, el['time'])
        worksheet.write(row, 4, el['plate_text'])
        row += 1

    workbook.close()
    print("Done!")




#for test
def counter_jsonfile(path: str) -> int:
    count = 0
    for _, _, files in os.walk(path):
        for file in files:
            if '.json' in file:
                count += 1

    return count










