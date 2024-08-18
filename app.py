#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, request, render_template
from sqlalchemy import create_engine, text
import pandas as pd  # 确保导入 pandas

# 创建 Flask 应用
app = Flask(__name__)

# 创建数据库连接
engine = create_engine('sqlite:///poetry.db')

@app.route('/')
def index():
    # 从数据库中查询部分数据
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM poems LIMIT 20"))
        data = result.fetchall()
        columns = result.keys()

    # 将数据转为HTML表格
    table_html = pd.DataFrame(data, columns=columns).to_html(classes='table table-striped', index=False)
    
    return render_template('index.html', table=table_html, columns=columns)

@app.route('/query', methods=['POST'])
def query_data():
    # 获取用户的查询
    query_column = request.form.get('column')
    query_value = request.form.get('value')
    
    # 从数据库中执行查询
    query = text(f"SELECT * FROM poems WHERE {query_column} LIKE :value LIMIT 20")
    with engine.connect() as connection:
        result = connection.execute(query, {"value": f"%{query_value}%"})
        data = result.fetchall()
        columns = result.keys()
    
    # 将数据转为HTML表格
    table_html = pd.DataFrame(data, columns=columns).to_html(classes='table table-striped', index=False)
    
    return render_template('query.html', table=table_html, columns=columns)

# 启动 Flask 应用
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)


# In[ ]:




