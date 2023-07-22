"""
@FileName：xml_utils.py
@Description：
@Author：zhoujing
@contact：121531845@qq.com
@Time：2023/7/18 22:08
@Department：红石扩大小区
@Website：www.zhoujing.com
@Copyright：©2019-2023 xxx信息科技有限公司
"""
import xml.etree.ElementTree as ET

"""
    ElementTree.write()       将构建的XML文档写入（更新）文件。
    Element.set(key, value)   添加和修改属性
    Element.text = ''         直接改变字段内容
    Element.remove(Element)   删除Element节点
    Element.append(Element)   为当前的Elment对象添加子对象
    ET.SubElement(Element,tag)创建子节点 
"""


#  增加自动缩进换行
def indent(elem, level=0):
    i = "" + level * " "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + " "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


if __name__ == '__main__':
    # ------------新增XML----------

    # 创建根节点
    a = ET.Element("student")
    # 创建子节点，并添加属性
    b = ET.SubElement(a, "name")
    b.attrib = {"NO.": "001"}
    # 添加数据
    b.text = "张三"
    # 创建elementtree对象，写文件
    indent(a, 0)
    tree = ET.ElementTree(a)
    tree.write("writeXml.xml", encoding="utf-8")

    # ----------编辑XML--------
    # 读取待修改文件
    updateTree = ET.parse("writeXml.xml")
    other_root = ET.parse("writeXml2.xml").getroot()
    root = updateTree.getroot()
    for ch in other_root:
        # newnode = ET.Element("name")
        root.append(ch)


    # --新增--

    # 创建新节点并添加为root的子节点
    # newnode = ET.Element("name")
    # newnode.attrib = {"NO.": "003"}
    # newnode.text = "张三水"
    # root.append(newnode)

    # ---修改---
    #
    # sub1 = root.findall("name")[1]
    # # --修改节点的属性
    # sub1.set("NO.", "100")
    # # --修改节点内文本
    # sub1.text = "陈真"

    # ----删除---
    #
    # # --删除标签内文本
    # sub1.text = ""
    # # --删除标签的属性
    # del sub1.attrib["NO."]
    # # --删除一个节点
    # root.remove(sub1)

    # 写回原文件
    indent(root, 0)
    updateTree.write("writeXml.xml", encoding="utf-8", xml_declaration=True)
