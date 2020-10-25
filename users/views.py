from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def register(request):
    """Rejestracja nowego użytkownika"""
    if request.method != 'POST':
        #Wyswietlenie pustego formularza rejestracji uzytkownika.
        form = UserCreationForm()
    else:
        #Przetworzenie wypełnionego formularza
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            # zalogowanie użytkownika, a następnie przekierownie go na stronę główną.
            return redirect('learning_logs:index')
    #wyswietlenie pustego formularza.
    context = {'form': form}
    return render(request, 'registration/register.html', context)