#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/7/16 下午3:19
@Author  : Bill Fang
@File    : RemoveBg.py
@Desc    : 
"""
from PIL import Image
import os
from rembg import remove,new_session

input_img = "E:\\img_test\\input"
output_img = "E:\\img_test\\output"


#获取目录下全部图片文件
def getFileList(file_path):
    imgs_path = []
    for filename in os.listdir(file_path):
        img_path = os.path.join(file_path, filename).lower()
        imgs_path.append(img_path)

    return imgs_path


#app = Flask(__name__)


"""@app.route('/remove_img_bg')
def hello_world():
    print(request.args.get('dir1'))
    print(request.args.get('dir2'))
    return 'Hello, World!'"""


"""if __name__ == '__main__':
    app.run()"""


if __name__=='__main__':

    # 待处理的图片路径
    input_path = 'E:\\img_test\\input\\1.jpg'
    # 处理后存储的图片路径
    output_path = 'E:\\img_test\\output\\1.png'

    # 加载自定义模型
    model_path = "E:\\img_test\\u2net.onnx"

    session = new_session(model_name='u2net_custom', model_path=model_path)
    with open(input_path, 'rb') as i:
        with open(output_path, 'wb') as o:
            input = i.read()
            output_image = remove(input, session=session)
            o.write(output_image)
    """imgs_path = getFileList(input_img)
    for img_path in imgs_path:
        img_name = os.path.basename(img_path)
        if img_name.endswith('.jpg') or img_name.endswith('.jpeg'):
            #解决jpg图片无Alpha通道
            input = Image.open(img_path).convert('RGB')
        else:
            input = Image.open(img_path)
        #rembg去除图片背景
        output = remove(input)
        # 将去除背景后的图片背景设置为白色
        background = Image.new('RGBA', output.size, (255, 255, 255, 255))
        background.paste(output, mask=output)
        out_path = os.path.join(output_img, img_name.replace('.jpg', '.png').replace('.jpeg','.png'))

        background.save(out_path)
        input.close()
        output.close()
        background.close()"""

