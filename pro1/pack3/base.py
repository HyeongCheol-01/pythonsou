import MySQLdb
import pickle

with open('mydb.dat', mode='rb') as obj:
    config = pickle.load(obj)

def chulbal():
    try:
        conn = MySQLdb.connect(**config)
        cursor = conn.cursor()

        sql = """
        
        """
        cursor.execute(sql)
        datas = cursor.fetchall()
        for a,b,c in datas:
            print(a,b,c)


    except Exception as e:
        print('err :', e)
    finally:
        cursor.close()
        conn.close()


if __name__=="__main__":
    chulbal()
