import json
import os
import xlsxwriter
import glob
import datetime
import pathlib


class Parser(object):
    def __init__(self, root_path: str):
        self.root_path = root_path
        self.events = []
        self.camera_uuids = {}

    def init_camera_folders(self)-> dict:
        for root, _, files in os.walk(self.root_path):
            for file in files:
                if '.json' in file:
                    with open(os.path.join(root,file)) as args:
                        current_uuid = json.load(args)['origin']['uuid']
                        if current_uuid not in self.camera_uuids.keys():
                            chunk_path = root.split('/')
                            self.camera_uuids[current_uuid] = '/'.join(chunk_path[0:3])

    def search_by_time(self, start: str, end: str, uuid: str) -> dict:
        camera_path = self.get_path_by_uuid(uuid)
        start_time = self.format_date(start)
        end_time = self.format_date(end)
        path = camera_path + os.sep + start_time['day_path']
        for directory in sorted(os.listdir(path)):
            if start_time['hour'] <= int(directory) and int(directory) <= end_time['hour']:
                pattern = directory + '/*/*/*.json'
                filenames = glob.glob(os.path.join(path, pattern))
                for filename in sorted(filenames):
                    with open(filename) as args:
                        json_dict = json.load(args)
                        if json_dict['origin']['uuid'] == uuid:
                            args_dict = dict()
                            args_dict['path'] = filename[:-9]
                            #camera uuid
                            args_dict['uuid'] = json_dict['origin']['uuid']
                            args_dict['time'] = json_dict['time']
                            args_dict['location'] = json_dict['origin']['location']['place']
                            images = json_dict['measurements'][0]['waypoints']['best']['images']
                            args_dict['images'] = {
                                "vehicle": images['vehicle']['name'],
                                "scene": images['scene']['name'],
                                "thumb": images['thumb']['name'],
                                "plate": images['license-plates'][0]['name']
                            }
                            vehicle = json_dict['measurements'][0]['waypoints']['best']['vehicle']
                            if "type" in vehicle.keys():
                                args_dict['vehicle'] = {
                                    "class": vehicle['type']['info'][0]['class'],
                                    "make": vehicle['type']['make'],
                                    "model": vehicle['type']['model'],
                                    "weight": vehicle['type']['weight']
                                }
                            else:
                                args_dict['vehicle'] = {
                                    "class": "",
                                    "make": "",
                                    "model": "",
                                    "weight": ""
                                }
                            args_dict['vehicle']['plate-text'] = vehicle['license-plates'][0]['text']['ucode']
                            self.events.append(args_dict)
        print("count json events: ", len(self.events))

    def format_date(self, date: str) -> dict:
        datestr = date.split('.')[0]
        tmp = datetime.datetime.strptime(datestr, "%Y-%m-%dT%H:%M:%S")
        day_path = "{:4d}/{:02d}/{:02d}".format(tmp.year, tmp.month, tmp.day)
        dict_date = {
            "day_path": day_path,
            "hour": tmp.hour,
            "minute": tmp.minute
        }
        return dict_date

    def create_excel(self) -> int:
        os.curdir(self.root_path)
        if not os.path.exists("xlsx"):
            os.makedirs("xlsx")
        now = datetime.datetime.now()
        xsls_name = now.date() + '.xlsx'    
        workbook = xlsxwriter.Workbook(root_path + '/xlsx/' + xsls_name)
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
        for el in self.events:
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

    def get_path_by_uuid(self, uuid) -> str:
        return self.camera_uuids[uuid]
# for test



def counter_jsonfile(path: str) -> int:
    count = 0
    for _, _, files in os.walk(path):
        for file in files:
            if '.json' in file:
                count += 1

    return count

