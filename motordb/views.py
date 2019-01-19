import operator
from functools import reduce

from django.db.models import Q
from django.shortcuts import render, redirect
from motordb import forms
from motordb import models


# Create your views here.


def motordb_index(request):

    motors = models.Motors.objects.all().order_by('pk').reverse()

    return render(request, 'motordb/index.html', {'motors': motors})


def motor_view(request):
    form = forms.Motors()

    if request.method == 'POST':
        form = forms.Motors(request.POST)

        if form.is_valid():
            print('validation success...')
            print('kw: ' + str(form.cleaned_data['kw']))
            print('speed: ' + str(form.cleaned_data['speed']))

    return render(request, 'motordb/form_page.html', {'form': form})


def test_view(request):
    form = forms.FormTest()
    if request.method == 'POST':
        form = forms.FormTest(request.POST)

        if form.is_valid():
            print('validation success...')
            print('Name: ' + str(form.cleaned_data['name']))
            print('Email: ' + str(form.cleaned_data['email']))
            print('Verification: ' + str(form.cleaned_data['verify_email']))
            print('Text: ' + str(form.cleaned_data['text']))

    return render(request, 'motordb/form_page.html', {'form': form})


def test_view2(request, motordb_pk=None):
    form = forms.MotorsForm()
    if not motordb_pk:
        if request.method == 'POST':
            form = forms.MotorsForm(request.POST)
            if form.is_valid():
                form.save(commit=True)
                return motordb_index(request)
            else:
                print('error: form invalid')
    if motordb_pk:
        motor = models.Motors.objects.get(pk=motordb_pk)
        form = forms.MotorsForm(instance=motor)
        form.save()

    return render(request, 'motordb/form_page.html', {'form': form})


def motordb_form(request):
    pass


def motordb_insert(request):
    pass


def motordb_find(request):
    pass


def motordb_details(request):
    pass


def motordb_delete(request, motordb_pk):
    delete = input('do you want to delete this ? (Y/N)')
    if delete == 'Y' or delete == 'y':
        motor = models.Motors.objects.get(pk=motordb_pk)
        motor.delete()
    return redirect('motordb_index')


def motordb_edit_form(request, motordb_pk):
    # edit = input('do you want to edit this ? (Y/N)')
    # if edit == 'Y':
    motor = models.Motors.objects.get(pk=motordb_pk)
    print(motor.get_kw_display())
    form = forms.MotorsForm(instance=motor)
    return render(request, 'motordb/form_page_edit.html', {
        'form': form,
        'motor': motor
    })


def motordb_edit(request, motordb_pk):
    motor_instance = models.Motors.objects.get(pk=motordb_pk)

    form = forms.MotorsForm(request.POST or None, instance=motor_instance)
    if form.is_valid():
        form.save(commit=True)
        return motordb_index(request)
    else:
        print('error: form invalid')


def del_all_motors(request):
    motors = models.Motors.objects.all()
    print(motors)
    for motor in motors:
        motor.delete()
    return redirect('motordb_index')


def motordb_search_form(request):
    filter_items = ('kw', 'speed', 'voltage')
    kwargs = {}
    if request.POST:
        for filter in filter_items:
            if request.POST[filter]:
                kwargs[filter] = request.POST[filter]

    motor = models.Motors.objects.all()

    motor_instance = forms.MotorsForm()
    return render(request, 'motordb/search.html', {
        'motors': motor,
        'motor_instance': motor_instance,
    })


def motordb_search(request):
    filter_items = ('kw', 'speed', 'voltage')

    kwargs = {}
    motor_instance = forms.MotorsForm()

    for filter in filter_items:
        if request.POST[filter]:
            kwargs[filter] = request.POST[filter]
            motor_instance.fields[filter].initial = request.POST[filter]
        else:
            motor_instance.fields[filter].initial = None

    motors = models.Motors.objects.filter(**kwargs)
    # motor_instance = forms.SearchForm()
    context = {
        'motors': motors,
        'motor_instance': motor_instance,
    }
    return render(request, 'motordb/search.html', context)


## drafts:
# motors = models.Motors.objects\
#         .filter(kw=request.POST['kw']).filter(speed=request.POST['speed']).filter(voltage=request.POST['voltage'])
#     m = models.Motors.objects.all()
#     queryset = models.Motors.objects.all()
#
#
#     filter_clauses = [Q(filter=request.POST[filter])
#                       for filter in filter_items
#                       if request.POST[filter]]
#
#     fil = []
#
#     kwargs = {
#         'kw': 1,
#         'speed': 2
#     }
#
#     mt = models.Motors.objects.filter(**kwargs)
#     if request.POST[filter]:
    #         fil.append(Q(filter=request.POST[filter]))
    # print('****')
    # print(fil)

    # print(filter_clauses)

    # if filter_clauses:
    #     queryset = queryset.filter(reduce(operator.and_, filter_clauses))

    # print(queryset)

    # for f in filter_items:
    #     # print(f)
    #     # print(request.POST[f])
    #     if request.POST[f]:
    #         # print(m)
    #         m = m.filter(request.POST[f])
    #         print(m)

    # motors = m.all()