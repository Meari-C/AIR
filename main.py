import discord
import datetime
import logging
import sys
import traceback
import os
import re

def synth(Lists):
    Lsynth=[]
    for i in range(len(Lists[0])):
        e_synth=[]
        for elm in Lists:
            e_synth.append(elm[i])
        Lsynth.append(e_synth)
    return Lsynth


class emojiDB():
    def __init__(self):
        self.e_id=[]
        self.birth=[]
        self.count=[]
        self.main_count=[]
        
    def exists(self,content):
        
        if(content in self.e_id):
            return True
        return False

    def update(self, e_id, birth, count, main_count):
        self.e_id=e_id
        self.birth=birth
        self.count=count
        self.main_count=main_count

class recorder():
    
    def __init__(self):
        self.client = None
        self.guild_id = None
        self.base_time = None
        self.emoji_season = None

        self.guild_emoji = []
        self.emojiDB = emojiDB()
              
        self.guild_updated = None
        
    def re_init(self, client, guild_id, base_time, now_season):
        if guild_id is None:
            raise ValueError("Must provide the Ahricord guild ID.")
        self.client = client
        self.guild_id = guild_id
        self.Emojis=[]
        self.base_time = base_time
        self.emoji_season = 1

        self.guild_updated = True
        self.update_emoji()

    def print_count(self, time, Top, in_main, noob ):
        
              
        if(self.guild_updated):
            ctn="이모지 업데이트가 완료되지 않아 출력할 수 없습니다."
            return ctn
        e_num=len(self.guild_emoji)
        cnt=0
        i=0
        ctn = "%s부터 %s시 까지 "%(self.base_time, time[:-13])
        
        if(noob):
            
            
            if(in_main):
                temp_count=sorted(synth( (self.emojiDB.birth[:],
                                          self.emojiDB.main_count[:],
                                          range(e_num)
                                          ) ),
                                  key = lambda x : (-x[0],Top*x[1]))
                ctn+="메인에서 "
            else:
                temp_count=sorted(synth( (self.emojiDB.birth[:],
                                          self.emojiDB.count[:],
                                          range(e_num)
                                          ) ),
                                  key = lambda x : (-x[0],Top*x[1]))
            ctn+="사용된 신규 이모지의 통계입니다.\n"
            
            if(self.emoji_season != temp_count[0][0]):
                ctn='신규 이모지가 아직 사용되지 않았습니다'
                return ctn

            while(cnt<3 and i<len(temp_count) and self.emoji_season == temp_count[i][0]):
                
                if(temp_count[i][1]==0):
                    i+=1
                    continue
                ctn+="%4d회 : "%(temp_count[i][1])
                j=0
                while(True):
                    if(j<10):
                        ctn+=str(self.guild_emoji[temp_count[i+j][2]])
                    j+=1
                    if(i+j>=len(temp_count) or self.emoji_season != temp_count[i+j][0]):break
                    
                    if(temp_count[i+j-1][1]!=temp_count[i+j][1]):break
                if(j>10):
                    ctn+=' 외 %4d종'%(j-10)
                ctn+='\n'

                i+=j
                cnt+=1
        else:
            if(in_main):
                temp_count=sorted(synth( (self.emojiDB.main_count[:],range(e_num)) ),
                                  key = lambda x : Top*x[0])
                ctn+="메인에서 "
            
            else:
                temp_count=sorted(synth( (self.emojiDB.count[:],range(e_num)) ),
                                  key = lambda x : Top*x[0])
                
            ctn+="사용된 이모지의 통계입니다.\n"
            while(cnt<3 and i<len(temp_count)):
                if(temp_count[i][0]==0):
                    i+=1
                    continue
                ctn+="%4d회 : "%(temp_count[i][0])
                j=0
                while(True):
                    if(j<10):
                        ctn+=str(self.guild_emoji[temp_count[i+j][1]])
                    j+=1
                    if(i+j>=len(temp_count)):break
                    if(temp_count[i+j-1][0]!=temp_count[i+j][0]):break
                if(j>10):
                    ctn+=' 외 %4d종'%(j-10)
                ctn+='\n'

                i+=j
                cnt+=1
            
        return ctn
        

    def print_unused(self , time , in_main, noob ):
        
        
        if(self.guild_updated):
            ctn= "이모지 업데이트가 완료되지 않아 출력할 수 없습니다."
            return ctn
        
        ctn = "%s부터 %s시 까지 "%(self.base_time, time[:-13])
        e_num=len(self.guild_emoji)
        
        if (noob):
            
            if(in_main):
                temp_count=sorted(synth( (self.emojiDB.birth[:],
                                          self.emojiDB.main_count[:],
                                          range(e_num)
                                          ) ),
                                  key = lambda x : (-x[0],x[1]))
                ctn+="메인에서 "
            else:
                temp_count=sorted(synth( (self.emojiDB.birth[:],
                                          self.emojiDB.count[:],
                                          range(e_num)
                                          ) ),
                                  key = lambda x : (-x[0],x[1]))

            ctn+="사용된 신규 이모지의 통계입니다.\n"
            if(temp_count[0][0]!=self.emoji_season):
                ctn="모든 신규 이모지가 한번도 쓰이지 않았습니다\n"
                return ctn
            if(temp_count[0][1]>0):
                ctn="모든 신규 이모지가 적어도 한 번은 쓰였습니다\n"
                return ctn

            ctn+="한 번도 사용되지 않은 \n"
            i=0
            while(temp_count[i][1]<1 and temp_count[i][0]==self.emoji_season):
                if(i<10):
                    ctn+=str(self.guild_emoji[temp_count[i][2]])
                i+=1
                if(i>=len(temp_count) or temp_count[i][0]!=self.emoji_season):break
            if(i>10):
                ctn+='\n외 %4d종의 이모지가 있습니다.'%(i-10)
            else:
                ctn+=' %4d종의 이모지가 있습니다.'%(i)
            

        else:
            
            if(in_main):
                temp_count=sorted(synth( (self.emojiDB.main_count[:],
                                          range(e_num) )
                                         ))
                ctn+="메인에서 "
            else:
                temp_count=sorted(synth( (self.emojiDB.count[:],
                                          range(e_num) )
                                         ))
            ctn +="사용된 이모지의 통계입니다.\n"
            
            if(temp_count[0][0]>0):
                ctn="모든 이모지가 적어도 한 번은 쓰였습니다\n"
                return ctn

            ctn+="한 번도 사용되지 않은 \n"
            i=0
            while(temp_count[i][0]<1):
                if(i<10):
                    ctn+=str(self.guild_emoji[temp_count[i][1]])
                i+=1
                if(i>=len(temp_count)):break
            if(i>10):
                ctn+='\n외 %4d종의 이모지가 있습니다.'%(i-10)
            else:
                ctn+=' %4d종의 이모지가 있습니다.'%(i)
            
        return ctn

    def count_emoji(self,datas,is_main,on_msg=False):
        
        if(on_msg):
            temp_list=self.get_emoji(datas)
        else:
            temp_list=[datas]
        
        K_list= self.check_emoji(temp_list)
        
        while(len(K_list)>0):
            K=K_list[0]
            cnt=0
            while(K in K_list):
                cnt+=1
                K_list.remove(K)
            if( cnt>5 ): cnt=5
            if(is_main):
                self.emojiDB.main_count[K]+=cnt
                
            
            self.emojiDB.count[K]+=cnt
            
            

    def get_emoji(self,msg):
        
        return re.findall(r'<a?:\w*:\d{18}>', msg.content)
    
    def check_emoji(self, temp_list):
        
        K_list=[]
        for temp in temp_list:
            
            K_id=int(temp[-19:-1])
            
            if( self.emojiDB.exists(K_id) ):
                K=self.emojiDB.e_id.index(K_id)

                if( temp==str(self.guild_emoji[K]) ):                    
                    K_list.append(K)
                    
        return K_list                       

    def update_emoji(self):
        
        self.guild_emoji=self.client.get_guild(self.guild_id).emojis
        
        N_id=[]
        N_birth=[]
        N_count=[]
        N_main_count=[]
        
        for emoji in self.guild_emoji:
            N_id.append(emoji.id)
            
            if( self.emojiDB.exists(emoji.id) ):
                K=self.emojiDB.e_id.index(emoji.id)
                
                N_birth.append(         self.emojiDB.birth[K]       )
                N_count.append(       self.emojiDB.count[K]       )
                N_main_count.append(  self.emojiDB.main_count[K]  )                
                
            else:
                
                N_birth.append(self.emoji_season)
                N_count.append(0)
                N_main_count.append(0)
        
        self.emojiDB.update( N_id[:],
                             N_birth[:],
                             N_count[:],
                             N_main_count[:])
        
        self.guild_updated=False
        
    def save_file(self):
        
        
        sav='%3d %s\n'%(self.emoji_season, self.base_time)
        
        for K in range(len(self.guild_emoji)):
            
            sav +=  "%35s"%self.guild_emoji[K].name     #name
            sav += " %18d"%self.emojiDB.e_id[K]          #id
            sav +=  " %3d"%self.emojiDB.birth[K]         #birth
            sav +=  " %4d"%self.emojiDB.count[K]       #count
            sav +=  " %4d"%self.emojiDB.main_count[K]  #main_count
            sav += "\n"
            
        return sav

    def load_file(self,settings,sav_file):
        
        sets = ( settings.strip() ).split()
        self.emoji_season   = int(sets[0])
        self.base_time      = sets[1]

        N_birth=[]
        N_id=[]
        N_count=[]
        N_main_count=[]        
        for counts in sav_file:
                                                  #   0   1      2      3           4
            temp=( counts.strip() ).split()       #name, id, birth, count, count_main

            N_id.append(        int(temp[1]) )
            N_birth.append(     int(temp[2]) )
            N_count.append(     int(temp[3]) )
            N_main_count.append(int(temp[4]) )

        
        self.emojiDB.update( N_id[:],
                             N_birth[:],
                             N_count[:],
                             N_main_count[:])
        
        self.update_emoji()
            
            
        


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
            
