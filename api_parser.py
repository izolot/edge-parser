import parser
from flask import Flask
from flask import jsonify
from flask import request
from flask import send_file
from flask_autoindex import AutoIndex

ROOT_PATH = "mnt"

app = Flask(__name__)
AutoIndex(app, browse_root=ROOT_PATH)
pars = parser.Parser(ROOT_PATH)
pars.init_camera_folders()

@app.route('/events', methods = ['GET'])
def get_events_by_time():
    start = request.args.get('start')
    end = request.args.get('end')
    uuid = request.args.get('uuid')
    return jsonify({'result': pars.search_by_time(start, end, uuid)})

@app.route('/excel', methods = ['GET'])
def get_excel():
    return send_file(pars.create_excel())




if __name__ == '__main__':
    app.run(debug=True)

