


class Jwt():

    def jwtsignature(self ,contact):

        encoded_jwt = jwt.encode({'contact': contact}, 'secret', algorithm='HS256')
        response ={'token' :encoded_jwt}
        return response