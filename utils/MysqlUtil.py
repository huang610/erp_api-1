from utils.LogUtil import my_log
import pymysql

class Mysql:
    def __init__(self,host,user,password,database,charset="utf8",port=3306):
        '''
        初始化数据，连接数据库，光标对象
        :param host:
        :param user:
        :param password:
        :param database:
        :param charset:
        :param port:
        :return:
        '''
        self.log = my_log()
        self.conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            charset=charset,
            port=port
            )
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def fetchone(self,sql):
        """
        单个查询
        :param sql:
        :return:
        """
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def fetchall(self,sql):
        """
        多个查询
        :param sql:
        :return:
        """
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def exec(self,sql):
        """
        执行sql
        :return:
        """
        try:
            if self.conn and self.cursor:
                self.cursor.execute(sql)
                self.conn.commit()
        except Exception as ex:
            self.conn.rollback()
            self.log.error("Mysql 执行失败")
            self.log.error(ex)
            return False
        return True

    def __del__(self):
        '''
        关闭光标对象, 关闭连接对象
        :return:
        '''
        if self.cursor is not None:
            self.cursor.close()

        if self.conn is not None:
            self.cursor.close()

# if __name__ == "__main__":
#     mysql = Mysql("192.168.37.203",
#                   "imslocal",
#                   "imslocal","ims_spt",
#                   charset="utf8",
#                   port=3307)
#     res = mysql.fetchall("select sum(medins_cnt) as medins_cnt ,sum(bydise_setl_psntime) as bydise_setl_psntime ,sum(sindise_cnt) as sindise_cnt ,round(case when sum(bydise_setl_psntime) = 0 then 0 else sum(totl_ipt_days) / sum(bydise_setl_psntime) end, 1) as avg_ipt_days,round(case when sum(paybydise_amt) = 0 then 0 else sum(psn_part_amt) / sum(paybydise_amt) end, 2) as psn_part_ratio ,round(case when sum(bydise_setl_psntime)=0 then 0 else sum(rept_ipt_psntime) / sum(bydise_setl_psntime) end, 2) as rept_ipt_rate from sindise_pay_regn_stt_e where stt_year = 2020;")
#     #res = mysql.exec("select stt_year code,concat(stt_year, '年') label from sindise_pay_regn_stt_e group by stt_year order by stt_year desc;")
#     print(res)

