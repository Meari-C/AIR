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
            
            
        
