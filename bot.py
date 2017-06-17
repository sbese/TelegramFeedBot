

class Bot:

    def __init__(self,token):

        import telebot
        from client import Client
        import info
        from sql import SQL_helper as SQL_DB
        self.client=Client(info.api,info.api_hash,info.phone)
        self.db=SQL_DB(info.path,info.db)
        self.bot=telebot.TeleBot(info.token)
        self.to_id=0
        self.client=Client(info.api,info.api_hash,info.phone)
        self.client_chat_id=info.client_chat_id

        
        @self.bot.message_handler()
        def nm(message):
            if message.chat.id==self.client_chat_id:
                if message.text.find('forward_to_')!=-1:
                    to_id=int(message.text.partition('forward_to_')[2])

                else: self.bot.forward_message(chat_id=self.to_id,
                                               from_chat_id=self.client_chat_id,
                                               message_id=message.message_id)

            else:
                self.db.check_id(message.chat.id)
                splited_text=message.text.split()
                if splited_text[0]=='/update':
                    self.update_feed(message)
                if splited_text[0]=='/add':
                    pass
                if splited_text[0]=='/dell':
                    pass

    def update_feed(message):
        pass
    def add_channels(message):
        pass
    def del_channels(message):
        pass
    
   

    def start(self):
        self.bot.polling(none_stop=True)
