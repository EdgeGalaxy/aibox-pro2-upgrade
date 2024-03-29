import os
import json
import yaml

import subprocess
import tarfile
from flask import Flask, request, jsonify

app = Flask(__name__)
# 设置文件上传的目标文件夹
UPGRADE_FOLDER = os.path.dirname(__file__)
# 设置配置文件的目标文件夹
UPDATE_FOLDER = '/data/weights'


def save_config(config_file, config_info):
    os.makedirs(UPDATE_FOLDER, exist_ok=True)
    with open(os.path.join(UPDATE_FOLDER, config_file), 'w') as f:
        yaml.dump(config_info, f)


@app.route('/update-config', methods=['POST'])
def update_config():
    # 获取新的配置参数
    try:
        request_param = request.get_data()
        request_param = json.loads(request_param)
        config_file = request_param.get('config_file')
        config_info = request_param.get('config_info')
        print(f"Received new config: {config_file}")

        # 更新配置文件
        save_config(config_file, config_info)

        # 重启Docker服务
        subprocess.run(['sudo', 'docker-compose', '-f', 'docker-compose_rt.yml', 'down'], check=True)
        subprocess.run(['sudo', 'docker-compose', '-f', 'docker-compose_rt.yml', 'up', '-d'], check=True)

        return jsonify({'message': 'Configuration updated and service restarted successfully'}), 200
    except Exception as e:
        print(e)
        jsonify({'message': 'File uploaded or service restarted not successfully'}), 200


@app.route('/update', methods=['POST'])
def update():
    # 获取新的配置参数
    try:
        request_param = request.files['file']
        file_name = request_param.filename
        print(f"Received new file: {file_name}")
        file_path = os.path.join(UPDATE_FOLDER, file_name)
        request_param.save(file_path)
        print(f"Saved file size: {os.path.getsize(file_path)} bytes")
        # 解压缩文件
        with tarfile.open(file_path, "r:gz") as tar:
            tar.extractall(path=UPDATE_FOLDER)

        os.remove(file_path)  # 删除压缩包

        # 重启Docker服务
        subprocess.run(['sudo', 'docker-compose', '-f', 'docker-compose_rt.yml', 'down'], check=True)
        subprocess.run(['sudo', 'docker-compose', '-f', 'docker-compose_rt.yml', 'up', '-d'], check=True)

        return jsonify({'message': 'File uploaded and service restarted successfully'}), 200
    except Exception as e:
        print(e)
        jsonify({'message': 'File uploaded or service restarted not successfully'}), 200


@app.route('/upgrade', methods=['POST'])
def upgrade():
    # 获取新的代码
    try:
        request_param = request.files['file']
        file_name = request_param.filename
        print(f"Received new file: {file_name}")
        file_path = os.path.join(UPGRADE_FOLDER, file_name)
        request_param.save(file_path)
        print(f"Saved file size: {os.path.getsize(file_path)} bytes")
        # 解压缩文件
        with tarfile.open(file_path, "r:gz") as tar:
            tar.extractall(path=UPGRADE_FOLDER)

        os.remove(file_path)  # 删除压缩包

        # 重启Docker服务
        subprocess.run(['sudo', 'docker-compose', '-f', 'docker-compose_rt.yml', 'down'], check=True)
        subprocess.run(['sudo', 'docker-compose', '-f', 'docker-compose_rt.yml', 'up', '-d', '--build'], check=True)

        return jsonify({'message': 'File uploaded and service restarted successfully'}), 200
    except Exception as e:
        print(e)
        jsonify({'message': 'File uploaded or service restarted not successfully'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
