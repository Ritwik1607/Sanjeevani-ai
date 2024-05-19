from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template, request, flash, redirect, url_for, session, send_file
import os
from flask_mail import Mail, Message
from config import Config  # Assuming config.py holds mail configuration
import google.generativeai as genai
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired
from reportlab.pdfgen import canvas

app = Flask(__name__)
app.config.from_object(Config)
mail = Mail(app)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

class SymptomForm(FlaskForm):
    symptom3 = TextAreaField('Please provide your name')
    symptom1 = TextAreaField('Describe your main symptom(s):', validators=[DataRequired()])
    symptom2 = TextAreaField('Do you have any other symptoms?')
    symptom4 = TextAreaField()

def generate_report(symptoms):
    diagnosis = "Based on your description, you might be experiencing [possible diagnosis]. However, this is not a confirmed diagnosis and further evaluation is needed. Please consult with a licensed physician for proper diagnosis and treatment."
    return diagnosis

def create_report_pdf(name, symptoms, diagnosis):
    pdf = canvas.Canvas("report.pdf")
    pdf.drawString(50, 750, f"Patient Name: {name}")
    pdf.drawString(50, 720, f"Symptoms: {symptoms}")
    pdf.drawString(50, 690, f"Diagnosis: {diagnosis}")
    pdf.save()

# ... Existing routes for diagnosis and report generation (/index, /download_report)

# Rendering loader page
@app.route("/", methods=['GET', 'POST'])
def load():
    return render_template("loader.html")

# Rendering home page
@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template("home.html")

# Rendering about page
@app.route("/about", methods=['GET', 'POST'])
def about():
    return render_template("about.html")

# Rendering contact page
@app.route("/contact", methods=['GET', 'POST'])
def contact():
    return render_template("contact.html")

data = []

# Endpoint to handle text and store it in the session (chatbot)
@app.route("/gemini", methods=['GET', 'POST'])
def text():

    data = session.get('data', [])

    if request.method == "POST":
        input_text = request.form.get("text")

        if input_text:
            # Using generative AI model to generate content
            model = genai.GenerativeModel(model_name="gemini-pro")
            response = model.generate_content(input_text)

            text_result = response.text

            data.append({'input': input_text, 'result': text_result})
            session['data'] = data

            return redirect(url_for('text'))

        else:
            flash("Please provide a valid input!", "error")

    return render_template("index.html", data=data[::-1])  # Reverse data for display

# ... Existing routes for logout, sending email (/logout, /send-mail)

if __name__ == '__main__':
    app.run(debug=True)
