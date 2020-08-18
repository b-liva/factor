from django.db.models.functions.datetime import TruncBase, TimezoneMixin

from datetime import datetime

from django.conf import settings
from django.db.models import (
    DateField, DateTimeField, DurationField, Field, IntegerField, TimeField,
    Transform,
)
from django.db.models.lookups import (
    YearExact, YearGt, YearGte, YearLt, YearLte,
)
from django.utils import timezone


class MyTruncBase(TimezoneMixin, Transform):
    kind = None
    tzinfo = None

    def __init__(self, expression, output_field=None, tzinfo=None, **extra):
        self.tzinfo = tzinfo
        print('init', expression)
        super().__init__(expression, output_field=output_field, **extra)

    def as_sql(self, compiler, connection):
        print('as sql')
        inner_sql, inner_params = compiler.compile(self.lhs)
        # Escape any params because trunc_sql will format the string.
        inner_sql = inner_sql.replace('%s', '%%s')
        print(inner_sql, inner_params)
        if isinstance(self.output_field, DateTimeField):
            print('datetimeField')
            tzname = self.get_tzname()
            sql = connection.ops.datetime_trunc_sql(self.kind, inner_sql, tzname)
        elif isinstance(self.output_field, DateField):
            print('dateField')
            sql = connection.ops.date_trunc_sql(self.kind, inner_sql)
        elif isinstance(self.output_field, TimeField):
            print('TimeField')
            sql = connection.ops.time_trunc_sql(self.kind, inner_sql)
        else:
            raise ValueError('Trunc only valid on DateField, TimeField, or DateTimeField.')
        print('assql: ', sql, inner_params)
        return sql, inner_params

    def resolve_expression(self, query=None, allow_joins=True, reuse=None, summarize=False, for_save=False):
        print('resolve exp')
        copy = super().resolve_expression(query, allow_joins, reuse, summarize, for_save)
        field = copy.lhs.output_field
        # DateTimeField is a subclass of DateField so this works for both.
        assert isinstance(field, (DateField, TimeField)), (
            "%r isn't a DateField, TimeField, or DateTimeField." % field.name
        )
        # If self.output_field was None, then accessing the field will trigger
        # the resolver to assign it to self.lhs.output_field.
        if not isinstance(copy.output_field, (DateField, DateTimeField, TimeField)):
            raise ValueError('output_field must be either DateField, TimeField, or DateTimeField')
        # Passing dates or times to functions expecting datetimes is most
        # likely a mistake.
        class_output_field = self.__class__.output_field if isinstance(self.__class__.output_field, Field) else None
        output_field = class_output_field or copy.output_field
        has_explicit_output_field = class_output_field or field.__class__ is not copy.output_field.__class__
        if type(field) == DateField and (
                isinstance(output_field, DateTimeField) or copy.kind in ('hour', 'minute', 'second', 'time')):
            raise ValueError("Cannot truncate DateField '%s' to %s. " % (
                field.name, output_field.__class__.__name__ if has_explicit_output_field else 'DateTimeField'
            ))
        elif isinstance(field, TimeField) and (
                isinstance(output_field, DateTimeField) or copy.kind in ('year', 'quarter', 'month', 'day', 'date')):
            raise ValueError("Cannot truncate TimeField '%s' to %s. " % (
                field.name, output_field.__class__.__name__ if has_explicit_output_field else 'DateTimeField'
            ))
        print('copy rexolve exp: ', copy)
        return copy

    def convert_value(self, value, expression, connection):
        print('convert value', value, expression, connection)
        print(type(value))
        if isinstance(self.output_field, DateTimeField):
            print('01')
            if settings.USE_TZ:
                if value is None:
                    raise ValueError(
                        "Database returned an invalid datetime value. "
                        "Are time zone definitions for your database installed?"
                    )
                value = value.replace(tzinfo=None)
                value = timezone.make_aware(value, self.tzinfo)
        elif isinstance(value, datetime):
            print('02')
            if isinstance(self.output_field, DateField):
                value = value.date()
            elif isinstance(self.output_field, TimeField):
                value = value.time()
        return value


class MyTruncMonth(MyTruncBase):
    kind = 'month'
