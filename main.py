from flask import Flask
from flask.helpers import url_for
from werkzeug.utils import redirect
from invoice_generator.routes import invoice_generator
from digital_signature.routes import digital_signature
from self_signed_certs.routes import self_signed_certificate

app = Flask(__name__,  static_folder=None)
app.config.from_object('config')
app.register_blueprint(invoice_generator, url_prefix='/invoice')
app.register_blueprint(digital_signature, url_prefix='/signature')
app.register_blueprint(self_signed_certificate, url_prefix='/selfsignedcert')



'''
redirects to the main page in the invoice_generator blueprint
'''
@app.route('/')
def redirection():
    return redirect(url_for('invoice_generator.main'))

if __name__ == '__main__':
    app.run(debug=True)

