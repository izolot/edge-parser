import parser
import datetime
from flask import Flask
from flask import jsonify
from flask import request
from flask import send_file
from flask_autoindex import AutoIndex

app = Flask(__name__)
AutoIndex(app, browse_root='mnt')


@app.route('/events', methods = ['GET'])
def get_events_by_time():
    start = request.args.get('start')
    end = request.args.get('end')
    pars = parser.Parser('mnt/edge1/local_arch/')
    return jsonify({'result': pars.search_by_time(start, end)})


if __name__ == '__main__':
    app.run(debug=True)

