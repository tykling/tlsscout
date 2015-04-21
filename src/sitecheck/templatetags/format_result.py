from django import template
from collections import Iterable
from django.template.loader import render_to_string
register = template.Library()

@register.filter
def format_result(value):
    if not isinstance(value, Iterable):
        value = [value]
    output = ""
    for result in value:
        if result.grade == "A+":
            formatdict = {
                'gradenumber': 8,
                'headline': 'Messages for %s' % result.serverip,
                'labelclass': 'label-success',
                'grade': result.grade,
            }
        elif result.grade == "A":
            formatdict = {
                'gradenumber': 7,
                'headline': 'Messages for %s' % result.serverip,
                'labelclass': 'label-success',
                'grade': result.grade,
            }
        elif result.grade == "A-":
            formatdict = {
                'gradenumber': 6,
                'headline': 'Messages for %s' % result.serverip,
                'labelclass': 'label-success',
                'grade': result.grade,
            }
        elif result.grade == "B":
            formatdict = {
                'gradenumber': 5,
                'headline': 'Messages for %s' % result.serverip,
                'labelclass': 'label-warning',
                'grade': result.grade,
            }
        elif result.grade == "C":
            formatdict = {
                'gradenumber': 4,
                'headline': 'Messages for %s' % result.serverip,
                'labelclass': 'label-warning',
                'grade': result.grade,
            }
        elif result.grade == "D":
            formatdict = {
                'gradenumber': 3,
                'headline': 'Messages for %s' % result.serverip,
                'labelclass': 'label-danger',
                'grade': result.grade,
            }
        elif result.grade == "E":
            formatdict = {
                'gradenumber': 2,
                'headline': 'Messages for %s' % result.serverip,
                'labelclass': 'label-danger',
                'grade': result.grade,
            }
        elif result.grade == "F":
            formatdict = {
                'gradenumber': 1,
                'headline': 'Messages for %s' % result.serverip,
                'labelclass': 'label-danger',
                'grade': result.grade,
            }
        else:
            if result.status_message and result.status_message != "":
                formatdict = {
                    'gradenumber': 0,
                    'headline': 'Error Message for %s' % result.serverip,
                    'labelclass': 'label-default',
                    'grade': result.grade,
                    'comments': result.status_message,
                }
            else:
                ### no results or comments yet
                continue

        if 'comments' not in formatdict:
            formatdict['comments'] = "No comments"
        output += render_to_string('includes/format_result.html', formatdict)
    return output

