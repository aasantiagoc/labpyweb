class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        #print("Antes de la vista")
        response = self.get_response(request)
        #print("Despues de la vista")

        return response