

class Bot:
    import telebot
    import client as Client
    import info
    client=Client.client(info.api,info.api_hash,info.phone)
    client_chat_id=280629735
    def __init__(self,token):
        self.bot=telebot.TeleBot(info.token)

        @self.bot.message_handler()
        def nm(message):
            global to_id
            global p
            p = message
            if message.chat.id==self.client_chat_id:
                if message.text.find('forward_to_')!=-1:
                    to_id=int(message.text.partition('forward_to_')[2])

                else: self.bot.forward_message(chat_id=to_id,
                                               from_chat_id=self.client_chat_id,
                                               message_id=message.message_id)

            else:
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
