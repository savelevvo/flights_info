from flask import Flask

app = Flask('flights_info')


@app.route('/')
def hello_world():
    return ''


if __name__ == '__main__':
    app.run()
