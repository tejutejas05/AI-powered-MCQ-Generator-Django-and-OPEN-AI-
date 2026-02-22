from django.shortcuts import render
from django.http import JsonResponse
import os
import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def home(request):
    return render(request,"generator/index.html")

def generator_mcqs(request):
    topic = request.GET.get('topic')
    difficulty = request.GET.get('difficulty')
    num_questions = request.GET.get('num_questions')


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


    model = genai.GenerativeModel("gemini-2.5-flash")

    response = model.generate_content(prompt)



    return JsonResponse({
        "mcqs" : response.text
    })




