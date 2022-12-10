from .models import Target
from .forms import TargetCreateForm

class TargetCreateFormMiddleware:

    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):
        create_form = TargetCreateForm()
        request.target_create_form = create_form
        response = self.get_response(request)  
        return response