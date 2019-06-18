from app import app
from flask import jsonify
from flask import request
from flask import send_from_directory
import parser, config

#init parser
parse_path = config.Config.PARSE_PATH
pars = parser.Parser(parse_path)
pars.init_camera_folders()



@app.route('/events', methods = ['GET'])
def get_events_by_time():
    start = request.args.get('start')
    end = request.args.get('end')
    uuid = request.args.get('uuid')
    pars.search_by_time(start, end, uuid)
    return jsonify({'result': pars.events})

@app.route('/excel', methods = ['GET'])
def download_file():
    filename = pars.create_excel()
    return send_from_directory(parse_path + '/xlsx', filename, 
                                mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", 
                                as_attachment=True)




