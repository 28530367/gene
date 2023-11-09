import pandas as pd

# 创建示例DataFrame
data = {'column_name': ['Hello', 'World', 'Python', 'Pandas']}
df = pd.DataFrame(data)

# 自定义函数用于颠倒字符串
def reverse_string(s):
    return s[::-1]

# 在列上应用自定义函数
df['column_name'] = df['column_name'].apply(reverse_string)

# 显示结果
print(df)
