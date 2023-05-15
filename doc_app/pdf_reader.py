import itertools
import re
import pdfplumber


def remove_tbcell_space(pg: str, space_char=r'\s|\.|,'):
    """
    去掉表格中文本文字的空格
    :param space_char: 去空格 获取其他
    :param pg:
    :return: str
    """
    ps_slice = re.split(space_char, pg)
    return ''.join(ps_slice)


def remove_pg_space(pg: str, space_char=r'\s|\.|,'):
    """
    去掉段落文本中的空格和换行
    :param space_char: 去空格 获取 其他
    :param pg:
    :return: str
    """
    ps_slice = re.split(space_char, pg)
    new_pg = ''.join(ps_slice)
    return new_pg


def str_Nempt(s):
    """
    去掉列表中空值字符串和None
    :param s:
    :return:
    """
    return list(filter(lambda ss: ss and ss.strip(), s))


def read_table_obj(tb):
    """
    读取pdf表格中对象内容
    :param tb:
    :return: pdf
    """
    # Alternative chain() constructor taking a single iterabl
    table_cells = list(itertools.chain.from_iterable(tb))
    table_cells = str_Nempt(table_cells)
    table_cells = [remove_tbcell_space(cell) for cell in table_cells]
    return ', '.join(table_cells)


def read_pdf_content(pdf_file_path):
    """
    读取 pdf 文档内容，返回表格和文本
    param file_path:
    nchunchenc
    :return: full_text
    """

    paragraphs_and_tables = []
    with pdfplumber.open(pdf_file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text is not None:
                page.text = '{}'.format(page_text)
                page_text = remove_pg_space(page_text, space_char=r'\t|\s{4, }')
                paragraphs_and_tables.append(page_text)
            tb_obj = page.extract_table()
            if tb_obj:
                tb_context = read_table_obj(tb_obj)
                paragraphs_and_tables.append(tb_context)
    full_text = ','.join(paragraphs_and_tables)
    return full_text


if __name__ == '__main__':
    demo_pdf_path = r'C:/Users/Administrator/Desktop/阿里巴巴 Java 开发手册.pdf'

    result = read_pdf_content(demo_pdf_path)
    print(result)
