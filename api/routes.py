import config
import time
from threading import Thread
from api import app
from flask import jsonify
from flask import request
from flask import send_from_directory
import parser


# init parser
parse_path = config.Config.ARCHIVE_PATH
pars = parser.Parser(parse_path)
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
    return send_from_directory(
                                parse_path + '/xlsx', filename,
                                mimetype="application/vnd.openxmlformats-" + "officedocument.spreadsheetml.sheet",
                                as_attachment=True)