p = Params(True)


logging.basicConfig(filename=p.log_path,
                    filemode="a",
                    format="%(asctime)s:%(levelname)s:%(name)s: %(message)s",
                    level=logging.INFO)

client = discord.Client(max_messages=10000)
Recorder=recorder()

def now_time():
    return str(datetime.datetime.now())
    
def emoji_ch_cond(client,channel_id):
    channel=client.get_channel(channel_id)
    if(channel.id in p.channel_emoji_except):
        return False
    elif(isinstance(channel, discord.DMChannel)):
        return False
    elif(isinstance(channel, discord.GroupChannel)):
        return False
    else:
        return True
    
def write_log(content):
    if p.log_debug:
        with open(p.log_path, "a") as log_file:
            log_file.write(content + "\n")
            
def is_admin(user):
    guild = client.get_guild(p.guild_id)
    admin_role = guild.get_role(p.admin_role_id)
    member = guild.get_member(user.id)
    if admin_role not in member.roles:
        return False
    return True

def sav_exists():
    if not(os.path.isdir(p.emoji_sav_dir)):
        return False
    
    if(os.listdir(p.emoji_sav_dir)==[]):
        return False

    return True
def FS_update(msg):
    if(msg.channel.id == p.channel_command and
       is_admin(msg.author)):
        Recorder.emoji_season+=1
    
