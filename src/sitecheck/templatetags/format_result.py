from django import template
from collections import Iterable
register = template.Library()

@register.filter
def format_result(value):
    if not isinstance(value, Iterable):
        value = [value]
    output = ""
    for result in value:
        if result.grade == "A+":
            labelclass="label-success"
        elif result.grade == "A":
            labelclass="label-success"
        elif result.grade == "A-":
            labelclass="label-success"
        elif result.grade == "B":
            labelclass="label-warning"
        elif result.grade == "C":
            labelclass="label-warning"
        elif result.grade == "D":
            labelclass="label-danger"
        elif result.grade == "E":
            labelclass="label-danger"
        elif result.grade == "F":
            labelclass="label-danger"
        else:
            labelclass="label-default"
            result.grade = "<i class='fa fa-frown-o'></i>"
            if result.status_message and result.status_message != "":
                output += "<div style='font-size: 36px'><span data-content='%s' data-placement='right' data-original-title='Error Message' data-trigger='hover click' class='popoverlabel label %s'>%s</span></div>" % (result.status_message, labelclass, result.grade)
                continue
        output += "<div style='font-size: 36px'><span class='label %s'>%s</span></div>" % (labelclass, result.grade)
    return output

