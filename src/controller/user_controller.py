from flask.views import MethodView
from flask import request
from flask import render_template
# from flask.json import jsonify
# from flask import current_app


class UserController(MethodView):
    # def get(self, user_id):
    #     # request.args.get("")
    #     return jsonify({"data": user_id})

    # def post(self):
    #     return jsonify({'response': 'ok'})

    def userAction(user_id: str):
        if user_id:
            userId: int = int(user_id)
        name1: str = request.args.get('name1', '')
        return render_template(
            'user.html',
            title='test user title',
            name=name1,
            userid=userId)

    def configAction():
        # print(current_app.config["ENV_TEST"])
        # envVal: str = conf  # os.environ["DEBUG"]
        # return jsonify({"data": current_app.config["ENV_TEST"]})
        # return jsonify({'config': envVal})
        return ""
