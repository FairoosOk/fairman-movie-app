from django.shortcuts import render, redirect
from django.contrib import messages
from airtable import Airtable
import os


AT = Airtable(os.environ.get('AIRTABLE_MOVIESTABLE_BASE_ID'),
              'Movies',
              api_key=os.environ.get('AIRTABLE_API_KEY'))

# Create your views here.
def home_page(request):
    user_query = str(request.GET.get('query', ''))
    search_result = AT.get_all(formula="FIND('" + user_query.lower() + "', LOWER({Name}))")
    stuff_for_frontend = {'search_result': search_result}
    return render(request, 'movies/movies_stuff.html', stuff_for_frontend)


def create(request):
    if request.method == "POST":
        data={
            'Name': request.POST.get('name'),
            'Pictures': [{'url':request.POST.get('url') or 'http://www.clker.com/cliparts/q/L/P/Y/t/6/no-image-available-md.png'}],
            'Rating': int(request.POST.get('rating')),
            'Trailer':request.POST.get('turl'),
            'Notes' : request.POST.get('notes')
             }
        try:
            response = AT.insert(data)
            #notify on create
            messages.success(request,'New Movie Added: {}'.format(response['fields'].get('Name')))
        except Exception as e:
            messages.warning(request,'Got an error:{}'.format(e))
    return redirect('/')

def edit(request, movie_id):
    if request.method == "POST":
        data={
            'Name': request.POST.get('name'),
            'Pictures': [{'url':request.POST.get('url') or 'http://www.clker.com/cliparts/q/L/P/Y/t/6/no-image-available-md.png'}],
            'Rating': int(request.POST.get('rating')),
            'Trailer':request.POST.get('turl'),
            'Notes': request.POST.get('notes')
             }
        try:
            response = AT.update(movie_id,data)
            #notify on update
            messages.success(request,'Updated Movie: {}'.format(response['fields'].get('Name')))
        except Exception as e:
            messages.warning(request,'Got an error while trying to update a movie {}'.format(e))
    return redirect('/')

def delete(request, movie_id):
    try:
        movie_name=AT.get(movie_id)['fields'].get('Name')
        AT.delete(movie_id)
        #notify on delete
        messages.warning(request,"Deleted Movie: {}".format(movie_name))
    except Exception as e:
        messages.warning(request,"Got an error while deleting Movie: {}".format(e))

    return redirect('/')
