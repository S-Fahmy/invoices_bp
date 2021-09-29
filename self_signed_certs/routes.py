from flask import Blueprint, render_template, request, jsonify, current_app
from .controllers.selfSignCertificate import selfSignedCert
import os

self_signed_certificate = Blueprint('self_signed_certificate', __name__)


@self_signed_certificate.route('/create')
def create_pems_if_not_found():
    try:
        certs_folder_path = current_app.config.get('CERTS_LOCATION')

        if not os.path.exists(certs_folder_path + '/pdfapp.key.pem') or not os.path.exists(certs_folder_path + '/pdfapp.cert.pem'):
            print('pems missing, have to recreate')
            status = selfSignedCert(cert_name=certs_folder_path + '/pdfapp.cert.pem',
                                    key_name=certs_folder_path + '/pdfapp.key.pem').create()
            return jsonify({"success": True}), 200 if status else jsonify({"success": False}), 500

        print('pems found')
        return jsonify({"success": True}), 200

    except Exception as e:
        print('something happened in self_signed_certificate create()', e)
        return jsonify({"success": False, "message": e}), 500