async def print_count(msg):
    cmd=(msg.content[8:].strip()).split()
    if(cmd==[]):
        await msg.channel.send("sry, mismatch")
        return
    in_main=False
    noob=False
    if('in_main' in cmd):
        in_main=True
    if('new' in cmd):
        noob=True
    if(cmd[0]=='top_rated'):
        ctn=Recorder.print_count( now_time(),-1,in_main,noob)
    elif(cmd[0]=='reverse_rated'):
        ctn=Recorder.print_count( now_time(),1,in_main,noob)
    elif(cmd[0]=='unused'):
        ctn=Recorder.print_unused( now_time(),in_main,noob)
    else:
        ctn="sry, mismatch"

    await msg.channel.send(ctn)
    

async def update_emoji(msg):
        
    if(not is_admin(msg.author)):
        ctn = "정비공만 이용할 수 있는 기능입니다.\n"
        await msg.channel.send(ctn)
        return
    await save_count(msg)
    Recorder.update_emoji()
    await msg.channel.send("업데이트가 완료되었습니다.")
    

async def save_count(msg):
    if(not is_admin(msg.author)):
        ctn = "정비공만 이용할 수 있는 기능입니다.\n"
        await msg.channel.send(ctn)
        return
        
    filename = now_time()[:-16]
    sav_msg = Recorder.save_file()
    
    sav_file=open(p.emoji_sav_dir+filename+'.txt','w')    
    sav_file.write(Recorder.save_file())
    sav_file.close
    await msg.channel.send("%s 세이브 완료했습니다."%(filename))

    sav_list=os.listdir(p.emoji_sav_dir)    
    while(len(sav_list)>10):
        sav_list=os.listdir(p.emoji_sav_dir)
        await export_count(client.get_user(550170449217191938),old_remove=True)

