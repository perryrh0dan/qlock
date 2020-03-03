from flask import Flask, request
from waitress import serve
import json

from src.config import Config

# Starting Flask webapp to configure word clock
def webApp():
    app = Flask(__name__)
    
    @app.route('/config', methods=['GET'])
    def getconfig():
        data = Config.instance().get()
        return Flask.response_class(
            response=json.dumps(data),
            status=200,
            mimetype='application/json'
        )

    @app.route('/config', methods=['POST'])
    def setconfig():
        data = request.get_json()
        Config.instance().set(data)
        return Flask.response_class(status=200)
    
    serve(app, host='0.0.0.0', port=5000)