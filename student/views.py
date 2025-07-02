from django.shortcuts import render
from django.conf import settings 
from groq import Groq
import re

client = Groq(api_key=settings.GROQ_API_KEY)

def learning_view(request):
    return render(request, 'student_homepage/Learning.html')

def ide_view(request):
    return render(request, 'student_homepage/IDEonline.html')

def practice_view(request):
    return render(request, 'student_homepage/practice.html')

def parse_quiz_text(quiz_text):
    questions = []
    blocks = re.split(r"\n\d+\.", quiz_text)
    for block in blocks:
        if not block.strip():
            continue
        lines = block.strip().splitlines()
        if len(lines) < 6:
            continue  # bỏ nếu không đủ dữ liệu

        q_text = lines[0].strip()
        opts = lines[1:5]
        answer_line = lines[5].strip()
        answer = answer_line.split(":")[-1].strip()[-1] 

        questions.append({
            "question": q_text,
            "options": opts,
            "answer": answer
        })
    return questions

def quizAI_view(request):
    quiz = []
    if request.method == 'POST':
        topic = request.POST.get('topic', '').strip()
        if topic:
            prompt = f"""
Generate exactly 5 multiple-choice quiz questions on the topic: "{topic}".
Each question must follow this strict format:

1. Question text?
A. Option A
B. Option B
C. Option C
D. Option D
Answer: A

Only output the questions in this format. Do not include explanations or introductions.
"""

            completion = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "system", "content": "You are a helpful AI that generates quizzes."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7
            )

            raw_text = completion.choices[0].message.content.strip()

            # Parse thành list các câu hỏi
            blocks = re.split(r'\n(?=\d+\.\s)', raw_text)
            for block in blocks:
                if "Answer:" not in block:
                    continue

                parts = block.strip().split('\n')
                question_line = parts[0][3:]  # Bỏ "1. "
                options = [line.strip() for line in parts[1:5] if line.strip()]
                answer_line = next((l for l in parts if l.lower().startswith("answer:")), None)
                answer = answer_line.split(":")[1].strip() if answer_line else ''

                quiz.append({
                    'question': question_line,
                    'options': options,
                    'answer': answer
                })

    return render(request, 'student_homepage/QuizAI.html', {'quiz': quiz})