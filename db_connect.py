# In[65]:


# In[66]:

import pymysql 

class DBConnect:
    
    # 생성자 선언
    def __init__(self):
        self.conn = pymysql.connect(host = 'localhost', 
                                    user = 'bitai', 
                                    password = '456123', 
                                    db = 'video_crawl_db', 
                                    charset = 'utf8')
        self.curs = self.conn.cursor(pymysql.cursors.DictCursor)
        
    # insert 메서드 정의
    def video_insert(self, tag_dict):
        try:
            # insert 쿼리 작성
            sql = """insert into video_crawl_table (youtuber_name, video_play_time, subscribe_num, views_num, upload_time, crwaling_time) values (%s, %s, %s, %s, %s, %s)"""
            
            for col_0, col_1, col_2, col_3, col_4, col_5, col_6 in tag_dict:
                # insert 쿼리 실행
                self.curs.execute(sql, "{}{}{}{}{}{}{}".format(col_0, col_1, col_2, col_3, col_4, col_5, col_6))
                
            # DML문 완료 후 커밋
            self.conn.commit()
            
        except Exception as e:
            print(e)
            
        finally:
            # 커넥트 인스턴스 닫기
            self.conn.close()

