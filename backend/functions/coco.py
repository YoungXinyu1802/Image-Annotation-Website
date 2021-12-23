import json
data = [ { 'a' : 1, 'b' : 2, 'c' : 3, 'd' : 4, 'e' : 5 } ]

def toCreateML(filename, xmin, ymin, xmax, ymax, tags):
    res = []
    image_name = filename
    annotations = []
    for i in range(len(xmin)):
        label = tags[i]
        x = (xmin[i] + xmax[i]) / 2
        y = (ymin[i] + ymax[i]) / 2
        width = xmax[i] - xmin[i]
        height = ymax[i] - ymin[i]
        coordinates = dict(zip(['x', 'y', 'width', 'height'], [x, y, width, height]))
        # coordinates = json.dumps(coordinates)
        anno = dict(zip(['label', 'coordinates'], [label, coordinates]))
        annotations.append(anno)
    createML = dict(zip(['image', 'annotations'], [image_name, annotations]))
    res = '[' + json.dumps(createML) + ']'
    return res

image_name = '00731.jpg'
xmin = [1, 2]
ymin =[1,2]
xmax = [2, 3]
ymax = [3, 4]
tags = ['t', 'w']
res = toCreateML(image_name, xmin, ymin, xmax, ymax, tags)
f = open("foo.json", "w")
f.write(res)
print(res)