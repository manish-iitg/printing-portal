# pip install PyPDF2

import os
from PyPDF2 import pdfFileMerger, pdfFileReader, pdfFileWriter

# code to merge multiple pdf files into one
source_dir = os.getcwd()

merger = pdfFileMerger()

for item in os.listdir(source_dir):
    if item.endswith('pdf'):
        merger.append(item)

merger.write('complete.pdf')
merger.close()

# code to extract specific pages from a PDF and save as a separate PDF
pdf_file_path = 'dir/<pdf_name>.pdf'
file_base_name = pdf_file_path.replace('.pdf', '')

pdf = pdfFileReader(pdf_file_path)

pages = [0, 2, 4] # pages 1,3,5
pdfWriter = pdfFileWriter()

for page_num in pages:
    pdfWriter.addPage(pdf.getPage(page_num))

with open('{0}_subset.pdf'.format(file_base_name), 'wb') as f:
    f.close()