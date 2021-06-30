from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import MealModelForm
from .models import Meal

# Create your views here.
@login_required
def meal_create_view(request):
    # request.user -> return something
    form = MealModelForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        form = MealModelForm()
    template_name = 'form.html'
    context = {'form': form}
    return render(request, template_name, context)

@login_required
def meal_update_view(request, pk=None):
    obj = None
    if pk:
        obj = get_object_or_404(Meal, pk=pk)
    form = MealModelForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
    template_name = 'form.html'
    context = {"title": f"Update {obj.name}", "form": form}
    if pk:
        context['obj'] = obj
    return render(request, template_name, context)

@login_required
def meal_list_view(request):
    qs = Meal.objects.all().order_by('-created')
    template_name = 'meals/list.html'
    context = {'object_list': qs}
    return render(request, template_name, context)

@login_required
def meal_delete_view(request, pk):
    obj = get_object_or_404(Meal, pk=pk)
    template_name = 'meals/delete.html'
    if request.method == "POST":
        obj.delete()
        return redirect("/meals")
    context = {"object": obj}
    return render(request, template_name, context)


