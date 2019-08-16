from flask import Flask
import views

app = Flask('flights_info')
app.register_blueprint(views.flight_info)

if __name__ == '__main__':
    app.run()
