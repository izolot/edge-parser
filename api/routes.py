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



# init parser
parse_path = config.Config.ARCHIVE_PATH
pars = Parser(parse_path)
print("Create instance")
pars.init_camera_folders()
events = []


@app.route('/api/events', methods=['GET'])
def get_events_by_time():
    start = request.args.get('start')
    end = request.args.get('end')
    uuid = request.args.get('uuid')
    events = pars.search_by_time(start, end, uuid)
    t = Thread(target = pars.create_excel, args = (uuid, events))
    t.start()
    return jsonify({'result': events})


@app.route('/api/excel', methods=['GET'])
def download_file():
    uuid = request.args.get('uuid')
    filename = uuid + '.xlsx'
    filepath = parse_path + '/xlsx'
    if not os.path.exists(os.path.join(filepath, filename)):
        return jsonify({'message': 'File is not found'})

    return send_from_directory(
                                    filepath, filename,
                                    mimetype="application/vnd.openxmlformats-" + "officedocument.spreadsheetml.sheet",
                                    as_attachment=True)



@app.route('/info', methods = ['GET'])
def get_info():
    return render_template("info.html")
