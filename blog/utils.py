class ApiResponse():

    STATUS_ERROR = 'error'
    STATUS_SERVER_ERROR = 'server_error'
    ALIAS_REDIRECT = 'redirect'

    status = 'success'
    alias = ''
    message = ''
    data = None

    def redirect(self, uri):
        self.alias = self.ALIAS_REDIRECT
        self.data = uri

    def error(self, msg, alias=''):
        self.status = self.STATUS_ERROR
        self.alias = alias
        self.message = msg

    def server_error(self, exception):
        self.status = self.STATUS_SERVER_ERROR
        self.message = str(exception)

    def make_resp(self):
        return {
            'status': self.status,
            'alias': self.alias,
            'message': self.message,
            'data': self.data,
        }

    def get_resp_data(self):

        return self.make_resp()



def string_sanitize(string):
    for char in [
        '"', '<', '>', ':', ';', 
        '=', '$', '#', '%', '&', 
        '*', '~', '`', '/', '|', 
        '\\', '{', '}', '[', ']',
    ]:
        if char in string:
            string = string.replace(char, '')
    return string