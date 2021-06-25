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
        return render_template('drawDetectedTextPage.html', title='Draw Detected Text')

    def getLabelPageAction():
        return render_template('getLabelPage.html', title='Get Label')

    def detectTextPageAction():
        return render_template('detectTextPage.html', title='Detect Text')

    def getImagePositionPageAction():
        return render_template('getImagePositionPage.html', title='Get Image Position')

    def textDetectApiPageAction():
        return render_template('textDetectApiPage.html', title='Detect Text API')
