from django.shortcuts import render, redirect
from .forms import RegisterForm, NoteForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from .models import Note
from django.shortcuts import get_object_or_404

@login_required(login_url='/login')
def home(request):
    notes = Note.objects.all()

    if request.method == "POST":
        delete_note_id = request.POST.get('delete-note-id')
        open_note_id = request.POST.get('open-note-id')

        if delete_note_id:
            note = Note.objects.filter(id=delete_note_id).first()
            if note and (note.author == request.user or request.user.has_perm("backend.delete_note")):
                note.delete()
        elif open_note_id:
            note = Note.objects.get(id=open_note_id)
            if note and (note.author == request.user or request.user.has_perm("backend.change_note")):
                return redirect('open_note', id=open_note_id) 
                

    notes = [note for note in notes if note.author == request.user]

    return render(request, 'backend/home.html', {"notes": notes})

@login_required(login_url='/login')
@permission_required("backend.add_note", login_url='/home', raise_exception=True)
def create_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.author = request.user
            note.save()
            return redirect('/home')
    else:
        form = NoteForm()

    return render(request, 'backend/create_note.html', {"form": form})

@login_required(login_url='/login')
@permission_required("backend.change_note", login_url='/home', raise_exception=True)
def open_note(request, id):
    note = get_object_or_404(Note, id=id, author=request.user)  # Fetch the note

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            note.save()
            return redirect('/home')
    else:
        form = NoteForm(instance=note)

    return render(request, 'backend/open_note.html', {"form": form})

def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('/home')
    else:
        form = RegisterForm()
    return render(request, 'registration/sign_up.html', {"form": form})

