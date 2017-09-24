import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
try:
    conn=MySQLdb.connect(host="localhost",user="root",passwd="zhangyanping",db="novel",charset="utf8")
    print "connected!"  
    sql="select bookName from book_content group by bookName"
    cursor=conn.cursor()
    cursor.execute(sql)
    bookList=cursor.fetchall()
    for each in bookList:
        print each[0]
        f=open(each[0]+".txt",'a+')
        sql="select title ,content from book_content where bookName='%s' order by chapterNum asc"%each[0]
        count=cursor.execute(sql)
        print "count",count
        result=cursor.fetchall()
        for each in result:
            title=each[0]
            content=each[1]
            print "title:%s \r content:%s"%(title,content)
            str=title+"\r"+content+"\r";
            f.write(str)
            f.close
    cursor.close()
    conn.close()
except Exception,e:
    print e