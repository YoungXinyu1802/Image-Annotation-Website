from lxml import etree

# 创建一个annotion节点
root = etree.Element('annotion')
# 创建一个子节点folder，一定要指定父节点
child1 = etree.SubElement(root, 'folder')
child1.text = 'VOCtype'

child2 = etree.SubElement(root, 'filename')
child2.text = '000001.jpg'

child3 = etree.SubElement(root, 'source')

child31 = etree.SubElement(child3, 'database')
child31.text = 'VOC'

child4 = etree.SubElement(root, 'size')

child41 = etree.SubElement(child4, 'width')
child41.text = '458'

child42 = etree.SubElement(child4, 'height')
child42.text = '45'

child5 = etree.SubElement(root, 'segmented')
child5.text = '0'
# 自定义数据集
objectlist = []
for i in range(0, 3):
    dic = dict(xmin=1, ymin=2, xmax=3, ymax=4)
    objectlist.append(dic)
print(objectlist)


for i in objectlist:
    child6 = etree.SubElement(root, 'object')

    child61 = etree.SubElement(child6, 'name')
    child61.text = 'face'

    child62 = etree.SubElement(child6, 'pose')
    child62.text = 'Unspecified'

    child63 = etree.SubElement(child6, 'truncated')
    child63.text = '0'

    child64 = etree.SubElement(child6, 'difficult')
    child64.text = '0'

    child65 = etree.SubElement(child6, 'bndbox')

    child651 = etree.SubElement(child65, 'xmin')
    child651.text = str(i['xmin'])

    child652 = etree.SubElement(child65, 'ymin')
    child652.text = str(i['ymin'])

    child653 = etree.SubElement(child65, 'xmax')
    child653.text = str(i['xmax'])

    child654 = etree.SubElement(child65, 'ymax')
    child654.text = str(i['ymax'])

tree = etree.ElementTree(root)
tree.write('pascal.xml', pretty_print=True)