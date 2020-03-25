class Params:
    def __init__(self, release=False, log_debug=True):
        self.token_test = os.environ["FAKE_TOKEN"]
        self.token_release = os.environ["BOT_TOKEN"]
        self.log_path = "log.txt"
        self.release = release
        self.log_debug = log_debug

        if release:
            self.token = self.token_release
            self.guild_id = 368797408479412224
            
            self.emoji_sav_dir='cnt_%d/'%(self.guild_id)

            self.admin_role_id = 386095313884151809

            self.channel_main = 368797408479412226
            self.channel_survey = 408682266114523147
            self.channel_command = 410091338214932490
            self.channel_test = 369052857942671360
             
            
            self.channel_emoji_except=[
                self.channel_survey
                ]

        else:
            self.token = self.token_test
            self.guild_id = 687658663078527006
            
            self.emoji_sav_dir='cnt_%d/'%(self.guild_id)

            self.admin_role_id = 691533503887835206

            self.channel_main = 687658663082721340
            self.channel_survey = 688009116194439263
            self.channel_command = 687697597040951340
            self.channel_test = 688009744681664632
             
            
            self.channel_emoji_except=[
                self.channel_survey
                ]
            
params = Params(True)
