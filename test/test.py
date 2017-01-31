from restful import Resource

class Test(Resource):
    def get(self):
        try:
            return "Server is working!"
        except Exception as e:
            return str(e)
