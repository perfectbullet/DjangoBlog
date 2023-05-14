import re
import xlrd
from docx import Document
from docx import document, table
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.text.paragraph import Paragraph
from loguru import logger


def remove_tbcell_space(pg: str, space_char=r'\s|\.|,'):
    """
    去掉丧格中文本文字的空格
    :param space_char 去空格 获取其他
    :param pg:
    :return: str
    """
    ps_slice = re.split(space_char, pg)
    return ''.join(ps_slice)


def remove_pg_space(pg: str, space_char=r'\t|\s+'):
    """
    去掉段落文本中的空格和换行
    :param
    :space_char : 正则匹配
    :param pg:
    :return: str
    """
    ps_slice = re.split(space_char, pg)
    new_pg = ','.join(ps_slice)
    return new_pg


def read_table_obj(tb: table.Table):
    """
    读取docx.table对象内容，
    :param
    :tb
    :return:
    """
    tb_cels = []
    for row_idx, row in enumerate(tb.rows):
        for column_idx, cell in enumerate(row.cells):
            text = remove_tbcell_space(cell.text)
            if text:
                tb_cels.append(text)  # handle duplicate table data by set sam(
                cell.text = ''
    tb_context = ','.join(tb_cels)
    return tb_context


def read_xls_content(excel_path):
    """
    读取 excel 全文内容
    :return:
    """
    ws = xlrd.open_workbook(excel_path)
    sheets = ws.sheets()
    cell_values = []
    for sheet in sheets:
        for row in sheet.getrows():
            for cell in row:
                cell_text = '{}'.format(cell.value)
                cell_text = remove_tbcell_space(cell_text)
                if cell_text:
                    # 去掉空值
                    cell_values.append(cell_text)
    tb_context = ''.join(cell_values)
    return tb_context


def read_docx_content(file_path):
    """
    读docx文档内容，并返回
    param file_path:
    return:
    """

    logger.info('read file %s', file_path)
    parent = Document(file_path)
    paragraphs_and_tables = []

    if isinstance(parent, document.Document):
        parent_elm = parent.element.body
    elif isinstance(parent, table._Cell):
        parent_elm = parent._tc
    else:
        raise ValueError("this is a value error")
    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            pg = Paragraph(child, parent)
            pg_text = remove_pg_space(pg.text, space_char=r'\t|\s{4,}')
            if pg_text:
                paragraphs_and_tables.append(pg_text)
        elif isinstance(child, CT_Tbl):
            tb = table.Table(child, parent)
            tb_content = read_table_obj(tb)
            paragraphs_and_tables.append(tb_content)
        else:
            logger.info('no use element %s , child')
    full_text = ''.join(paragraphs_and_tables)
    return full_text


if __name__ == '__main__':
    demo_excel_path = r''
