class SQL_helper:
    
    import sqlite3
    import os
    
    def __init__(self,path,db_name):

        import sqlite3
        import os
        
        os.chdir(path)
        self.conn=sqlite3.Connection(db_name)
        self.cursor=self.conn.cursor()
        
        
    def check_id(self,chat_id,table):
        
        ids=[x[0] for x in [x for x in self.cursor.execute('SELECT id FROM {}'.format(table))]]
        print(ids)
        if not (chat_id in ids):
            self.cursor.execute('INSERT INTO {}(id) VALUES({})'.format(table,str(chat_id)))
            self.conn.commit()

    def get_channels(self,chat_id,table):

        return[x[0] for x in [x for x in self.cursor.execute('select channels from test1 where id=2')]][0].split(',')

    def check_channel(self,list_channels,table):

        channels=[x[0] for x in [x for x in self.cursor.execute('SELECT channel FROM {}'.format(table))]]

        for channel in list_channels:
            if not (channel in channels):
                self.cursor.execute('INSERT INTO{}(channel) VALUES({})'.format(table,channel))

