import boto3
from pydub import AudioSegment


from vpgenerator import audioeffects
from vpgenerator import aiaudioengine


AWS_ENGINE = "AWS"

# Complete the voice list https://docs.aws.amazon.com/polly/latest/dg/voicelist.html
# VoiceId Valid Values: Aditi | Amy | Astrid | Bianca | Brian | Camila | Carla | Carmen | Celine | Chantal | Conchita | Cristiano | Dora | Emma | Enrique | Ewa | Filiz | Gabrielle | Geraint | Giorgio | Gwyneth | Hans | Ines | Ivy | Jacek | Jan | Joanna | Joey | Justin | Karl | Kendra | Kevin | Kimberly | Lea | Liv | Lotte | Lucia | Lupe | Mads | Maja | Marlene | Mathieu | Matthew | Maxim | Mia | Miguel | Mizuki | Naja | Nicole | Olivia | Penelope | Raveena | Ricardo | Ruben | Russell | Salli | Seoyeon | Takumi | Tatyana | Vicki | Vitoria | Zeina | Zhiyu | Aria | Ayanda
AWS_VOICES = {
    "Mathieu":{"lang":"fr","voiceId":"Mathieu","engine":"standard"},
    "Lea":{"lang":"fr","voiceId":"Lea","engine":"neural"},
    "Remi":{"lang":"fr","voiceId":"Remi","engine":"neural"},
    "Chantal":{"lang":"fr","voiceId":"Chantal","engine":"standard"},
    "Gabrielle":{"lang":"fr","voiceId":"Gabrielle","engine":"neural"},
    "Celine":{"lang":"fr","voiceId":"Celine","engine":"standard"},
    "Joanna":{"lang":"en","voiceId":"Joanna","engine":"neural"},
    "Stephen":{"lang":"en","voiceId":"Stephen","engine":"neural"},
    "Bianca":{"lang":"it","voiceId":"Bianca","engine":"neural"},
    "Lupe":{"lang":"es","voiceId":"Lupe","engine":"neural"},
    "Vicki":{"lang":"de","voiceId":"Vicki","engine":"neural"}
    }


class AwsAudioConfig(aiaudioengine.AIAudioConfig):


    def __init__(self):
        super().__init__()
        self.aiengine = "AWS"
        self.awsvoice = "Lea"
        self.awsaccesskeyid = ""
        self.awssecretkey = ""

    def insert_paramaters(self,dic):
        super().insert_paramaters(dic)
        dic["awsvoice"] = self.awsvoice
        dic["awsaccesskeyid"] = self.awsaccesskeyid
        dic["awssecretkey"] = self.awssecretkey
    
    
    def extract_paramaters(self,dic):
        super().extract_paramaters(dic)
        self.awsvoice = dic["awsvoice"]
        self.awsaccesskeyid = dic["awsaccesskeyid"]
        self.awssecretkey = dic["awssecretkey"]


class AwsAudioEngine(aiaudioengine.AIAudioEngine):
    
    def __init__(self):
        self.config = AwsAudioConfig()
    
    
    def load_config(self, config_path):
        self.config = AwsAudioConfig()
        self.config.load(config_path)
    
    
    def save_config(self, config_path):
        self.config.save(config_path)
    

    def convert_text_to_ogg(self, text, ogg_filepath):   
        percent = self.config.audiospeed
        ssmltext=f"<speak><prosody volume='x-loud' rate='{percent}%'>{text}</prosody></speak>"
        
        polly_client = boto3.Session(
                    aws_access_key_id=self.config.awsaccesskeyid,                  
                    aws_secret_access_key=self.config.awssecretkey,
                    region_name='eu-central-1').client('polly')

        awsvoice = AWS_VOICES[self.config.awsvoice]
        
        response = polly_client.synthesize_speech(VoiceId=awsvoice["voiceId"],
                    OutputFormat='ogg_vorbis',
                    TextType = "ssml",                 
                    Text=ssmltext,
                    Engine= awsvoice["engine"])

        file = open(ogg_filepath, 'wb')
        file.write(response['AudioStream'].read())
        file.close()
        
        audioeffects.update_ogg_audio_gain(ogg_filepath,  self.config.audiogain)
    