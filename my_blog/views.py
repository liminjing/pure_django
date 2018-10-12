from django.shortcuts import render
from my_blog.models import Item_detail
from django.core.paginator import Paginator

# Create your views here.
def blog(request):
    return render(request,'blog.html')

def new_blog(request):
    items=Item_detail.objects[:10]

    limit=3
    paginator=Paginator(items,limit)
    page=request.GET.get('page',1)
    page_info=paginator.page(page)
    context={
        'items':page_info
    }

    return render(request,'new_blog.html',context)