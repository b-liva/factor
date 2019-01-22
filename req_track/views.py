from django.shortcuts import render, redirect
from request.models import Requests
from req_track.models import ReqEntered
from .forms import E_Req_Form

# Create your views here.


def e_req_add(request):

    if request.method == 'POST':
        form = E_Req_Form(request.POST or None)
        if form.is_valid():
            ereq_item = form.save(commit=False)
            # if Requests.objects.get(number=request.POST['number']):
            #     ereq_item.started = True
            ereq_item.save()
            return redirect('e_req_index')
    if request.method == 'GET':
        form = E_Req_Form()

    context = {
        'form': form,
    }
    return render(request, 'req_track/add_form.html', context)


def e_req_index(request):
    reqs = ReqEntered.objects.all()
    context = {
        'reqs': reqs,
    }
    return render(request, 'req_track/ereq_notstarted.html', context)


def e_req_read(request):
    pass


def e_req_delete(request):
    pass


def e_req_delete_all(request):
    ereq_all = ReqEntered.objects.all()
    for e in ereq_all:
        e.delete()

    return redirect('e_req_index')




def e_req_report(request):
    reqs = ReqEntered.objects.filter(is_entered=False).filter(is_request=True)

    context = {
        'reqs': reqs,
    }
    return render(request, 'req_track/ereq_notstarted.html', context)



def check_orders(request):
    ereqs = ReqEntered.objects.filter(is_entered=False)
    for e in ereqs:
        if Requests.objects.filter(number=e.number_automation):
            print(f"order No: {e.number_automation}: is entered.")
            e.is_entered = True
            e.save()
        else:
            print(f"order No: {e.number_automation}: is not entered.")

    return redirect('e_req_report')
