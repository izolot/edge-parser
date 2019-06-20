import config
from app import app
from flask import jsonify
from flask import request
from flask import send_from_directory
from . import parser


# init parser
parse_path = config.Config.PARSE_PATH
pars = parser.Parser(parse_path)
pars.init_camera_folders()
events = []


@app.route('/api/events', methods=['GET'])
def get_events_by_time():
    start = request.args.get('start')
    end = request.args.get('end')
    uuid = request.args.get('uuid')
    filename = pars.gen_name_by_time(start,end)
    events = pars.search_by_time(start, end, uuid)
    pars.create_excel(filename, events)
    return jsonify({'result': events})


@app.route('/api/excel', methods=['GET'])
def download_file(filename):
    return send_from_directory(
                                parse_path + '/xlsx', filename, 
                                mimetype="application/vnd.openxmlformats-" + "officedocument.spreadsheetml.sheet",
                                as_attachment=True)
