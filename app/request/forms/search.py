from django import forms
from django_jalali import forms as jforms
from django.contrib.auth import get_user_model
User = get_user_model()
import django.db.utils


def prepare_owner_choices():
    # this is the format.
    # owner_choices = (
    #     (0, '---',),
    #     (2, 'محمدی',),
    #     (3, 'علوی',),
    #     (4, 'ظریف',),
    # )

    owner_choices = ((0, '---'),)
    try:

        exps = User.objects.filter(sales_exp=True)
        users = [(u.pk, u.last_name) for u in exps]
        owner_choices = list(owner_choices)
        owner_choices.extend(users)
        owner_choices = tuple(owner_choices)
    except:
        owner_choices = []

    return owner_choices


class SpecSearchForm(forms.Form):
    def file(self):
        pass

    customer_name = forms.CharField(label='مشتری', max_length=100, required=False)
    customer_name.widget = forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'autocomplete'
    })
    # rpm = forms.CheckboxSelectMultiple()

    date_min = jforms.jDateField(label='زمان(از)', required=False)
    date_min.widget = jforms.jDateInput(attrs={
        'id': 'date_fa_start',
        'autocomplete': 'off',
        'class': 'form-control',
    })
    date_max = jforms.jDateField(label='زمان(تا)', required=False)
    date_max.widget = jforms.jDateInput(attrs={
        'id': 'date_fa_end',
        'autocomplete': 'off',
        'class': 'form-control',
    })

    kw_min = forms.FloatField(label='کیلووات(از)', max_value=10000, required=False)
    kw_min.widget = forms.TextInput(attrs={
        'class': 'form-control',
    })
    kw_max = forms.FloatField(label='کیلووات(تا)', max_value=10000, required=False)
    kw_max.widget = forms.TextInput(attrs={
        'class': 'form-control',
    })
    rpm = forms.IntegerField(label='سرعت', max_value=3001, required=False)
    rpm.widget = forms.TextInput(attrs={
        'class': 'form-control'
    })
    # price = forms.BooleanField(label='مالی', required=False)
    # price.widget = forms.CheckboxInput()
    # tech = forms.BooleanField(label='فنی', required=False)
    # tech.widget = forms.CheckboxInput()
    # permission = forms.BooleanField(label='مجوز', required=False)
    # permission.widget = forms.CheckboxInput()
    # sent = forms.BooleanField(label='ارسال شده', required=False)
    # sent.widget = forms.CheckboxInput()
    PRICE_CHOICES = (
        ('0', '---',),
        ('True', 'بله',),
        ('False', 'خیر',),
    )
    SENT_CHOICES = (
        ('0', '---',),
        ('True', 'بله',),
        ('False', 'خیر',),
    )
    PERMISSION_CHOICES = (
        ('0', '---',),
        ('True', 'بله',),
        ('False', 'خیر',),
    )
    TECH_CHOICES = (
        ('0', '---',),
        ('True', 'بله',),
        ('False', 'خیر',),
    )
    TYPE_CHOICES = (
        ('0', '---',),
        ('روتین', 'روتین',),
        ('پروژه', 'پروژه',),
        ('تعمیرات', 'تعمیرات',),
        ('ضد انفجار', 'ضد انفجار',),
    )
    CHOICES = (
        ('0', '---',),
        ('True', 'بله',),
        ('False', 'خیر',),
    )
    OWNER = (
        ('0', '---',),
        ('2', 'محمدی',),
        ('3', 'علوی',),
        ('4', 'ظریف',),
    )
    ITEM_PER_PAGE = (
        ('50', '50',),
        ('100', '100',),
    )
    price = forms.ChoiceField(widget=forms.Select(attrs={
        'class': 'form-control',
    }), choices=CHOICES, required=False)
    tech = forms.ChoiceField(widget=forms.Select(attrs={
        'class': 'form-control',
    }), choices=CHOICES, required=False)
    permission = forms.ChoiceField(widget=forms.Select(attrs={
        'class': 'form-control',
    }), choices=CHOICES, required=False)
    sent = forms.ChoiceField(widget=forms.Select(attrs={
        'class': 'form-control',
    }), choices=CHOICES, required=False)
    owner = forms.ChoiceField(widget=forms.Select(attrs={
        'class': 'form-control',
    }), choices=OWNER, required=False)
    type = forms.ChoiceField(widget=forms.Select(attrs={
        'class': 'form-control',
    }), choices=TYPE_CHOICES, required=False)
    item_per_page = forms.ChoiceField(widget=forms.Select(attrs={
        'class': 'form-control',
    }), choices=ITEM_PER_PAGE, required=False)

    SORT_CHOICES = (
        ('1', 'کیلووات',),
        # ('2', 'customer',),
        ('3', 'تاریخ',),
        ('4', 'تعداد',),
    )

    sort_asc_dsc = (
        (1, 'صعودی',),
        (2, 'نزولی',),
    )
    sort_by = forms.ChoiceField(widget=forms.Select(attrs={
        'class': 'form-control',
    }), choices=SORT_CHOICES, required=False)

    dsc_asc = forms.ChoiceField(widget=forms.Select(attrs={
        'class': 'form-control',
    }), choices=sort_asc_dsc, required=False)


