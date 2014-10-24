# -*- coding: utf-8 -*-
from datetime import datetime

def integrate(y_values, h):
    """ Returns the area under a curve using Simpson's rule

    Keyword arguments:
    y_vals -- measures
    h -- gaps between measures
    """
    if len(y_values) < 2:
        return 0.0
    i = 1
    total = y_values[0] + y_values[-1]
    for y in y_values[1:-1]:
        if i % 2 == 0:
            total += 2 * y
        else:
            total += 4 * y
        i += 1
    return total * (h / 3.0)


def get_sec(s):
    l = map(int, s.split(':'))
    return sum(n * sec for n, sec in zip(l[::-1], (1, 60, 3600)))
    
def get_todays_date():
    return datetime.now().date()