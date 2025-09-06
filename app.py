from flask import Flask, render_template, request, send_file
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import re
import pandas as pd
import logging

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)

# Set maximum upload size to 50 MB
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 50 MB

# Gemini function
def get_gemini_response(input):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(input)
        return response.text
    except Exception as e:
        return f"Error in Gemini API call: {str(e)}"

# Convert PDF to text
def input_pdf_text(uploaded_file):
    try:
        reader = pdf.PdfReader(uploaded_file)
        text = ""
        for page in range(len(reader.pages)):
            page = reader.pages[page]
            text += str(page.extract_text())
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

# Check if PDF is a CV or resume based on keywords
def is_resume(text):
    resume_keywords = ["experience", "education", "skills", "certification", "contact", "profile", "portfolio", "references"]
    for keyword in resume_keywords:
        if keyword.lower() in text.lower():
            return True
    return False

logging.basicConfig(level=logging.DEBUG)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            jd = request.form["job_description"]
            uploaded_files = request.files.getlist("resumes")

            logging.debug(f"Number of files uploaded: {len(uploaded_files)}")

            if not jd.strip():
                return render_template("index.html", result="Job description cannot be empty.", jd=jd)

            if uploaded_files:
                results = {}
                match_data = []

                for uploaded_file in uploaded_files:
                    try:
                        file_name = uploaded_file.filename
                        resume_text = input_pdf_text(uploaded_file)
                        evaluation_result = ""

                        if not is_resume(resume_text):
                            results[file_name] = "The uploaded file is not a CV or resume. Please upload a valid resume."
                            continue

                        input_prompt = f"""
                        ### As an expert Application Tracking System (ATS), your task is to evaluate a resume based on the job description.

                        ### Job Description: {jd}

                        ### Resume Text: {resume_text}

                        ### Evaluation Output:
                        1. Calculate and show only the percentage of match between the resume and the job description.
                        2. Show matching keywords or skills from the job description
                        3. Identify any key skills or keywords from the job description that are missing in the resume.
                        """
                        response = get_gemini_response(input_prompt)

                        match_percentage = "N/A"
                        matching_keywords = []
                        missing_keywords = []
                        matching_keywords_text = ""
                        missing_keywords_text = ""
                        # Extract match percentage
                        match_search = re.search(r"(\d+)%", response)
                        if match_search:
                            match_percentage = match_search.group(1)

                        # Extract matching keywords or skills
                        match_keywords_start = response.find("Matching Keywords or Skills:")
                        missing_keywords_start = response.find("Missing Key Skills or Keywords:")
                         
                        if match_keywords_start != -1 and missing_keywords_start != -1:
                            matching_keywords_text = response[match_keywords_start + len("Matching Keywords or Skills:"):missing_keywords_start].strip()
                            missing_keywords_text = response[missing_keywords_start + len("Missing Key Skills or Keywords:"):].strip()
                        else:
                            match_keywords_start = response.find("Matching Keywords and Skills:")
                            missing_keywords_start = response.find("Missing Keywords and Skills:")

                            if match_keywords_start != -1 and missing_keywords_start != -1:
                                matching_keywords_text = response[match_keywords_start + len("Matching Keywords and Skills:"):missing_keywords_start].strip()
                                missing_keywords_text = response[missing_keywords_start + len("Missing Keywords and Skills:"):].strip()

                        if matching_keywords_text:
                            matching_keywords = [kw.strip('- ') for kw in matching_keywords_text.split('\n') if kw.strip()]

                        if missing_keywords_text:
                            missing_keywords = [kw.strip('- ') for kw in missing_keywords_text.split('\n') if kw.strip()]

                        evaluation_result += f"\n\n{response}"

                        results[file_name] = evaluation_result
                        match_data.append({
                            "File Name": file_name,
                            "Match Percentage": match_percentage,
                            "Matching Keywords": ", ".join(matching_keywords),
                            "Missing Keywords": ", ".join(missing_keywords)
                        })

                        logging.debug(f"Processed file: {file_name}, Match Percentage: {match_percentage}")
                    except Exception as file_error:
                        results[uploaded_file.filename] = f"Error processing file: {str(file_error)}"

                df = pd.DataFrame(match_data)
                df.to_excel("match_results.xlsx", index=False)

                return render_template("index.html", result=results, jd=jd)

            return render_template("index.html", result="No files uploaded. Please upload one or more resumes.", jd=jd)

        except Exception as e:
            logging.error(f"An unexpected error occurred: {str(e)}")
            return render_template("index.html", result=f"An unexpected error occurred: {str(e)}", jd="")

    return render_template("index.html", result=None)

@app.route('/download')
def download_file():
    path = "match_results.xlsx"
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
