from django.http import JsonResponse, HttpResponse
from logic.utils import getForm
from logic.reservation_actions.CreateReservation import createReservation
from logic.reservation_actions.ConfirmReservation import confirmReservation
from logic.reservation_actions.FinishReservation import finishReservation
from logic.reservation_actions.GetMessages import getMessages
from logic.reservation_actions.GetMessageDetail import getMessageDetail
from logic.reservation_actions.GetReservations import getReservations
from logic.reservation_actions.CreateComment import createComment
from logic.reservation_actions.GetAllReservaions import getAllReservation


# Create your views here.
def create(request):
    if request.method == 'POST':
        form = getForm(request.POST)
        createReservation(form)
        return JsonResponse({'message': '订单创建成功'}, status=200)


def confirm(request):
    if request.method == 'POST':
        form = getForm(request.POST)
        message, code = confirmReservation(form)
        return JsonResponse({'message': message, 'code': code}, status=200)


# def consult(request):
#     if request.method == 'POST':
#         form = getForm(request.POST)
#         message, code = consultReservation(form)
#         return JsonResponse({'message': message, 'code': code}, status=200)


def finish(request):
    if request.method == 'POST':
        form = getForm(request.POST)
        message, code = finishReservation(form)
        return JsonResponse({'message': message, 'code': code}, status=200)


def comment(request):
    if request.method == 'POST':
        form = getForm(request.POST)
        message, code = createComment(form)
        return JsonResponse({'message': '评价成功', 'code': code}, status=200)


def message(request):
    if request.method == 'POST':
        form = getForm(request.POST)
        messages = getMessages(form)
        return JsonResponse({'messages': messages}, status=200)


def message_detail(request):
    if request.method == 'POST':
        form = getForm(request.POST)
        message = getMessageDetail(form)
        return JsonResponse({'message': message}, status=200)


def reservation(request):
    if request.method == 'GET':
        reservations = getAllReservation()
        return JsonResponse({'message': reservations}, status=200)
    elif request.method == 'POST':
        form = getForm(request.POST)
        reservations = getReservations(form)
        return JsonResponse({'message': reservations}, status=200)
