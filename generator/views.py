from django.shortcuts import render
from django.http import JsonResponse
import os
import google.generativeai as genai
from dotenv import load_dotenv
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse
import json
from io import BytesIO

load_dotenv()


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def home(request):
    return render(request, "generator/index.html")

def download_pdf(request):
    if request.method != "POST":
        return HttpResponse("Invalid request")

    mcqs_json = request.POST.get("mcqs")

    if not mcqs_json:
        return HttpResponse("No MCQs received")

    mcqs = json.loads(mcqs_json)

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    elements = []

   
    if isinstance(mcqs, list):

       
        if isinstance(mcqs[0], dict):
            for i, mcq in enumerate(mcqs):
                elements.append(Paragraph(f"Q{i+1}: {mcq['question']}", styles['Heading3']))
                for opt in mcq['options']:
                    elements.append(Paragraph(opt, styles['BodyText']))
                elements.append(Paragraph(f"Answer: {mcq['answer']}", styles['Normal']))
                elements.append(Spacer(1, 12))

        
        else:
            for q in mcqs:
                elements.append(Paragraph(q.replace("\n", "<br/>"), styles['BodyText']))
                elements.append(Spacer(1, 12))

    doc.build(elements)
    buffer.seek(0)

    return HttpResponse(buffer, content_type='application/pdf')

def generator_mcqs(request):
    topic = request.GET.get('topic', '').strip()
    difficulty = request.GET.get('difficulty', '').strip()
    num_questions = request.GET.get('num_questions', '').strip()



    if not topic or not difficulty or not num_questions:
        return JsonResponse({
            "error": "Please provide topic, difficulty, and number of questions."
        }, status=400)

    prompt = f"""
        Generate {num_questions} {difficulty} multiple choice questions about {topic}.

        Format strictly like:

        Q1: question
        A) option
        B) option
        C) option
        D) option
        Answer: correct option
        """

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)

        mcqs_text = response.text if response.text else "No questions generated."

        return JsonResponse({
            "mcqs": mcqs_text
        })

    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)