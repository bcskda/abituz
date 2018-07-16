import re

reg_program_table = r'<table class="w100">([\s\S]*)</table>'
reg_program_entry = r'<tr>([\s\S]*?)</tr>'
reg_program_header = r'<!-- +--> +([\s\S]*?) \(.*?,.*?, (.*?) +</td>'
reg_program_entity_num = r'<a href="[\s\S]*?([0-9]+)'

reg_student_table = r'<table class="w100" id="ratingTable">([\s\S]*)</table>'
reg_student_or_group = r'<tr class="(throw|trPos|trPosBen)"([\s\S]*?)</tr>'
reg_student_group_name = r'<th .*?>\s+(.+)\s*?</th>'
reg_student_entry = r'<tr class="trPosBen"[\s\S]*?</tr>'
reg_student_fields = r'<td.*?>\s*([\s\S]*?)\s*</td>'
reg_student_score = r'<span[\s\S]*?class="sumMark"[\s\S]*?>([0-9]*?)</span>'


pat_program_table = re.compile(reg_program_table)
pat_program_entry = re.compile(reg_program_entry)
pat_program_header = re.compile(reg_program_header)
pat_program_entity_num = re.compile(reg_program_entity_num)

pat_student_table = re.compile(reg_student_table)
pat_student_or_group = re.compile(reg_student_or_group)
pat_student_group_name = re.compile(reg_student_group_name)
pat_student_entry = re.compile(reg_student_entry)
pat_student_fields = re.compile(reg_student_fields)
pat_student_score = re.compile(reg_student_score)