class ReqSearchForm(forms.Form):
    customer_name = forms.CharField(label='مشتری', max_length=100, required=False)
    customer_name.widget = forms.TextInput(attrs={'class': 'form-control', 'id': 'autocomplete'})
    date_min = jforms.jDateField(label='تاریخ(از)', required=False)
    date_min.widget = jforms.jDateInput(attrs={'id': 'date_fa_start', 'autocomplete': 'off', 'class': 'form-control', })
    date_max = jforms.jDateField(label='تاریخ(تا)', required=False)
    date_max.widget = jforms.jDateInput(attrs={
        'id': 'date_fa_end',
        'autocomplete': 'off',
        'class': 'form-control',})
    CHOICES = (
        ('0', '---',),
        ('no_prof', 'بدون پیش فاکتور',),
        ('close', 'بسته',),
        ('open', 'باز',),
        ('to_follow', 'اولویت پیگیری',),
    )

    status = forms.ChoiceField(
        label='وضعیت',
        widget=forms.Select(attrs={
        'class': 'form-control',
    }), choices=CHOICES, required=False)

    SORT_CHOICES = (
        # ('1', 'کیلووات',),
        ('date_fa', 'تاریخ',),
        ('number', 'شماره درخواست',),
        # ('4', 'تعداد',),
    )

    sort_asc_dsc = (
        (1, 'نزولی',),
        (2, 'صعودی',),
    )
    sort_by = forms.ChoiceField(
        label='مرتب سازی',
        widget=forms.Select(attrs={
        'class': 'form-control',
    }), choices=SORT_CHOICES, required=False)

    dsc_asc = forms.ChoiceField(
        label='اولویت',
        widget=forms.Select(attrs={
        'class': 'form-control',
    }), choices=sort_asc_dsc, required=False)

    owner_choices = (
        (0, '---',),
        (2, 'محمدی',),
        (3, 'علوی',),
        (4, 'ظریف',),
    )

    owner = forms.ChoiceField(
        label='کارشناس',
        widget=forms.Select(attrs={
        'class': 'form-control',
    }), choices=owner_choices, required=False)


