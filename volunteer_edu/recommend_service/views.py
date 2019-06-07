from django.http import JsonResponse
from logic.recommend_actions.RecommendVolunteers import recommendVolunteers
from logic.utils import getForm


# Create your views here.
def recommend_volunteer(request):
    if request.method == 'POST':
        form = getForm(request.POST)
        message = recommendVolunteers(form)
        return JsonResponse({'message': message}, status=200)
