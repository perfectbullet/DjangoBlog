# coding:utf-8

import pdfkit
# pdfkit.from_string pdfkit.from_url pdfkit.from_file  -->html

# pdfkit.from_url('https://hao.360.com/', 'test1.pdf')
pdfkit.from_string('你好', 'test2.pdf')
