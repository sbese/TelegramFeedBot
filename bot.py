class Bot:
    def __init__(self,init):
        self.bot=telebot.TeleBot('377500143:AAGCIxWShxKID1CdAIRE4NstRoUfsw4CYjo')

    def update(message):
        pass
    def add(message):
        pass
    def del(message):
        pass
    
    @bot.message_handler()
    def nm(message):
        global to_id
        global p
        p = message
        if message.chat.id==client_chat_id:
            if message.text.find('forward_to_')!=-1:
                to_id=int(message.text.partition('forward_to_')[2])

            else: bot.forward_message(chat_id=to_id,
                                      from_chat_id=client_chat_id,
                                      message_id=message.message_id)

        else:
            splited_text=message.text.split()
            if splited_text[0]=='/update':
                self.update(message)
            if splited_text[0]=='/add':
                pass
            if splited_text[0]=='/dell':
                pass

    def start(self):
        self.bot.polling(none_stop=True)
