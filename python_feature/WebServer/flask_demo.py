from flask import Flask, request

app = Flask(__name__)


@app.route('/hello', methods=['POST'])
def hello():
    info = request.json
    name = info['name']
    age = info['age']

    age += 10
    rsp = f"name: {name}, age: {age}"
    return str({'success': True, 'msg': rsp})


if __name__ == '__main__':
    app.run()

# <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
# <title>500 Internal Server Error</title>
# <h1>Internal Server Error</h1>
# <p>The server encountered an internal error and was unable to complete your request. Either the server is overloaded or
# 	there is an error in the application.</p>