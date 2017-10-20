
from Utils import to_sql_token

import MySQLdb

import time, base64, md5

class QueueBuilderRep:
    
    __temp_prefix = '__temp_queue__'

    def __table(self, name):
        return to_sql_token(name)
    
    def __init__(self, db_user, db_passwd):
        
        self.__db = MySQLdb.connect(host="localhost", user=db_user, passwd=db_passwd)
        cursor = self.__db.cursor()        
        cursor.execute("CREATE DATABASE IF NOT EXISTS exomind")
        cursor.execute("USE exomind")
        self.__cursor = cursor

        # queues tables
        statement1= """        
        CREATE TABLE IF NOT EXISTS queues (
            name VARCHAR(256) NOT NULL PRIMARY KEY
       );
       """
        self.__cursor.execute(statement1)
        
        # delete temporary queues of previous sessions
        for queue_name in self.get_queues():
            if queue_name.startswith(self.__temp_prefix):
                self.drop_queue(queue_name)


    def __contains__(self, name):
        name = self.__table(name)
        try:
            self.create_queue(name)
            self.drop_queue(name)
            return False
        except:
            return True

    def create_queue(self, name, index=False):
        name = self.__table(name)
        self.__cursor.execute("INSERT INTO queues VALUES ('%s')" % name)

        statement1= """
        CREATE TABLE %s_queue (
            item_number BIGINT NOT NULL PRIMARY KEY,
            serial_number VARCHAR(256) NOT NULL
        );
       """
        self.__cursor.execute(statement1 % (name))

        if index:
            statement2 = """
            CREATE INDEX %s_queue_index
            ON %s_queue (serial_number)
           """
            self.__cursor.execute(statement2 % (name,name))


       
    def drop_queue(self, name):
        name = self.__table(name)        
        self.__cursor.execute("DELETE FROM queues WHERE name='%s'" % name)

        drop_statement1= """        
        DROP TABLE %s_queue;
       """
        self.__cursor.execute(drop_statement1 % (name))
    
    def push(self, queue_name, elem, reverse=False):
        queue_name = self.__table(queue_name)
        if self.len(queue_name) > 0:
            if not reverse:
                push_statement1= """        
                SELECT item_number
                FROM %s_queue
                ORDER BY item_number
                DESC
                LIMIT 0,1
                INTO @top;
                """                        
                self.__cursor.execute(push_statement1 % (queue_name))
                
                push_statement1= """
                INSERT INTO %s_queue ( item_number, serial_number )
                VALUES( @top + 1, '%s');        
               """
                self.__cursor.execute(push_statement1 % (queue_name, elem))
                
            else:
                push_statement1= """        
                SELECT item_number
                FROM %s_queue
                ORDER BY item_number
                LIMIT 0,1
                INTO @top;
                """
                self.__cursor.execute(push_statement1 % (queue_name))
            
                push_statement1= """
                INSERT INTO %s_queue ( item_number, serial_number )
                VALUES( @top - 1, '%s');        
               """
                self.__cursor.execute(push_statement1 % (queue_name, elem))
       
        else:

            push_statement1= """
            INSERT INTO %s_queue ( item_number, serial_number )
            VALUES( 0, '%s');        
           """
            self.__cursor.execute(push_statement1 % (queue_name, elem))
            
        
    def pop(self, queue_name, type='FIFO'):
        queue_name = self.__table(queue_name)
        if type == 'FIFO':
            push_statement1= """        
            SELECT item_number, serial_number
            FROM %s_queue 
            ORDER BY item_number
            LIMIT 0,1
            INTO @item_number, @serial_number
            ;
            """
        elif type == 'LIFO':
            push_statement1= """        
            SELECT item_number, serial_number
            FROM %s_queue 
            ORDER BY item_number
            DESC
            LIMIT 0,1
            INTO @item_number, @serial_number
            ;
            """
        self.__cursor.execute(push_statement1 % (queue_name))
        
        push_statement1= """
        DELETE FROM %s_queue WHERE @item_number = item_number
        ;
        """
        self.__cursor.execute(push_statement1 % (queue_name))
        
        push_statement1= """
        SELECT @serial_number
        ;
        """
        self.__cursor.execute(push_statement1)
        rows = self.__cursor.fetchall()
        for row in rows:
            return row[0]

    def unpop(self, queue_name, n, type='FIFO'):
        queue_name = self.__table(queue_name)
        if type == 'LIFO':
            reverse = False
            self.push(queue_name, n, reverse)
            return
        elif type == 'FIFO':
            reverse = True
            self.push(queue_name, n, reverse)

    def len(self, queue_name):
        queue_name = self.__table(queue_name)
        push_statement1= """
        SELECT COUNT(*) FROM %s_queue;
        ;
        """
        self.__cursor.execute(push_statement1 % queue_name)
        rows = self.__cursor.fetchall()
        for row in rows:
            return int(row[0])

    def __get_something(self, table, node=None):
        table = self.__table(table)
        cursor = self.__cursor
        if not node:
            cursor.execute("SELECT * FROM %s" % table)
            return cursor.fetchall()
        else:
            cursor.execute("SELECT * FROM %s WHERE serial_number='%s'" % (table,node))
            return cursor.fetchall()            
        
    def get_queues(self, include_temp=True):
        for row in self.__get_something('queues'):
            if include_temp or not row[0].startswith(self.__temp_prefix):                 
                yield row[0]
   
    def get_elems(self, queue_name, elem=None):
        for row in self.__get_something('%s' % queue_name, elem):
            yield row

    def exists_elem(self, queue_name, elem):
        ret = False
        for row in self.get_elems('%s_queue' % queue_name, elem):
            ret = True
            break
        return ret

    def get_temporary_queue(self):
        return self.__temp_prefix + base64.b64encode(md5.new(str(time.time())).digest()).replace('/','A').replace('+','A')[:12]
    
if __name__=='__main__':
    
    p = QueueBuilderRep()
    
    g_name = 'AAA'
    if not g_name in p:
        p.create_queue(g_name)
    p.drop_queue(g_name)
 
    p.create_queue(g_name)
    
    p.push(g_name, 'alice')
    p.push(g_name, 'bob')
    p.push(g_name, 'eve')
    while p.len(g_name) > 0:
        print p.pop(g_name)
    
    p.drop_queue(g_name)
        
