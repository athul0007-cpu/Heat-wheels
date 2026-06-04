from django.shortcuts import redirect, render
from django.views import View

from .models import FAQ, SupportMessage


class ContactView(View):
    template_name = 'support/contact.html'

    def get(self, request):
        return render(request, self.template_name, {'faqs': FAQ.objects.filter(featured=True)})

    def post(self, request):
        SupportMessage.objects.create(
            user=request.user if request.user.is_authenticated else None,
            subject=request.POST.get('subject', ''),
            message=request.POST.get('message', ''),
            email=request.POST.get('email', ''),
        )
        return redirect('support:contact')
