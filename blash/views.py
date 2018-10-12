from django.shortcuts import render
from blash.models import Pokemon
from django.core.paginator import Paginator

# Create your views here.
def blash(request):
    return render(request,'blash.html')


def new_blash(request):
    # context = {
    #     'title': 'this is a title',
    #     'desc': 'here is description',
    #     'rate': '6.0'
    # }

    pokemon=Pokemon.objects[:20]

    # context = {
    #     'title': pokemon[0].name,
    #     'desc':pokemon[0].desc,
    #     'rate':pokemon[0].rate
    # }

    limit=4
    paginator=Paginator(pokemon,limit)
    page=request.GET.get('page',1)
    page_info=paginator.page(page)

    print(request)
    print(request.GET)

    context={
        'pokemon':page_info
    }

    return render(request,'new_blash.html',context)


def new_website(request):
    info=Pokemon.objects[:1]
    pagnitor=Paginator(info,5)
    page=request.GET.get('page',1)
    page_info=pagnitor.page(page)
    context={
        'items':page_info
    }
    return render(request,'new_website.html',context)


