# -*- coding: utf-8 -*-
import os
import time

from flask import (after_this_request, jsonify, render_template, request,
                   send_from_directory)

from config import Config
from parser_model.edge_parser import Parser
from parser_api import app
from threading import Thread

print("Initialization Parser....")
pars = Parser(Config.ARCHIVE_PATH, Config.CAMERAS_CONFIG_FILE)
# инициализация проходит через файл конфигурации
pars.init_cameras_config()
print("Parser initialized")


def is_one_day(start, end):
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
    try:
        events = pars.search_by_time(start, end, uuid)
    except BaseException as e:
        return str(e)
    if len(events) == 0:
        return "Events not found"
    id_file = pars.generate_file_id(uuid)
    if len(events) > Config.EXCEL_LIMIT_ROW:
        filename = pars.create_folder_excels(
            id_file, events, Config.EXCEL_LIMIT_ROW
        )
    else:
        filename = pars.create_excel(id_file, events)
    # delete file after 10 min
    filepath = os.path.join(pars.root_path, filename)
    t = Thread(
        target=pars.delete_after_time, args=(filepath, Config.EXCEL_TIME_LIVE))
    t.start()
    return jsonify({'id_file': filename, 'result': events})


"""
download file by uuid(id_file)
uuid = filename + extension
"""
@app.route('/api/excel', methods=['GET'])
def download_file():
    uuid = request.args.get('uuid')
    if not os.path.exists(os.path.join(pars.root_path, uuid)):
        return jsonify({'message': 'File is not found'})

    @after_this_request
    def remove_file(respone):
        os.remove(os.path.join(pars.root_path, uuid))
        return respone
    return send_from_directory(
                                    pars.root_path, uuid,
                                    attachment_filename="Oтчет_" + time.
                                    strftime("%Y_%m_%d") + "." + uuid.
                                    split('.')[1],
                                    as_attachment=True)


@app.route('/api/info', methods=['GET'])
def get_info():
    return render_template("info.html")

# для получения списка камер которые хранятся в архиве
@app.route('/api/cameras', methods=['GET'])
def get_list_cameras():
    return jsonify({'cameras': pars.camera_uuids})
