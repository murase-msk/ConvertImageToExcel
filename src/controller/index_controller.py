# from flask.json import jsonify
from flask.views import MethodView
from flask import render_template


class IndexController(MethodView):
    # def get(self):
    #     return jsonify({"data": "index"})

    # def post(self):
    #     return jsonify({'response': 'ok'})

    def indexAction():
        return render_template('index.html', title='Convert PDF to Excel')

    def drawDetectedTextPageAction():
        return render_template('drawDetectedTextPage.html', title='Convert PDF to Excel')
