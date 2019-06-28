import config
import time
import os
from edge_parser import Parser
from threading import Thread
from api import app
from flask import jsonify
from flask import request
from flask import send_from_directory
from flask import render_template
from flask import after_this_request



# init parser
parse_path = config.Config.ARCHIVE_PATH
pars = Parser(parse_path)
print("Create instance")
pars.init_camera_folders()
events = []

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
    events = pars.search_by_time(start, end, uuid)
    id_file = pars.generate_file_id(uuid)
    pars.create_excel(id_file, events)
    # при реализации в несколько тредов файл не всегда успевает записаться вовремя
    # t = Thread(target = pars.create_excel, args = (id_file, events))
    # t.start()
    return jsonify({'id_file': id_file ,'result': events})

"""
download file by uuid(id_file) 
"""
@app.route('/api/excel', methods=['GET'])
def download_file():
    uuid = request.args.get('uuid')
    filename = uuid + '.xlsx'
    filepath = parse_path + '/xlsx'
    if not os.path.exists(os.path.join(filepath, filename)):
        return jsonify({'message': 'File is not found'})
    @after_this_request
    def remove_file(response):
        os.remove(os.path.join(filepath, filename))
        return response
    return send_from_directory(
                                    filepath, filename,
                                    mimetype="application/vnd.openxmlformats-" + "officedocument.spreadsheetml.sheet",
                                    attachment_filename="Oтчет_"+ time.strftime("%Y_%m_%d") + ".xlsx",
                                    as_attachment=True)


@app.route('/api/info', methods = ['GET'])
def get_info():
    return render_template("info.html")

# для получения списка камер которые хранятся в архиве
@app.route('/api/cameras', methods = ['GET'])
def get_list_cameras():
    return jsonify({'cameras': pars.camera_uuids})
