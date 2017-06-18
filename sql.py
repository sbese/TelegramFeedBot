class SQL_helper:
    
    def __init__(self,path,db_name):

        import sqlite3
        import os
        
        os.chdir(path)
        self.conn=sqlite3.Connection(db_name)
        self.cursor=self.conn.cursor()
        
        
    def check_id(self,chat_id,table):
        
        
        ids=[x[0] for x in [x for x in self.cursor.execute('SELECT id FROM {}'.format(table))]]
        if not (chat_id in ids):
            self.cursor.execute(
                'INSERT INTO {}(id) VALUES({})'.format(
                    table,str(chat_id)
                    )
                )
            self.conn.commit()

    

    def get_channels(self,chat_id,table):

        res=[
            x[0] for x in [
                x for x in self.cursor.execute(
                    'select channels from {} where id={}'.format(
                        table,str(chat_id)
                        )
                    )
                ]
            ]
        if len(res)!=0:
            if res[0] is None:
                return []
            else:
                return str(res[0]).split(',')
        else :
            return []


    def get_all_channels(self,table):

        return[
            x[0] for x in [
                x for x in self.cursor.execute(
                    'select channels from {} '.format(table)
                    )
                ]
            ]

    def missing_channels(self,list_channels,table):

        channels=[
            x[0] for x in [
                x for x in self.cursor.execute(
                    'SELECT channel FROM {}'.format(table)
                    )
                ]
            ]

        return [channel for channel in list_channels if not channel in channels]
        

    def update_channels_list(self,channels,table,chat_id):
        self.cursor.execute("UPDATE {} set channels={} where id={}".format(table,channels,chat_id))
        self.conn.commit()   
       


