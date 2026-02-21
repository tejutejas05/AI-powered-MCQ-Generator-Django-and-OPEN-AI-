from django.shortcuts import render
from django.http import JsonResponse
import os


def generator_mcqs(request):
    topic = request.GET.get('topic')
    difficulty = request.GET.get('difficulty')
    num_questions = request.GET.get('num_questions')


    prompt = f"""
    Generate {num_questions} {difficulty} multiple choice questions about {topic}.
    Provide 4 options and mark the correct answer.
    Return the result in JSON Format.
    """

    return JsonResponse({
        "message" : "Prompt created successfully",
        "prompt" : prompt
    })




