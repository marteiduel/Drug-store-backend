from flask import Flask, jsonify, request, url_for 
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS 
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku 
import os 

app = Flask(__name__)
heroku = Heroku(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")

CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Patient(db.Model):
    patient_id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(50))
    patient_age = db.Column(db.String(50))
    patient_address = db.Column(db.String(60))
    patient_birthdate = db.Column(db.String(250))
    patient_gender = db.Column(db.String(100))
    patient_number = db.Column(db.String(50))
    patient_income = db.Column(db.String(100))
    patient_commercial = db.Column(db.Boolean, default=False)
    patient_medicare = db.Column(db.Boolean, default=False)
    patient_medicaid = db.Column(db.Boolean, default=False)
    

    def __init__(self, patient_name, patient_age, patient_address, patient_birthdate, patient_number,patient_gender, patient_income, patient_commercial, patient_medicare, patient_medicaid):
        self.patient_name = patient_name
        self.patient_age = patient_age
        self.patient_address = patient_address
        self.patient_birthdate = patient_birthdate 
        self.patient_income = patient_income
        self.patient_gender = patient_gender
        self.patient_number = patient_number
        self.patient_commercial = patient_commercial
        self.patient_medicare = patient_medicare
        self.patient_medicaid = patient_medicaid
        

class PatientFullSchema(ma.Schema):
    class Meta: 
        fields= ("patient_id", "patient_name", "patient_age", "patient_address", "patient_birthdate", "patient_gender", "patient_number", "patient_income", "patient_commercial", "patient_medicare", "patient_medicaid" )

patient_schema = PatientFullSchema()
patients_schema = PatientFullSchema(many=True)

@app.route("/") #homepage
def greeting():
    return "<h1>Patients Info API</h1>" 

@app.route("/patients",methods=["GET"])
def get_patients():
    all_patients = Patient.query.all()
    result = patients_schema.dump(all_patients)
    return jsonify(result.data)


@app.route("/patient/<id>",methods=["GET"])
def get_patient(id):
    patient = Patient.query.get(id)
    return patient_schema.jsonify(patient)


@app.route("/add-patient" , methods=["POST"])
def add_patient():
    name = request.json["name"]
    age = request.json["age"]
    address = request.json["address"]
    birthdate = request.json["birthdate"]
    gender = request.json["gender"]
    number = request.json["number"]
    income = request.json["income"]
    commercial = request.json["commercial"]
    medicare = request.json["medicare"]
    medicaid = request.json["medicaid"]

    new_patient = Patient(name, age, address, birthdate, gender, number, income, commercial, medicare, medicaid)

    db.session.add(new_patient)
    db.session.commit()

    return jsonify("Patient Added")

@app.route("/patient/<id>", methods=["DELETE"])  
def delete_patient(id):
    patient = Patient.query.get(id)
    db.session.delete(patient)
    db.session.commit()

    return jsonify("Patient deleted")


@app.route("/patient/<id>", methods=["PUT"])  
def update_patient(id):
    patient = Patient.query.get(id)
    
    name = request.json["name"]
    age = request.json["age"]
    address = request.json["address"]
    birthdate = request.json["birthdate"]
    gender = request.json["gender"]
    number = request.json["number"]
    income = request.json["income"]
    commercial = request.json["commercial"]
    medicare = request.json["medicare"]
    medicaid = request.json["medicaid"]


    patient.name = name
    patient.age = age
    patient.address =  address
    patient.birthdate = birthdate
    patient.gender = gender
    patient.number = number
    patient.income = income
    patient.commercial = commercial
    patient.medicare = medicare
    patient.medicaid = medicaid


    db.session.commit()

    return patient_schema.jsonify(patient)


if __name__ =="__main__":
    app.debug = True
    app.run()