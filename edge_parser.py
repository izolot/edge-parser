import json
import os
import xlsxwriter
import glob
import datetime



class Parser(object): 
    
    def __init__(self, root_path: str):
        self.root_path = root_path
        self.camera_uuids = {}
        

    def init_camera_folders(self):
        for root, _, files in os.walk(self.root_path):
            for file in files:
                if '.json' in file:
                    with open(os.path.join(root, file)) as args:
                        current_uuid = json.load(args)['origin']['uuid']
                        if current_uuid not in self.camera_uuids.keys():
                            chunk_path = root.split('/')
                            # save path without year/mounth/day/hour/minute/uuid [6]
                            self.camera_uuids[current_uuid] = '/'.join(
                                chunk_path[0:-6])
        print(self.camera_uuids)

    def search_by_time(self, start: str, end: str, uuid: str) -> dict:
        if len(uuid) < 36:
            return "Error  -> Bad UUID"
        camera_path = self.get_path_by_uuid(uuid)
        start_time = self.format_date(start)
        end_time = self.format_date(end)
        if camera_path is None:
            return "Error  -> Archive by UUID is not found"
        events = []    
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
                            time = datetime.datetime.strptime(json_dict['time'], "%Y-%m-%dT%H:%M:%S.%f%z")
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
                            events.append(args_dict)
        print("Json elements: - ", len(events))
        return events

    #2019-06-21T01:00:00
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

    def create_excel(self, filename, data):
        xlsx_path = os.path.join(self.root_path, "xlsx")
        if not os.path.exists(xlsx_path):
            os.makedirs(xlsx_path)
        xlsx_name = filename + '.xlsx'
        workbook = xlsxwriter.Workbook(os.path.join(xlsx_path, xlsx_name))
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

    def get_path_by_uuid(self, uuid) -> str:
        if uuid in self.camera_uuids:
            return self.camera_uuids[uuid]
        else:
            self.init_camera_folders()
            if uuid in self.camera_uuids:
                return self.camera_uuids[uuid]
            else:
                return None



