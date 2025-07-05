from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import get_user

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
        #URLs que no requieren autenticación
        self.public_urls = [
            '/',                        
            '/admin/',            
            '/admin/login/', 
            '/logout/'
        ]
    def __call__(self, request):
        #Verificar URL actual
        
        if self.is_public_url(request.path):
            response = self.get_response(request)
            return response
        if not request.user.is_authenticated:
            return redirect('login')
        
        response = self.get_response(request)
        return response;
    def is_public_url(self, path):
        if path in self.public_urls:
            return True
        return False
