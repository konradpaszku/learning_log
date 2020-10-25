from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.

def check_topic_owner(request, top_id):
    topic = Topic.objects.get(id=top_id)
    if topic.owner != request.user:
        raise Http404


def index(request):
    """Strona glowna dla aplikacji learning log"""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """Wyswietlanie wszystkich tematow"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)
@login_required
def topic(request, topic_id):
    """Wyswietla pojedynczy temat i wszystkie powiazane z nim wpisy."""
    topic = get_object_or_404(Topic, id=topic_id)
    #Make sure that topic is being fot actual user
    check_topic_owner(request, topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """Dodaj nowy temat"""
    if request.method != 'POST':
        #nie przekazano żadnych danych, należy utworzyć pusty formularz.
        form = TopicForm()
    else:
        #Przekazano dane za pomoca żądania POST, należy je utworzyć
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')

    #Wyswietlanie pustego formularza
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    
    
    """Dodawanie nowego wpisu dla określonego tematu"""
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(request, topic_id)

    if request.method != 'POST':
        #Nie przekazano żadnych danych, należy utworzyć pusty formularz.
        form = EntryForm()
    else:
        #Przekazano dane za pomocą żądania POST, należy je przetworzyć.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)
    # Wyswietlanie pustego formularza
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edycja istniejącego pliku"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_topic_owner(request, entry_id)

    if request.method != 'POST':
        # żądanie początkowe, wypełnianie formularza aktualną treścią wpisu.
        form = EntryForm(instance=entry)
    else:
        #Przekazano dane za pomocą żądania POST, należy je przetworzyć.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
    context = {'entry': entry, 'topic':topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)

#def check_topic_owner():
    #if topic.owner != request.user:
     #   raise Http404