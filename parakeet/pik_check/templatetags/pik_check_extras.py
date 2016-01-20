from django import template
from datetime import timedelta

register = template.Library()


@register.filter(name='naturaldelta')
def naturalTimeDelta(delta):
    """
    Returns appropriate humanized form for a timedelta
    """
    if isinstance(delta, timedelta):
        ret = ''
        if delta.days:
            if delta.days == 1:
                ret += ' 1 day'
            else:
                ret = '{0} {1!s} days'.format(ret, delta.days)
            delta = delta - timedelta(days=delta.days)
        if delta.seconds / 3600:
            hours = delta.seconds / 3600
            delta = delta - timedelta(hours=hours)
            if hours == 1:
                ret += ' 1 hour'
            else:
                ret = '{0} {1!s} hours'.format(ret, hours)
        if delta.seconds / 60:
            minutes = delta.seconds / 60
            delta = delta - timedelta(minutes=minutes)
            if minutes == 1:
                ret += ' 1 minute'
            else:
                ret = '{0} {1!s} minutes'.format(ret, minutes)
        if delta.seconds:
            if delta.seconds == 1:
                ret += ' 1 second'
            else:
                ret = '{0} {1!s} seconds'.format(ret, delta.seconds)

        return ' '.join(ret.split())  # remove extra whitespace
    else:
        return str(delta)
