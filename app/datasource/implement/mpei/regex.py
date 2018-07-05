import re

reg_time = r'\(данные на (.*?)\)'
"""Matches last update time"""

reg_exam = r'<td class="parName">(.*?)</td>'
"""Matches required exam`s name"""

reg_table = r'<div class="title2">(.*?)</div><table class="thin-grid competitive-group-table"[\s\S]*?</table>'
"""Matches the beginning of the competitive table.
Capturing group 1 contains the enrollment group.
"""

reg_student = r'<tr>(.*?)</tr>\n?'
"""Matches a student described by a <table> line"""

reg_fields = r'<td.*?>(.*?)</td>'
"""Matches a field in student`s description"""

pat_time = re.compile(reg_time)
pat_exam = re.compile(reg_exam)
pat_table = re.compile(reg_table)
pat_student = re.compile(reg_student)
pat_field = re.compile(reg_fields)