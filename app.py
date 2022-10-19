from flask import Flask, render_template, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sensor_data.db'
db = SQLAlchemy(app)

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensor_data = db.Column(db.Integer, default=0)
    
    #There is an implicit constructor here by flask

    def __repr__(self) -> str:
        return f"Data: {self.sensor_data}"

@app.route("/update_data", methods=["PUT"])
def update_data():
    sensor_data = SensorData.query.first().sensor_data
    return jsonify("", render_template("sensor_data_model.html", data=sensor_data))

@app.route("/upload_data", methods=["POST"])
def upload_data():
    request_data = request.get_json()
    esp_data = request_data['sensor_data']
    data_object = SensorData.query.first()
    if data_object == None:
        sensor_data = SensorData(sensor_data=esp_data)  
        db.session.add(sensor_data)
        db.session.commit()
        return ''
    data_object.sensor_data = esp_data
    db.session.commit()
    return ''

@app.route("/")
def index():
    return render_template("Welcome.html")

@app.route("/home")
def home():
    return render_template("Home.html", data=SensorData.query.first().sensor_data)


if __name__ == "__main__":
    app.run(debug=True)