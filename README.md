# Smart ATS

Smart ATS is an AI-powered Applicant Tracking System (ATS) designed to evaluate resumes against job descriptions. The application provides a detailed analysis, including match percentages, missing keywords, and actionable feedback, helping users optimize their resumes for job applications.



---

## Features

### Backend
- **Flask Application**:  
  Handles resume uploads and integrates with the Gemini Pro API for content analysis.
  
- **Resume Parsing**:  
  Extracts text from PDF resumes using `PyPDF2`.
  
- **AI-Powered Analysis**:  
  Provides detailed evaluations, including:  
  - Match percentage between resume and job description.  
  - Matching keywords or skills found in both the job description and the resume.  
  - Missing keywords or skills from the job description that are absent in the resume.  
  
- **Error Validation**:  
  - Ensures only valid resumes are processed by checking for essential keywords (e.g., "experience," "skills").  
  - Handles errors in API calls, invalid formats, and incomplete uploads gracefully.

- **Excel Report Generation**:  
  - Outputs evaluation results, including match percentage, matching keywords, and missing keywords, into an Excel file for download.

### Frontend
- **Bootstrap UI**:  
  A modern, responsive interface for seamless user interactions.
  
- **Real-Time Loader**:  
  A dynamic animated loader with a blurred background displays while resumes are being processed.
  
- **Feedback Messages**:  
  Clear alerts inform users of invalid uploads, missing job descriptions, or other processing errors.

### API Integration
- **Gemini Pro API**:  
  The AI engine evaluates resumes based on the job description and generates insights, including match percentages and keyword analysis.
  
- **Environment Variables**:  
  Secure management of `GEMINI_API_KEY` using `.env` files and `python-dotenv`.

---

## How It Works

1. **Input**  
   - Users paste a job description into a text field.  
   - Upload one or more resumes in PDF format.  

2. **Processing**  
   - The system extracts text from uploaded resumes using `PyPDF2`.  
   - The extracted resume text and job description are analyzed by the Gemini API to calculate match percentages, identify matching and missing keywords, and generate suggestions.  

3. **Output**  
   - Displays a match percentage.  
   - Lists matching and missing keywords.  
   - Provides actionable suggestions for improving the resume.  
   - An Excel report containing results for all uploaded resumes is available for download.

4. **Validation**  
   - Rejects non-resume files or PDFs without relevant resume content.  
   - Returns clear error messages if processing fails or invalid inputs are provided.  

---

## Tech Stack

- **Backend**: Flask, Python, PyPDF2  
- **Frontend**: HTML, CSS, Bootstrap  
- **AI Integration**: Gemini Pro API  
- **Data Analysis**: Pandas  
- **Environment Management**: Python `dotenv`
