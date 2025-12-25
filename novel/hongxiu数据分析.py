import jieba
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import plotly.express as px

# 读取数据
df = pd.read_csv('book.csv')

# 数据清洗
# 转换字数为浮点数（万）
df['字数'] = df['字数'].str.replace('万', '').astype(float)

# ------------ 可视化设置 ------------
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题


# ------------ 分类分布（前10）------------
plt.figure(figsize=(12,6))
category_counts = df['分类'].value_counts().head(10)
sns.barplot(x=category_counts.values, y=category_counts.index, palette='viridis')
plt.title('小说分类TOP10分布')
plt.xlabel('数量')
plt.ylabel('分类')
plt.tight_layout()
plt.savefig('分类分布（前10）.png')
plt.show()

# ------------ 字数分布）------------
plt.figure(figsize=(10,6))
sns.histplot(df['字数'], bins=20, kde=True)
plt.title('小说字数分布')
plt.xlabel('字数（万）')
plt.ylabel('数量')
plt.savefig('字数分布.png')
plt.show()

# ------------ 状态分布 ------------
plt.figure(figsize=(6,6))
status_counts = df['状态'].value_counts()
plt.pie(status_counts, labels=status_counts.index,
        autopct='%1.1f%%', startangle=90)
plt.title('作品状态比例')
plt.savefig('状态分布.png')
plt.show()

# ------------ 作者分布（前10）------------
plt.figure(figsize=(12,6))
top_authors = df['作者'].value_counts().head(10)
sns.barplot(x=top_authors.values, y=top_authors.index, palette='rocket')
plt.title('高产作者TOP10')
plt.xlabel('作品数量')
plt.ylabel('作者')
plt.savefig('作者分布（前10）.png')
plt.show()

# ------------ 分类与字数的箱线图 ------------
plt.figure(figsize=(14,8))
top_categories = df['分类'].value_counts().head(5).index.tolist()
filtered_df = df[df['分类'].isin(top_categories)]
sns.boxplot(x='分类', y='字数', data=filtered_df)
plt.title('主要分类字数分布')
plt.xticks(rotation=45)
plt.savefig('分类与字数的箱线图.png')
plt.show()


# ------------ 简介词云分析 ------------
text = ' '.join(df['简介'].dropna())
wordcloud = WordCloud(
    width=800,
    height=400,
    background_color='white',
    font_path='simhei.ttf'  # 中文字体路径
).generate(text)

plt.figure(figsize=(12,8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('小说简介词云')
plt.savefig('小说简介词云.png')
plt.show()

# ------------ 分类字数分布散点图 ------------
fig = px.scatter(df,
                 x='分类',
                 y='字数',
                 color='状态',
                 hover_data=['书名'],
                 title='小说分类与字数分布')
fig.show()
