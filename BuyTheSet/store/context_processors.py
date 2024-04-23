from .models import Category
from .forms import SearchForm

def get_categories(request):
    return {'categories': Category.objects.all()}

def search(request):
    return {'search_form': SearchForm()}
