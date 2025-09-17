# routes/adhd_tools.py

from flask import Blueprint, request, jsonify
from utils.gpt_adhd_tools import generate_adhd_tools

adhd_tools_bp = Blueprint('adhd_tools', __name__)

@adhd_tools_bp.route('/generate-adhd-tools', methods=['POST'])
def handle_generate_adhd_tools():
    data = request.get_json()
    if not data or 'summary' not in data:
        return jsonify({'error': 'Summary text is required'}), 400

    summary = data['summary']
    aids = generate_adhd_tools(summary)

    if "error" in aids:
        return jsonify(aids), 500
    

    return jsonify(aids)