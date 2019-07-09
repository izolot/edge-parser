import datetime
import glob
import json
import math
import os
import shutil
import time
import xlsxwriter


class Parser(object):
    
    def __init__(self, path) -> None:
        self.root_path = path
        self.camera_uuids = {}


    def init_cameras_config(self) -> None:
        config_path = os.path.join(self.root_path, 'cameras.config')
        with open(config_path , 'r') as config:
            self.camera_uuids = json.load(config)['cameras']
        print("Init cameras - ", self.camera_uuids)

    def search_by_time(self, start: str, end: str, uuid: str) -> dict:
        if len(uuid) < 36:
            raise BaseException("Error  -> Bad UUID")
        camera_path = self.get_path_by_uuid(uuid)
        if camera_path is None:
            raise BaseException("Error  -> Camera UUID is not found. Please add camera to archive_path/cameras.config")
        start_time = self.format_date(start)
        end_time = self.format_date(end)
        events = []
        #check period for compare by hour or by minute
        if start_time['hour'] != end_time['hour']:
            path = camera_path + os.sep + start_time['day_path']
            start = start_time['hour']
            end = end_time['hour']
            path_pattern = '/*/*/*.json'
        else:
            path = camera_path + os.sep + start_time['day_path'] + os.sep + str(start_time['hour'])
            start = start_time['minute']
            end = end_time['minute'] + 1
            path_pattern = '/*/*.json'
        for directory in sorted(os.listdir(path)):
            if start <= int(directory) and int(directory) < end:
                pattern = directory + path_pattern
                filenames = glob.glob(os.path.join(path, pattern))
                for filename in sorted(filenames):
                    with open(filename) as args:
                        json_dict = json.load(args)
                        if json_dict['origin']['uuid'] == uuid:
                            args_dict = self.parse_json_args(filename, json_dict)
                            events.append(args_dict)
        print("Json elements: - ", len(events))
        return events

    def parse_json_args(self, filename, json_dict):
        args_dict = dict()
        args_dict['path'] = filename[:-9]
        #camera uuid
        args_dict['uuid'] = json_dict['origin']['uuid']
        time = datetime.datetime.strptime(json_dict['time'].split('.')[0], "%Y-%m-%dT%H:%M:%S")
        text_time = time.strftime("%Y.%m.%d %H:%M:%S")
        args_dict['time'] = text_time
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
        return args_dict

    #pattern 2019-06-21T01:00:00
    def format_date(self, date: str) -> dict:
        tmp = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
        day_path = "{:4d}/{:02d}/{:02d}".format(tmp.year, tmp.month, tmp.day)
        dict_date = {
            "day_path": day_path,
            "year":tmp.year,
            "month":tmp.month,
            "day": tmp.day,
            "hour": tmp.hour,
            "minute": tmp.minute,
        }
        return dict_date

    
    def generate_file_id(self, uuid):
        # gen id and remove 0x
        now = hex(int(time.time()))[2:]
        uuid = uuid.replace('-','')
        return str(now) + uuid


    def create_excel(self, filename, data) -> str:
        xlsx_name = filename + '.xlsx'
        workbook = xlsxwriter.Workbook(os.path.join(self.root_path, xlsx_name))
        worksheet = workbook.add_worksheet()
        excel_format = workbook.add_format(
            {'align': 'center', 'valign': 'vcenter', 'text_wrap': True })
        title_format = workbook.add_format({'bg_color': '396cb4', 'align': 'center', 'valign': 'vcenter',
                                            'border_color': 'black', 'top':1,
                                             'bottom':1, 'left':1, 'right':1 })
        worksheet.set_column('A:F', 31)
        worksheet.set_row(0, 40, excel_format)
        worksheet.write('A1', 'Фото машины', title_format)
        worksheet.write('B1', 'Фото ГРЗ', title_format)
        worksheet.write('C1', 'ID Камеры', title_format)
        worksheet.write('D1', 'Дата и время события \n гггг.мм.дд чч:мм:сс', title_format)
        worksheet.write('E1', 'Распознанный ГРЗ', title_format)
        worksheet.write('F1', 'Тип авто', title_format)

        row = 1
        for el in data:
            worksheet.set_row(row, 170, excel_format)
            worksheet.insert_image(
                row, 0, os.path.join(el['path'], el['images']['thumb']),
                {'object_position': 3})
            worksheet.insert_image(
                row, 1, os.path.join(
                    el['path'], el['images']['plate']),
                {'object_position': 3, 'x_offset': 20, 'y_offset': 20,
                    'x_scale': 1.5, 'y_scale': 1.5})
            worksheet.write(row, 2, el['location'])
            worksheet.write(row, 3, el['time'])
            worksheet.write(row, 4, el['vehicle']['plate-text'])
            worksheet.write(row, 5, el['vehicle']['make'] + '\n' + el['vehicle']['model'])
            row += 1
        workbook.close()
        return xlsx_name


    def create_folder_excels(self, foldername, data, num_rows) -> str:
        folder_path = os.path.join(self.root_path, foldername) + os.sep
        os.mkdir(folder_path)
        # how many files create with limit rows
        num_files =  round(len(data)//num_rows) + 1
        for i in range(0, num_files):
            if i == num_files - 1:
                end = len(data)
            else:
                end = num_rows * (i + 1)
            begin = num_rows * i
            self.create_excel(folder_path  + "part_" + str(i + 1), data[begin:end])
        shutil.make_archive(folder_path, "zip", folder_path)
        shutil.rmtree(folder_path, ignore_errors=True)
        return foldername + ".zip"


    def get_path_by_uuid(self, uuid) -> str:
        if uuid in self.camera_uuids:
            return self.camera_uuids[uuid]['archive_path']
        else:
            self.init_cameras_config()
            if uuid in self.camera_uuids:
                return self.camera_uuids[uuid]['archive_path']
            else:
                return None