class ProformaSearchForm(forms.Form):

    customer_name = forms.CharField(label='مشتری', max_length=100, required=False)
    customer_name.widget = forms.TextInput(attrs={'class': 'form-control', 'id': 'autocomplete'})
    date_min = jforms.jDateField(label='تاریخ(از)', required=False)
    date_min.widget = jforms.jDateInput(attrs={'id': 'date_fa_start', 'autocomplete': 'off', 'class': 'form-control', })
    date_max = jforms.jDateField(label='تاریخ(تا)', required=False)
    date_max.widget = jforms.jDateInput(attrs={
        'id': 'date_fa_end',
        'autocomplete': 'off',
        'class': 'form-control', })
    CHOICES = (
        ('0', '---',),
        ('expired', 'منقضی',),
        ('valid', 'معتبر',),
        ('perm', 'مجوز',),
        ('to_follow', 'اولویت پیگیری',),
    )
    ITEM_PER_PAGE = (
        ('50', '50',),
        ('100', '100',),
    )

    status = forms.ChoiceField(
        label='وضعیت',
        widget=forms.Select(attrs={
            'class': 'form-control',
        }), choices=CHOICES, required=False)

    SORT_CHOICES = (
        # ('1', 'کیلووات',),
        # ('customer', 'مشتری',),
        ('date_fa', 'تاریخ',),
        ('number', 'شماره',),
        # ('4', 'تعداد',),
    )

    sort_asc_dsc = (
        (1, 'نزولی',),
        (2, 'صعودی',),
    )
    sort_by = forms.ChoiceField(
        label='مرتب سازی',
        widget=forms.Select(attrs={
            'class': 'form-control',
        }), choices=SORT_CHOICES, required=False)

    dsc_asc = forms.ChoiceField(
        label='اولویت',
        widget=forms.Select(attrs={
            'class': 'form-control',
        }), choices=sort_asc_dsc, required=False)

    owner_choices = prepare_owner_choices()

    owner = forms.ChoiceField(
        label='کارشناس',
        widget=forms.Select(attrs={
            'class': 'form-control',
        }), choices=owner_choices, required=False)

    item_per_page = forms.ChoiceField(
        label='تعداد',
        widget=forms.Select(attrs={
            'class': 'form-control',
        }), choices=ITEM_PER_PAGE, required=False)


class PermSearchForm(ProformaSearchForm):
    SORT_CHOICES = (
        ('due_date', 'تاخیر',),
        ('qty_remaining', 'مانده مجوز',),
        ('number', 'شماره پیش فاکتور',),
        ('perm_number', 'شماره مجوز',),
    )
    sort_asc_dsc = (
        (1, 'صعودی',),
        (2, 'نزولی',),
    )
    sort_by = forms.ChoiceField(
        label='مرتب سازی',
        widget=forms.Select(attrs={
            'class': 'form-control',
        }), choices=SORT_CHOICES, required=False)
    dsc_asc = forms.ChoiceField(
        label='اولویت',
        widget=forms.Select(attrs={
            'class': 'form-control',
        }), choices=sort_asc_dsc, required=False)
    CHOICES = (
        ('0', '---',),
        ('complete', 'تحویل شده',),
        ('not_complete', 'مانده',),

    )
    status = forms.ChoiceField(
        label='وضعیت',
        widget=forms.Select(attrs={
            'class': 'form-control',
        }), choices=CHOICES, required=False)


class PrefSpecSearchForm(PermSearchForm):
    SORT_CHOICES = (
        ('xpref_id__date_fa', 'تاریخ',),
        # ('xpref_id__perm_date', 'تاریخ',),
        ('kw', 'کیلووات',),
        ('qty_remaining', 'مانده',),
        ('xpref_id__req_id__number', 'شماره درخواست',),
        ('xpref_id__number', 'شماره پیش فاکتور',),
        ('xpref_id__perm_number', 'شماره مجوز',),
    )
    sort_by = forms.ChoiceField(
        label='مرتب سازی',
        widget=forms.Select(attrs={
            'class': 'form-control',
        }), choices=SORT_CHOICES, required=False)

    kw_min = forms.FloatField(label='کیلووات(از)', max_value=10000, required=False)
    kw_min.widget = forms.TextInput(attrs={
        'class': 'form-control',
    })
    kw_max = forms.FloatField(label='کیلووات(تا)', max_value=10000, required=False)
    kw_max.widget = forms.TextInput(attrs={
        'class': 'form-control',
    })
    rpm = forms.IntegerField(label='سرعت', max_value=3001, required=False)
    rpm.widget = forms.TextInput(attrs={
        'class': 'form-control'
    })

    PROJECT_TYPE_CHOICES = (
        ('0', '---',),
        ('روتین', 'روتین',),
        ('پروژه', 'پروژه',),
        ('ضد انفجار', 'ضدانفجار',),
        ('تعمیرات', 'خدمات پس از فروش',),
        ('سایر', 'سایر',),

    )
    project_type = forms.ChoiceField(
        label='نوع پروژه',
        widget=forms.Select(attrs={
            'class': 'form-control',
        }), choices=PROJECT_TYPE_CHOICES, required=False)


