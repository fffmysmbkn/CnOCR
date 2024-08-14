# coding: utf-8
# Copyright (C) 2022, [Breezedeus](https://github.com/breezedeus).
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

# 安装Flask： pip install flask

# 启动服务： FLASK_APP=scripts/flask-serve.py flask run
# 调用服务： curl -F image=@docs/examples/huochepiao.jpeg http://127.0.0.1:8555/ocr

import io
from copy import deepcopy
from typing import List, Dict, Any

from pydantic import BaseModel
from PIL import Image
from flask import Flask, jsonify, request

from cnocr import CnOcr
from cnocr.utils import set_logger

logger = set_logger(log_level='DEBUG')

OCR_MODEL = CnOcr()
app = Flask(__name__)


class OcrResponse(BaseModel):
    status_code: int = 200
    results: List[Dict[str, Any]]

    def dict(self, **kwargs):
        the_dict = deepcopy(super().dict())
        return the_dict


@app.route('/')
def root():
    return {"message": "Welcome to CnOCR Server!"}


@app.route('/ocr', methods=['POST'])
def ocr() -> Dict[str, Any]:
    file = request.files['image']
    img_bytes = file.read()
    image = Image.open(io.BytesIO(img_bytes)).convert('RGB')
    res = OCR_MODEL.ocr(image)
    for _one in res:
        _one['position'] = _one['position'].tolist()
        if 'cropped_img' in _one:
            _one.pop('cropped_img')

    return jsonify(OcrResponse(results=res).dict())

@app.route('/ocrStream', methods=['POST'])
def ocrStream()-> Dict[str, Any]:
    # 检查请求中是否有文件数据
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    # 如果用户没有选择文件，浏览器也可能发送一个空的文件名
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        # 这里你可以处理文件，例如保存到磁盘或数据库
        # file.save(os.path.join(UPLOAD_FOLDER, filename))
        
        # 读取文件流
        file_stream = file.read()
        
        image = Image.open(io.BytesIO(img_bytes)).convert('RGB')
        res = OCR_MODEL.ocr(image)
        for _one in res:
            _one['position'] = _one['position'].tolist()
            if 'cropped_img' in _one:
                _one.pop('cropped_img')

        return jsonify(OcrResponse(results=res).dict())


if __name__ == "__main__":
    app.run()
