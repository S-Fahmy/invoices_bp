import os
import pathlib

CERTS_LOCATION = os.getcwd() + '/invoices_files/certificates/'
pathlib.Path(CERTS_LOCATION).mkdir(parents=True, exist_ok=True) 

PDFS_LOCATION = os.getcwd() + '/invoices_files/pdfs/'
pathlib.Path(PDFS_LOCATION + '/logo').mkdir(parents=True, exist_ok=True) #logo image can be added in the logo folder as header_logo.png

HANDWRITTEN_SIGNATURES_FOLDER = os.getcwd() + '/invoices_files/handwritten_signatures/'
pathlib.Path(HANDWRITTEN_SIGNATURES_FOLDER).mkdir(exist_ok=True)