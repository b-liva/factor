from django.http import JsonResponse
from django.shortcuts import render
from .models import SpecCommunications, ReqSpec
from .forms import SpecCmForm
import json


# Create your views here.
def speccm_vueadd(request):
    data = json.loads(request.body.decode('utf-8'))
    all_chats = []
    if request.method == 'POST':
        form_data = {}
        form_data['spec'] = data['spec']
        form_data['text'] = data['text']
        print(f"{data['text']} for sped {data['spec']}")
        form = SpecCmForm(data)
        if form.is_valid():
            print('form is valid')
            speccm_item = form.save(commit=False)
            # speccm_item.text = form_data['text']
            speccm_item.is_read = False
            # speccm_item.spec_id = form_data['spec']
            speccm_item.owner = request.user
            speccm_item.save()
        else:
            print(f"form is not valid: {form.errors}")
        chats = ReqSpec.objects.filter(is_active=True).get(pk=form_data['spec']).speccommunications_set.all()
        for c in chats:
            all_chats.append({
                'chat_txt': c.text,
                'chat_owner': c.owner.username,
                'dir': 'left' if c.owner.is_customer else 'right',

            })

    context = {
        'chats': all_chats,
    }
    return JsonResponse(context, safe=False)


def speccm_add(request):
    if request.method == 'POST':
        form = SpecCmForm(request.POST or None)
        if form.is_valid():
            speccm = form.save(commit=False)
            speccm.owner = request.user
            speccm.save()
            # redirect to somewhere...

    if request.method == 'GET':
        form = SpecCmForm()

    context = {
        'form': form,
    }
    return render(request, '', context)


def speccm_index(request):
    pass


def speccm_read(request):
    pass


def speccm_delete(request):
    pass


def speccm_report(request):
    pass


def get_chat(request):
    all_chats = []
    data = json.loads(request.body.decode('utf-8'))
    # spec_id = request.POST.get('spec')
    spec_id = data['spec']
    spec = ReqSpec.objects.filter(is_active=True).get(pk=spec_id)
    chats = spec.speccommunications_set.all()
    for c in chats:
        all_chats.append({
            'chat_txt': c.text,
            'chat_owner': c.owner.username,
            'dir': 'left' if c.owner.is_customer else 'right',
        })

    context = {
        'chats': all_chats,
    }
    return JsonResponse(context, safe=False)
