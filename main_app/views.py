from django.shortcuts import render,redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

from .models import Finch, Seed
from .forms import FeedingForm

class FinchCreate(CreateView):
  model = Finch
  fields = '__all__'
  success_url = '/finches/{finch_id}'

# Create your views here.
# Define the home view
def home(request):
  # Include an .html file extension - unlike when rendering EJS templates
  return render(request, 'home.html')

def about(request):
  # Include an .html file extension - unlike when rendering EJS templates
  return render(request, 'about.html')

def finches_index(request):
  finches = Finch.objects.all()
  return render(request, 'finches/index.html', {
    'finches': finches
  })


class FinchCreate(CreateView):
  model = Finch
  fields = ['name', 'size', 'description', 'image_url']

class FinchUpdate(UpdateView):
  model = Finch
  # Let's disallow the renaming of a Finch by excluding the name field!
  fields = ['name', 'size', 'description', 'image_url']

class FinchDelete(DeleteView):
  model = Finch
  success_url = '/finches'


def add_feeding(request, finch_id):
  form = FeedingForm(request.POST)
  if form.is_valid():
    new_feeding = form.save(commit=False)
    new_feeding.finch_id = finch_id
    new_feeding.save()
  return redirect('detail', finch_id=finch_id)

def assoc_seed(request, finch_id, seed_id):
  Finch.objects.get(id=finch_id).seeds.add(seed_id)
  return redirect('detail', finch_id=finch_id)

def disassoc_seed(request, finch_id, seed_id):
  Finch.objects.get(id=finch_id).seeds.remove(seed_id)
  return redirect('detail', finch_id=finch_id)

def finches_detail(request, finch_id):
  finch = Finch.objects.get(id=finch_id)
  id_list = finch.seeds.all().values_list('id')
  seeds_finch_doesnt_have = Seed.objects.exclude(id__in=id_list)
  feeding_form = FeedingForm()
  return render(request, 'finches/detail.html', { 
    'finch': finch,
    'feeding_form': feeding_form,
    'seeds': seeds_finch_doesnt_have
    })

class SeedList(ListView):
  model = Seed

class SeedDetail(DetailView):
  model = Seed

class SeedCreate(CreateView):
  model = Seed
  fields = '__all__'

class SeedUpdate(UpdateView):
  model = Seed
  fields = ['name', 'color']

class SeedDelete(DeleteView):
  model = Seed
  success_url = '/seeds'
