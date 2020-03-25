import discord
import datetime
import logging
import sys
import traceback
import os

from params import params as p
from record_bot import recorder
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

