import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import image_handle

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = '../static/uploads'


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/find_out_points', methods=['POST'])
def find_out_points():
    image_file = request.files['image']
    template_file = request.files['template']
    image_filename = secure_filename(image_file.filename)
    template_filename = secure_filename(template_file.filename)
    if image_filename != '' and template_filename != '':
        image_ext = os.path.splitext(image_filename)[1]
        template_ext = os.path.splitext(template_filename)[1]
        if image_ext not in app.config['UPLOAD_EXTENSIONS'] or template_ext not in app.config['UPLOAD_EXTENSIONS']:
            return jsonify({
                "success": False,
                "message": "File extension not allowed!"
            })
        image_path = os.path.join(app.config['UPLOAD_PATH'], image_filename)
        template_path = os.path.join(app.config['UPLOAD_PATH'], template_filename)
        image_file.save(image_path)
        template_file.save(template_path)
        position = image_handle.find_out_point(image_path, template_path)
        os.remove(image_path)
        os.remove(template_path)
        if position['x'] is not None and position['y'] is not None:
            return jsonify({
                "success": True,
                "position": {
                    "x": str(position['x']),
                    "y": str(position['y'])
                },
            })
        else:
            return jsonify({
                "success": False,
                "message": "Cannot detect position!",
            })
    else:
        return jsonify({
            "success": False,
            "message": "Please choose image and template to handle!"
        })


if __name__ == '__main__':
    app.run()
