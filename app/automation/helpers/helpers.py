LOOKUP_STR = [
    '22KW-3000',
    '18.5KW-1500',
    '22KW-1500',
    '15KW-1000',
    '30KW-3000',
    '37KW-3000',
    '30KW-1500',
    '18.5KW-1000',
    '22KW-1000',
    '45KW-3000',
    '37KW-1500',
    '45KW-1500',
    '30KW-1000',
    '55KW-3000',
    '55KW-1500',
    '37KW-1000',
    '75KW-3000',
    '90KW-3000',
    '75KW-1500',
    '90KW-1500',
    '45KW-1000',
    '55KW-1000',
    '15KW-1500',
    '18.5KW-3000',
    '15KW-3000',
    '11KW-1500',
    '11KW-1000',
    '5.5KW-3000',
    '5.5KW-1500',
    '7.5KW-3000',
    '7.5KW-1500',
    '3.7KW-1000',
    '110KW-3000',
    '132KW-3000',
    '160KW-3000',
    '185KW-3000',
    '200KW-3000',
    '110KW-1500',
    '132KW-1500',
    '160KW-1500',
    '185KW-1500',
    '200KW-1500',
    '75KW-1000',
    '90KW-1000',
    '110KW-1000',
    '132KW-1000',
    '220KW-3000',
    '250KW-3000',
    '280KW-3000',
    '315KW-3000',
    '220KW-1500',
    '250KW-1500',
    '280KW-1500',
    '315KW-1500',
    '160KW-1000',
    '185KW-1000',
    '200KW-1000',
    '220KW-1000',
    '355KW-3000',
    '400KW-3000',
    '450KW-3000',
    '355KW-1500',
    '400KW-1500',
    '450KW-1500',
    '250KW-1000',
    '280KW-1000',
    '315KW-1000',
]


def spec_is_routine(spec):
    from decimal import Decimal
    spec_lookup_str = f"{Decimal(spec.kw).normalize()}KW-{spec.rpm}"
    if spec_lookup_str not in LOOKUP_STR:
        return False
    return True


def order_is_routine(order):
    specs = order.reqspec_set.all()
    for spec in specs:
        if not spec_is_routine(spec):
            return False
    return True