async def load_count(msg, by_self = False):
    if(by_self and sav_exists() ):
        sav_list=os.listdir(p.emoji_sav_dir)
        sav_list.sort(reverse=True)
        sav_file=open(p.emoji_sav_dir+sav_list[0],'r')
        sav_datas=sav_file.readlines()
        Recorder.load_file( sav_datas[0], sav_datas[1:] )
        sav_file.close()
        return
    
    if(not is_admin(msg.author)):
        ctn = "정비공만 이용할 수 있는 기능입니다.\n"
        await msg.channel.send(ctn)
        return
    
    if(not sav_exists()):
        await msg.channel.send("세이브 파일이 존재하지 않습니다")
        return
    
    sav_list=os.listdir(p.emoji_sav_dir)
    sav_list.sort(reverse=True)
    
    sav_file=open(p.emoji_sav_dir+sav_list[0],'r')
    sav_datas=sav_file.readlines()
    Recorder.load_file( sav_datas[0], sav_datas[1:] )
    sav_file.close()
    
    await msg.channel.send("%s의 카운트를 불러왔습니다."%(sav_list[0][:-4]))

async def export_count(author,old_remove=False):
    
    if(not sav_exists()):
        await msg.channel.send("ERROR : 파일이 존재하지 않습니다")
        return
    sav_list=os.listdir(p.emoji_sav_dir)
    if(old_remove):
        sav_list.sort()
    else:
        sav_list.sort(reverse=True)
    export_pack=discord.File(p.emoji_sav_dir+sav_list[0])
    await author.send(file=export_pack)
    
    if(old_remove==True):
        os.remove(p.emoji_sav_dir+sav_list[0])

@client.event
async def on_error(event, *args, **kwargs):
    ctn = "Event: {}\n".format(str(event))
    ctn += "Args: {}\n".format(str(args))
    ctn += "KWArgs: {}\n".format(str(kwargs))
    exc_type, exc_val, tb = sys.exc_info()
    ctn += "Exception info: {0}, {1}, {2}\n".format(str(exc_type), str(exc_val), str(tb))
    print(ctn)
    logging.error(ctn)
    traceback.print_tb(tb, file=p.log_path)
    


@client.event
async def on_ready():
    
    ctn = "========== {} ==========\n".format(str(datetime.datetime.now()))
    ctn += "Bot is now booting up.\n"
    ctn += "Server name: {}\n".format(client.get_guild(p.guild_id).name)
    ctn += "\nair-chord is ready to take off, sir.\n"
    
    Recorder.re_init(client,p.guild_id,str(datetime.datetime.now())[:-16],0)

    if not(os.path.isdir(p.emoji_sav_dir)):
        os.makedirs(os.path.join(p.emoji_sav_dir))
    if(sav_exists()):
        await load_count(msg=None, by_self=True)
    print(ctn)
    write_log(ctn)
    

@client.event
async def on_message(msg):
    if( msg.author.bot ):
        return None
    #commands
    if( msg.content[:2] == '$$' and
        ( msg.channel.id == p.channel_command or
          msg.channel.id == p.channel_test) ):
        cmd=(msg.content.rstrip())[3:]
        if(cmd[:5]=='print'):
            await print_count(msg)
        elif(cmd=='update'):
            await update_emoji(msg)
        elif(cmd=='save'):
            await save_count(msg)
        elif(cmd=='load'):
            await load_count(msg)
        elif(cmd=='export'):
            await export_count(msg.author)
        elif(cmd=='force_season_update'):
            FS_update(msg)
        elif(cmd=='help'):
            await msg.author.send('https://blog.naver.com/atashiac/221872477674')
        else:
            await msg.channel.send("sry, mismatch")
    if( msg.content[12:]=='!print_emoji'):
       FS_update(msg)
        
        

    #emoji record
    if(not emoji_ch_cond(client,msg.channel.id)):
        pass
    else:
        is_main=False
        if(msg.channel.id==p.channel_main):
            is_main=True
        Recorder.count_emoji(msg,is_main,on_msg=True)

@client.event
async def on_message_edit(before,msg):
    if( msg.author.bot ):
        return None
    if(not emoji_ch_cond(client,msg.channel.id)):
        pass
    else:
        is_main=False
        if(msg.channel.id==p.channel_main):
            is_main=True
        Recorder.count_emoji(msg,is_main,on_msg=True)
    

@client.event
async def on_reaction_add(react,usr):
    if(not emoji_ch_cond(client,react.message.channel.id)):
        pass
    elif(react.emoji.is_unicode_emoji()):
        pass
    else:
        is_main=False
        if(react.message.channel_id==p.channel_main):
            is_main=True
        Recorder.count_emoji(str(react.emoji),is_main)
        
@client.event
async def on_guild_emojis_update(g,b,a):
    Recorder.guild_updated=True
    



if __name__ == "__main__":
    client.run(p.token)

