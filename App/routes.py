from flask import jsonify
from flask_cors import CORS
from App import app, config
from App.services import get_coldest_city_context


CORS(app)


@app.route('/get_lowest_temp', methods=['GET'])
def get_lowest_temp():
    cities = config.cities
    coldest_city_context = get_coldest_city_context()
    return jsonify(coldest_city_context), 200


if __name__ == '__main__':
    app.run()
