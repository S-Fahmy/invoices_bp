import os
import base64
from flask import  Blueprint, render_template, request, jsonify, current_app
from .controllers import pdfBuilderController
from digital_signature.controllers import pdfDigitalSignatureController

invoice_generator = Blueprint('invoice_generator', __name__, template_folder='templates', static_folder='static')



@invoice_generator.route('/')
def main():
    return render_template('index.html')



@invoice_generator.route('/pdf/generate', methods=["POST"])
def create_a_pdf():

    try:
        data = request.json

        #TODO: more customized/detailed validations...
        if data is None or data.get('invoiceData' , None) is None or data.get('pdfName', None) is None or data['pdfName'] == '':
            print('data incomplete')
            return jsonify({'success': False, 'message': 'data incorrect'}), 500

        # print(data.get('invoiceData'))
        pdf_name = data['pdfName']
        invoice_data = data['invoiceData']

        pdfs_folder = current_app.config.get('PDFS_LOCATION')
        if not os.path.exists(pdfs_folder):
                os.makedirs(pdfs_folder)

        sig_position = pdfBuilderController.build_pdf(pdf_name, invoice_data, pdfs_folder)
        #build the pdf file first
        if sig_position:
            #sign it
            success = pdfDigitalSignatureController.sign_pdf_file(pdf_name + '.pdf', current_app.config.get('CERTS_LOCATION'), current_app.config.get('PDFS_LOCATION'), current_app.config.get('HANDWRITTEN_SIGNATURES_FOLDER') + "/signature.png", sig_position)

            if not success:
                return jsonify({'success': False, 'message': 'error during signing file'}), 500
        
        return jsonify({'success': True}), 200

    except Exception as e:
        print('something happened in create_a_pdf', e)
        return jsonify({'success': False, 'message': 'error'}), 500


'''
saves the handwritten signature bytes to png
currently the signatures files are limited to one because the file name is hardcoded to signature.png so new ones will replace existing ones.
'''
@invoice_generator.route('/signature/save', methods = ['POST'])
def save_signature():
    try:
        signatureImgData =  request.json.split(',')[1]
        
        with open(current_app.config.get('HANDWRITTEN_SIGNATURES_FOLDER') + "/signature.png", "wb") as image:
            image.write(base64.b64decode(signatureImgData))
        
        return jsonify({'success': True}), 200

    except Exception as e:

        print('something happened in save_signature', e)
        return jsonify({'valid': False, 'message': 'error'}), 500



'''
loads up the signature image and return as bytes to the frontend canva object
'''
@invoice_generator.route('/signature/load', methods = ['GET'])
def get_existing_signature():
    if not os.path.exists(current_app.config.get('HANDWRITTEN_SIGNATURES_FOLDER') + '/signature.png'):
        print('no existing sig images found')
        return jsonify({'success': False}), 200


    img_data = ""
    with open(current_app.config.get('HANDWRITTEN_SIGNATURES_FOLDER') + "/signature.png", "rb") as image:
        data = base64.b64encode(image.read())
        img_data = data.decode()

    return jsonify({'success': True, 'img_data': img_data}), 200