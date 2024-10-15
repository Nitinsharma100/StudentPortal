from django.shortcuts import render, redirect
from .models import Notes, Homework, Todo
from .forms import *
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch
from django.contrib.auth.decorators import login_required
import requests
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
import wikipedia
from django.shortcuts import render, get_object_or_404, redirect
# Create your views here.

def home(request):
    return render(request, 'dashboard/home.html')

@login_required(login_url='login')  # Ensure user is logged in to access notes
def notes(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user=request.user, title=request.POST['title'], description=request.POST['description'])
            notes.save()
            messages.success(request, f"Notes Added by {request.user.username} Successfully!")
    else:
        form = NotesForm()

    notes = Notes.objects.filter(user=request.user)
    return render(request, 'dashboard/notes.html', {'notes': notes, 'form': form})

@login_required(login_url='login')
def delete_note(request, pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect('notes')

class NotesDetailView(generic.DetailView):
    model = Notes
    template_name = 'dashboard/notes_detail.html'

@login_required(login_url='login')
def homework(request):
    if request.method == 'POST':
        form = Homeworkform(request.POST)
        if form.is_valid():
            finished = request.POST.get('is_finished') == 'on'

            homework = Homework(
                user=request.user,
                subject=request.POST['subject'],
                title=request.POST['title'],
                description=request.POST['description'],
                due=request.POST['due'],
                is_finished=finished,
            )
            homework.save()
            messages.success(request, f'Homework Added by {request.user.username} Successfully!')
    else:
        form = Homeworkform()

    homework = Homework.objects.filter(user=request.user)
    homework_done = len(homework) == 0

    return render(request, 'dashboard/homework.html', {'homework': homework, 'homedone': homework_done, 'form': form})

@login_required(login_url='login')
def update_homework(request, pk=None):
    homework = Homework.objects.get(id=pk)
    homework.is_finished = not homework.is_finished  # Toggle the finished status
    homework.save()
    return redirect('homework')

@login_required(login_url='login')
def delete_homework(request, pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect('homework')

@login_required(login_url='login')
def youtube(request):
    if request.method == 'POST':
        form = Dashboardform(request.POST)
        text = request.POST['text']
        video_search = VideosSearch(text, limit=10)

        try:
            video_results = video_search.result()
        except Exception as e:
            messages.error(request, "Error fetching video results: " + str(e))
            video_results = None

        result_list = []
        if video_results and 'result' in video_results:
            for i in video_results['result']:
                result_dict = {
                    'input': text,
                    'title': i.get('title'),
                    'duration': i.get('duration'),
                    'thumbnails': i.get('thumbnails')[0]['url'] if i.get('thumbnails') else None,
                    'channel': i.get('channel', {}).get('name'),
                    'link': i.get('link'),
                    'views': i.get('viewCount', {}).get('short'),
                    'published': i.get('publishedTime')
                }

                desc = ''
                if i.get('descriptionSnippet'):
                    for j in i['descriptionSnippet']:
                        desc += j['text']
                result_dict['descriptionSnippet'] = desc

                result_list.append(result_dict)
        else:
            messages.error(request, "No results found!")

        return render(request, 'dashboard/youtube.html', {'form': form, 'results': result_list})
    else:
        form = Dashboardform()

    return render(request, 'dashboard/youtube.html', {'form': form})

@login_required(login_url='login')
def todo(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            finished = request.POST.get('is_finished') == 'on'

            todo = Todo(user=request.user, title=request.POST['title'],desc=request.POST['desc'], is_finished=finished)
            todo.save()
            messages.success(request, f"Todo Added by {request.user.username} Successfully!")
    else:
        form = TodoForm()

    todo = Todo.objects.filter(user=request.user)
    todos_done = len(todo) == 0

    return render(request, 'dashboard/todo.html', {'todo': todo, 'form': form, 'todos_done': todos_done})

@login_required(login_url='login')
def delete_todo(request, pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect('todo')

@login_required(login_url='login')
def updatetodo(request, pk=None):
    todo = get_object_or_404(Todo, pk=pk) 
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save() 
            return redirect('todo') 
    else:
        form = TodoForm(instance=todo)
    return render(request, 'dashboard/updatetodo.html', {'form': form})





def books(request):
    if request.method == 'POST':
        form = Dashboardform(request.POST)
        text = request.POST['text']
        url = 'https://www.googleapis.com/books/v1/volumes?q=' + text
        r = requests.get(url)
        answer = r.json()
        result_list = []

      
        if 'items' in answer:
            for i in answer['items']:
                volume_info = i.get('volumeInfo', {})
                result_dict = {
                    'title': volume_info.get('title'),
                    'authors': ', '.join(volume_info.get('authors', [])),
                    'publishedDate': volume_info.get('publishedDate'),
                    'description': volume_info.get('description', 'No description available'),
                    'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail'),
                    'previewLink': volume_info.get('previewLink')
                }

                result_list.append(result_dict)
        else:
            messages.error(request, "No results found!")

        return render(request, 'dashboard/books.html', {'form': form, 'results': result_list})
    else:
        form = Dashboardform()

    return render(request, 'dashboard/books.html', {'form': form})



def dictionary(request):
    if request.method == 'POST':
        form = Dashboardform(request.POST)  # Validate form with POST data
        if form.is_valid():
            text = form.cleaned_data['text']  # Use cleaned data
            url = 'https://api.dictionaryapi.dev/api/v2/entries/en_US/' + text
            r = requests.get(url)
            answer = r.json()

            try:
                phonetics = answer[0]['phonetics'][0]['text']
                audio = answer[0]['phonetics'][0]['audio']
                definition = answer[0]['meanings'][0]['definitions'][0]['definition']  # Correct spelling
                example = answer[0]['meanings'][0]['definitions'][0].get('example', 'No example available')
                synonyms = answer[0]['meanings'][0]['definitions'][0].get('synonyms', [])

                context = {
                    'form': form,
                    'input': text,
                    'phonetics': phonetics,
                    'audio': audio,
                    'definition': definition,
                    'example': example,
                    'synonyms': synonyms,
                }
            except (KeyError, IndexError):
                context = {
                    'form': form,
                    'input': '',
                    'error': 'Error in fetching data. Please try again.'
                }
    else:
        form = Dashboardform()
        context = {'form': form}

    return render(request, 'dashboard/dictionary.html', context)


def wiki(request):
    if request.method=="POST":
        text=request.POST['text']
        form=Dashboardform(request.POST)
        search=wikipedia.page(text)
        context={
            'form':form,
            'title':search.title,
            'link':search.url,
            'detail':search.summary
        }
        return render(request, 'dashboard/wiki.html', context)
    else:
        
        form=Dashboardform()
        context={
        'form':form
        }
    return render(request, 'dashboard/wiki.html', context)

import requests
from django.shortcuts import render
from .forms import Conversionform, ConversionLengthform, ConversionMassform

def conversion(request):
    if request.method == 'POST':
        form = Conversionform(request.POST)
        if form.is_valid():
            measurement_type = request.POST.get('measurement')

            if measurement_type == 'length':
                measurement_form = ConversionLengthform(request.POST)
                context = {
                    'form': form,
                    'm_form': measurement_form,
                    'input': True
                }

                if 'input' in request.POST:
                    first = request.POST.get('measure1')
                    second = request.POST.get('measure2')
                    input_value = request.POST.get('input')
                    answer = ''

                    if input_value and float(input_value) >= 0:
                        if first == 'yard' and second == 'foot':
                            answer = f"{input_value} yard = {float(input_value) * 3} foot"
                        elif first == 'foot' and second == 'yard':
                            answer = f"{input_value} foot = {float(input_value) / 3} yard"

                    context['answer'] = answer

            elif measurement_type == 'mass':
                measurement_form = ConversionMassform(request.POST)
                context = {
                    'form': form,
                    'm_form': measurement_form,
                    'input': True
                }

                if 'input' in request.POST:
                    first = request.POST.get('measure1')
                    second = request.POST.get('measure2')
                    input_value = request.POST.get('input')
                    answer = ''

                    if input_value and float(input_value) >= 0:
                        if first == 'pound' and second == 'kilogram':
                            answer = f"{input_value} pound = {float(input_value) * 0.453592} kilogram"
                        elif first == 'kilogram' and second == 'pound':
                            answer = f"{input_value} kilogram = {float(input_value) * 2.20462} pound"

                    context['answer'] = answer

            return render(request, 'dashboard/conversion.html', context)

    else:
        form = Conversionform()
        context = {
            'form': form,
            'input': False
        }

    return render(request, 'dashboard/conversion.html', context)

def register(request):
    if request.method=='POST':
        form=Userregistrationform(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            messages.success(request,f"Account Created for {username}")
            return redirect("login")
    else:
        
        form=Userregistrationform()
    context={
        'form':form
    }
    return render(request,'dashboard/register.html',context)

def profile(request):
    homework=Homework.objects.filter(is_finished=False,user=request.user)
    todo=Todo.objects.filter(is_finished=False,user=request.user)

    if len(homework)==0:
        homework_done=True
    else:
        homework_done=False
    if len(todo)==0:
        todo_done=True
    else:
        todo_done=False
    context={
        'homework':homework,
        'todo':todo,
        'homework_done':homework_done,
        'todo_done':todo_done
    }
    return render(request,'dashboard/profile.html',context)


class CustomLogoutView(LogoutView):
    template_name = 'dashboard/logout.html'
    next_page = reverse_lazy('login')  
    



