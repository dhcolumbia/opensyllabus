#!/usr/bin/python

'''
https://stackoverflow.com/questions/582336/how-can-you-profile-a-python-script
(use with a second file option)
http://chairnerd.seatgeek.com/fuzzywuzzy-fuzzy-string-matching-in-python/
normal sort + token sort (seems less accurate)
'''

from extractors import miner, pdf2, pdfbox, textstream, xpdf
import os
import cProfile
import pstats
import StringIO


def miner_with_layout(pdf_file, txt_file):
    pdf = miner.Miner(pdf_file, txt_file)
    pdf.extract()

def miner_without_layout(pdf_file, txt_file):
    pdf = miner.Miner(pdf_file, txt_file, layout_analysis=False)
    pdf.extract()

def xpdf_with_layout(pdf_file, txt_file):
    pdf = xpdf.XPDF(pdf_file, txt_file)
    pdf.extract()

def xpdf_without_layout(pdf_file, txt_file):
    pdf = xpdf.XPDF(pdf_file, txt_file, layout=False)
    pdf.extract()

def textstream_default(pdf_file, txt_file):
    pdf = textstream.TextStream(pdf_file, txt_file)
    pdf.extract()

def pdf2_default(pdf_file, txt_file):
    pdf = pdf2.PDF2(pdf_file, txt_file)
    pdf.extract()

def pdfbox_default(pdf_file, txt_file):
    pdf = pdfbox.PDFBox(pdf_file, txt_file)
    pdf.extract()

def run_all(pdf_file, txt_file):
    miner_with_layout(pdf_file, txt_file)
    miner_without_layout(pdf_file, txt_file)
    xpdf_with_layout(pdf_file, txt_file)
    xpdf_without_layout(pdf_file, txt_file)
    textstream_default(pdf_file, txt_file)
    pdf2_default(pdf_file, txt_file)
    pdfbox_default(pdf_file, txt_file)

def time_all(pdf_file):
    methods = ['miner_with_layout', 'miner_without_layout', 'xpdf_with_layout', 
    'xpdf_without_layout', 'textstream_default', 'pdf2_default', 'pdfbox_default']

    base_name = os.path.basename(pdf_file)
    directory_name = os.path.dirname(pdf_file)

    # i.e. 'pride_and_prej' from './input/pride_and_prej/1.pdf'
    shorter_directory_name = os.path.basename(directory_name)
    # i.e. '1' from './input/pride_and_prej/1.pdf'
    file_base_name = os.path.splitext(base_name)[0]

    output = ''

    for method in methods:
        # build file path based on source text, input PDF, and method employed
        txt_file = './output/' + shorter_directory_name + '/' + method + '/' + file_base_name + '.txt'

        command = method + '(\'%s\', \'%s\')' % (pdf_file, txt_file)
        temp = 'statsfile'
        cProfile.run(command, temp)

        stream = StringIO.StringIO()
        stats = pstats.Stats(temp, stream=stream)
        stats.print_stats()
        stats.sort_stats('time')
        output = output + method + '\n-------------------------------------\n' + stream.getvalue()

    # clean up intermediary file
    os.remove('statsfile')

    # write results to log file
    with open('./stats/' + shorter_directory_name + '/' + file_base_name + '_speed_log.txt', "w") as log_file:
        log_file.write(output)

if __name__ == '__main__': 
    pdf_file = './input/pride_and_prej/1.pdf'
    time_all(pdf_file)