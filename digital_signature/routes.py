
from .controllers import pdfDigitalSignatureController 
from flask import  Blueprint, render_template, request, jsonify, current_app

digital_signature = Blueprint('digital_signature', __name__, static_folder='static')

'''
takes pdf name as a parameter, and calls the signature validation function on it
currently just return valid true or false
'''
@digital_signature.route('/validate/<string:pdf_name>', methods = ['GET'])
def validate_a_pdf(pdf_name):
    try:

        valid = pdfDigitalSignatureController.validated_pdf_file(pdf_name, current_app.config.get('CERTS_LOCATION'), current_app.config.get('PDFS_LOCATION'))
        if valid is False:
            
            return jsonify({'valid': False}), 200

        return jsonify({'valid': True}), 200

    except Exception as e:

        print('something happened in validate_a_pdf', e)
        return jsonify({'valid': False, 'message': 'error'}), 500
