import os

from django.conf import settings
from django.http import FileResponse, HttpResponseNotFound
from django.shortcuts import render
from django.db import connections
from django.shortcuts import render
import asyncio
from confirm_students.telegram_message import send_telegram_message


def get_students(request):
    with connections['default'].cursor() as cursor:
        cursor.execute("SELECT surname, name, gender, room_id , payment_accommodation, payment_food, phone_number, tg_id, id FROM users where is_payment_approved == 1 and approved_by_admin == false ")
        students = cursor.fetchall()

        students_json = [{
            "surname": students[i][0],
            "name": students[i][1],
            "gender": students[i][2],
            "room_id": students[i][3],
            "payment_accommodation": students[i][4],
            "payment_food": students[i][5],
            "phone_number": students[i][6],
            "telegram_id": students[i][7],
            "id": students[i][8]

        } for i in range(len(students)) ]

        if request.method == 'POST':
            telegram_id = request.POST.get('telegram_id')
            action = request.POST.get('action')

            if action == 'accept':
                # Send a confirmation message
                asyncio.run(send_telegram_message(int(telegram_id), "Ваша регистрация прошла успешно✅\nЖдем вас 28-го августа вместе с документами🎉"))
                confirm(telegram_id)
            elif action == 'decline':
                # Optionally, handle the 'decline' action (if needed)
                asyncio.run(send_telegram_message(int(telegram_id), "Ваш платеж отклонен! Регистрируйтесь снова."))
                decline(telegram_id)
        context = {
            "students": students_json,
        }
        return render(request, "confirm_students/index.html", context)

def view_accommodation_pdf(request, file_name):
    # if request.GET.get("view_pdf"):

    pdf_path = os.path.join("/Users/arsensejtkaliev/PycharmProjects/SDUDormInfo/", file_name)

    return FileResponse(open(pdf_path, 'rb'), content_type='application/pdf')

def confirm(telegram_id):
    with connections['default'].cursor() as cursor:
        cursor.execute("UPDATE users SET approved_by_admin = 1 WHERE tg_id = %s", (telegram_id,))

def decline(telegram_id):
    with connections['default'].cursor() as cursor:
        cursor.execute("DELETE FROM users WHERE tg_id = %s", (telegram_id,))