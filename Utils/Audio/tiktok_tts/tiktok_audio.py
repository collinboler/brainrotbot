from tiktok_voice import tts, Voice
import re

# ----------- all voices -------------
# GHOSTFACE
# CHEWBACCA
# C3PO
# STITCH
# STORMTROOPER
# ROCKET
# MADAME_LEOTA
# GHOST_HOST
# PIRATE
# AU_FEMALE_1
# AU_MALE_1
# UK_MALE_1
# UK_MALE_2
# US_FEMALE_1
# US_FEMALE_2
# US_MALE_1
# US_MALE_2
# US_MALE_3
# US_MALE_4
# MALE_JOMBOY
# MALE_CODY
# FEMALE_SAMC
# FEMALE_MAKEUP
# FEMALE_RICHGIRL
# MALE_GRINCH
# MALE_DEADPOOL
# MALE_JARVIS
# MALE_ASHMAGIC
# MALE_OLANTERKKERS
# MALE_UKNEIGHBOR
# MALE_UKBUTLER
# FEMALE_SHENNA
# FEMALE_PANSINO
# MALE_TREVOR
# FEMALE_BETTY
# MALE_CUPID
# FEMALE_GRANDMA
# MALE_XMXS_CHRISTMAS
# MALE_SANTA_NARRATION
# MALE_SING_DEEP_JINGLE
# MALE_SANTA_EFFECT
# FEMALE_HT_NEYEAR
# MALE_WIZARD
# FEMALE_HT_HALLOWEEN
# FR_MALE_1
# FR_MALE_2
# DE_FEMALE
# DE_MALE
# ES_MALE
# ES_MX_MALE
# BR_FEMALE_1
# BR_FEMALE_2
# BR_FEMALE_3
# BR_MALE
# BP_FEMALE_IVETE
# BP_FEMALE_LUDMILLA
# PT_FEMALE_LHAYS
# PT_FEMALE_LAIZZA
# PT_MALE_BUENO
# ID_FEMALE
# JP_FEMALE_1
# JP_FEMALE_2
# JP_FEMALE_3
# JP_MALE
# KR_MALE_1
# KR_FEMALE
# KR_MALE_2
# JP_FEMALE_FUJICOCHAN
# JP_FEMALE_HASEGAWARIONA
# JP_MALE_KEIICHINAKANO
# JP_FEMALE_OOMAEAIIKA
# JP_MALE_YUJINCHIGUSA
# JP_FEMALE_SHIROU
# JP_MALE_TAMAWAKAZUKI
# JP_FEMALE_KAORISHOJI
# JP_FEMALE_YAGISHAKI
# JP_MALE_HIKAKIN
# JP_FEMALE_REI
# JP_MALE_SHUICHIRO
# JP_MALE_MATSUDAKE
# JP_FEMALE_MACHIKORIIITA
# JP_MALE_MATSUO
# JP_MALE_OSADA
# SING_FEMALE_ALTO
# SING_MALE_TENOR
# SING_FEMALE_WARMY_BREEZE
# SING_MALE_SUNSHINE_SOON
# SING_FEMALE_GLORIOUS
# SING_MALE_IT_GOES_UP
# SING_MALE_CHIPMUNK
# SING_FEMALE_WONDERFUL_WORLD
# SING_MALE_FUNNY_THANKSGIVING
# MALE_NARRATION
# MALE_FUNNY
# FEMALE_EMOTIONAL
# ----------------------------------------

def clean_text(text):
    """
    Cleans the input text by:
    1. Removing special characters (except basic punctuation)
    2. Replacing newlines with spaces
    3. Trimming extra spaces
    """
    # Replace newlines and multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    
    # Remove unwanted special characters (keep basic punctuation)
    text = re.sub(r'[^\w\s.,!?\-]', '', text)
    
    # Trim leading/trailing spaces
    return text.strip()


#make it so that we can choose the voice model in the main.py
def text_to_speech(text, output='./Assets/reddit_audio.mp3'):
    cleaned_text = clean_text(text)
    tts(cleaned_text, voice=Voice.US_MALE_1, output_file_path=output, play_sound=False)
    return output