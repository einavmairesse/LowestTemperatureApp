from flask import jsonify
from flask_cors import CORS
from App import app, cache
from App.services import get_coldest_city_content, get_next_cache_flush

CORS(app)


@app.route('/get_lowest_temp', methods=['GET'])
@cache.cached(timeout=get_next_cache_flush())
def get_lowest_temp():
    coldest_city_content = get_coldest_city_content()
    return jsonify(coldest_city_content), 200


if __name__ == '__main__':
    app.run()
