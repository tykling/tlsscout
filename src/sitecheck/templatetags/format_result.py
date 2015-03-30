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
            gradenumber = 8
        elif result.grade == "A":
            labelclass="label-success"
            gradenumber = 7
        elif result.grade == "A-":
            labelclass="label-success"
            gradenumber = 6
        elif result.grade == "B":
            labelclass="label-warning"
            gradenumber = 5
        elif result.grade == "C":
            labelclass="label-warning"
            gradenumber = 4
        elif result.grade == "D":
            labelclass="label-danger"
            gradenumber = 3
        elif result.grade == "E":
            labelclass="label-danger"
            gradenumber = 2
        elif result.grade == "F":
            labelclass="label-danger"
            gradenumber = 1
        else:
            labelclass="label-default"
            gradenumber = 0
            result.grade = "X"
            if result.status_message and result.status_message != "":
                output += "<span style='display: none'>%s</span><span style='font-size: 36px'><span data-content='%s' data-placement='right' data-original-title='Error Message' data-trigger='hover click' class='popoverlabel label %s'>%s</span></span>&nbsp;" % (gradenumber, result.status_message, labelclass, result.grade)
                continue
        output += "<span style='display: none'>%s</span><span style='font-size: 36px'><span class='label %s'>%s</span></span>&nbsp;" % (gradenumber, labelclass, result.grade)
    return output

