#encoding=utf-8
import MySQLdb
import json
db = MySQLdb.connect("localhost", "root", "", "lawdb", charset="utf8")
cursor = db.cursor()
def getContent():

   # SQL 查询语句
   sql = u"SELECT DISTINCT DOCNAME FROM law_0_doc"
   try:
      # 执行SQL语句
      cursor.execute(sql)
      # 获取所有记录列表
      result = cursor.fetchall()
      Fls = [item[0] for item in result]
      f = open("fls.json", "w")
      data = json.dumps(Fls, ensure_ascii=False)
      f.write(data.encode('utf-8'))
   except:
      result = u"NOT FOUND"
   return result
if __name__ == '__main__':
    getContent()