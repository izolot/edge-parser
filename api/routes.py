
import os
import time
from threading import Thread

from flask import (after_this_request, jsonify, render_template, request,
                   send_from_directory)

from api import app
from config import Config
from edge_parser import Parser


def is_one_day(start,end):
    first_date = start.split('T')[0]
    second_date = end.split('T')[0]
    return first_date == second_date


@app.route('/api/events', methods=['GET'])
def get_events_by_time():
    start = request.args.get('start')
    end = request.args.get('end')
    uuid = request.args.get('uuid')
    if not is_one_day(start, end):
        return "Error ->  Please choose only one day"
    # выбор сделан в пользу однопоточного решения
    pars = Parser()
    events = pars.search_by_time(start, end, uuid)
    id_file = pars.generate_file_id(uuid)
    if len(events) > Config.EXCEL_LIMIT_ROW:
        foldername = pars.create_folder_excels(
            id_file, events, Config.EXCEL_LIMIT_ROW
        )
        return jsonify({'id_file': foldername ,'result': events})
    else:
        filename = pars.create_excel(id_file, events)
        return jsonify({'id_file': filename ,'result': events})

"""
download file by uuid(id_file)
uuid = filename + extension 
"""
@app.route('/api/excel', methods=['GET'])
def download_file():
    uuid = request.args.get('uuid')
    if not os.path.exists(os.path.join(parse_path, uuid)):
        return jsonify({'message': 'File is not found'})
    @after_this_request
    def remove_file(respone):
        os.remove(os.path.join(parse_path, uuid))
        return respone
    return send_from_directory(
                                    parse_path, uuid,
                                    attachment_filename="Oтчет_"+ time.strftime("%Y_%m_%d") + "." + uuid.split('.')[1],
                                    as_attachment=True)


@app.route('/api/info', methods = ['GET'])
def get_info():
    return render_template("info.html")

# для получения списка камер которые хранятся в архиве
@app.route('/api/cameras', methods = ['GET'])
def get_list_cameras():
    return jsonify({'cameras': pars.camera_uuids})
