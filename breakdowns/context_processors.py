from .models import StandardLibrary

def library_processor(request):
	library_list = StandardLibrary.objects.all()
	return {'library_list': library_list}
