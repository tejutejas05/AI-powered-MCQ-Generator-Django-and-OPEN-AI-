from django.shortcuts import render
from django.http import JsonResponse
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# configure Gemini safely
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def home(request):
    return render(request, "generator/index.html")


def generator_mcqs(request):
    topic = request.GET.get('topic', '').strip()
    difficulty = request.GET.get('difficulty', '').strip()
    num_questions = request.GET.get('num_questions', '').strip()

    # ✅ validate inputs
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