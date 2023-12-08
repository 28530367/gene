from django.test import TestCase

# Create your tests here.

number = 0.00000123456789

# 使用 format 函数
scientific_notation_format = '{:.3e}'.format(number)
print(scientific_notation_format)

# 使用 f-string
scientific_notation_fstring = f'{number:.3e}'
print(scientific_notation_fstring)