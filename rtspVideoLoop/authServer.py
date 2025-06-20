from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/auth', methods=['POST'])
def auth():
    data = request.get_json()
    if data.get('user') == 'admin1':
        print('password used: ' + data.get('password'))
        return jsonify({"ok": True}), 200
    return jsonify({"ok": False}), 401

if __name__ == '__main__':
    app.run(port=9000)

