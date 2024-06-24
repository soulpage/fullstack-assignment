from flask import Blueprint, jsonify

management_bp = Blueprint('management', __name__)

@management_bp.route('/file/<filename>', methods=['DELETE'])
def delete_file(filename):
    # Implement file deletion logic here
    return jsonify({'message': f'File {filename} deleted successfully'}), 200

@management_bp.route('/file/<filename>', methods=['GET'])
def get_file(filename):
    # Implement file retrieval logic here
    return jsonify({'message': f'Retrieving file {filename}'}), 200
