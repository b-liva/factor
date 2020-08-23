from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from jfeature.models import Feature
from jfeature.forms import FeatureForm


# Create your views here.
@login_required
def upsert(request, fid=None):
    if fid:
        feature = get_object_or_404(Feature, pk=fid)
    else:
        feature = Feature()

    if request.method == 'POST':
        form = FeatureForm(request.POST or None, instance=feature)

        if form.is_valid():
            feature_obj = form.save(commit=False)
            feature_obj.owner = request.user
            feature_obj.save()
            messages.add_message(request, level=messages.SUCCESS, message='درخواست با موفقیت ثبت گردید.')
            return redirect('feature:create')
        else:
            messages.error(request, 'بروز خطا، داده ثبت نشد.')
            return redirect('feature:create')
    else:
        form = FeatureForm(instance=feature)

    features = Feature.objects.all()
    context = {
        'form': form,
        'features': features
    }
    return render(request, 'jfeature/edit_or_create.html', context)
