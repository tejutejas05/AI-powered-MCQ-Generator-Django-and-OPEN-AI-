from django.shortcuts import render
from django.http import JsonResponse
import os
import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def generator_mcqs(request):
    topic = request.GET.get('topic')
    difficulty = request.GET.get('difficulty')
    num_questions = request.GET.get('num_questions')


    prompt = f"""
Generate {num_questions} {difficulty} MCQs about {topic}.

Format:
Q1:
A)
B)
C)
D)
Answer:
"""
    model = genai.GenerativeModel("gemini-2.5-flash")

    response = model.generate_content(prompt)



    return JsonResponse({
        "mcqs" : response.text
    })




