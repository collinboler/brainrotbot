import re

# Reddit shorthand mappings
REDDIT_MAPPINGS = {
    'DM': 'Direct Message',
    'PM': 'Private Message',
    'AITA': 'am I the ay hole',
    'AITAH': 'am I the ay hole',
    'TIFU': 'today I effed up',
    'TL;DR': 'too long, didn\'t read',
    'TLDR': 'too long, didn\'t read',
    'TL; DR': 'too long, didn\'t read',
    'ETA': 'edited to add',
    'FWIW': 'for what it\'s worth',
    'IMO': 'in my opinion',
    'IMHO': 'in my humble opinion',
    'AFAIK': 'as far as I know',
    'TIL': 'today I learned',
    'IIRC': 'if I remember correctly',
    'FTFY': 'fixed that for you',
    'IANAL': 'I am not a lawyer',
    'IME': 'in my experience',
    'GF': 'girl friend',
    'BF': 'boy friend',
    'MIL': 'mother in law',
    'FIL': 'father in law',
    'SIL': 'sister in law',
    'BIL': 'brother in law',
    'WIBTAH': 'would I be the ay hole',
    'WIBTA': 'would I be the ay hole',
}

# YouTube-unfriendly words with their substitutions
YOUTUBE_UNFRIENDLY_WORDS = {
    # Profanity
    r'\b(f\*ck|f\*\*k|fuck|effing)\b': 'mess up',
    r'\b(sh\*t|sh\*t|shit|crap)\b': 'stuff',
    r'\b(b\*tch|b\*\*ch|bitch)\b': 'woman',
    
    # Sexual content
    r'\b(sex|sexual)\b': 'intimate',
    r'\b(porn|pornograph)\b': 'inappropriate content',
    r'\b(masturbat|jerk off)\b': 'personal time',
    r'\b(erotic|horny)\b': 'romantic',
    r'\b(tits|boobs)\b': 'chest',
    
    # Extreme violence
    r'\b(mutilat|dismember|decapitat|massacre)\b': 'harmed',
    r'\b(kill|killed|killing)\b': 'unalive',
    
    # Drug references
    r'\b(cocaine|heroin|meth|crack|weed)\b': 'harmful substance',
    r'\b(overdose|drugged)\b': 'medical emergency',
    r'\b(stoned|high)\b': 'impaired',
    
    # Offensive slurs (replaced with neutral terms)
    r'\b(retard|tard)\b': 'person with challenges',
    r'\b(faggot|dyke|tranny|homo)\b': 'person',
    r'\b(midget)\b': 'short person',
    r'\b(nigger)\b': 'black person',
    r'\b(nigga)\b': 'black fellow',
    
    # Crude body part references
    r'\b(dick|pussy|cock|balls)\b': 'genatailia',
    
    # Extremely offensive terms
    r'\b(cunt|asshole|bastard)\b': 'person',
    
    # Religious/Offensive exclamations
    r'\b(hell|damn)\b': 'goodness',
    
    # Derogatory terms
    r'\b(whore|slut)\b': 'person',
    r'\b(loser|idiot|moron)\b': 'individual',
    
    # Hate speech and discriminatory language
    r'\b(gay|queer)\b': 'fruity',
    r'\b(transgender)\b': 'fruity with extra steps',
    
    # More Profanity & Variants  
    r'\b(ass|arse)\b': 'butt',  
    r'\b(motherf\*?ucker|mf|mofo)\b': 'bad person',  
    r'\b(wtf)\b': 'what in the world',  

    # More Sexual References  
    r'\b(bang|screw|nail)\b': 'hook up',  
    r'\b(cumming|cum)\b': 'finish',  
    r'\b(boner|erection)\b': 'arousal',  

    # More Violence & Crime  
    r'\b(assault|murder|stab|shoot|bomb)\b': 'attack',  
    r'\b(terrorist|terrorism)\b': 'criminal',  

    # More Drug References  
    r'\b(xanax|adderall|oxy|fentanyl)\b': 'prescription drug',  
    r'\b(lean|sizzurp|codeine)\b': 'drink',   
}

def filter_youtube_unfriendly_content(text):
    """Filter out YouTube-unfriendly content by substituting problematic words."""
    for pattern, replacement in YOUTUBE_UNFRIENDLY_WORDS.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text

def convert_age_gender(text):
    """Convert age/gender format (e.g., 24F, 25M, M17, F42) to written form"""
    def replace_match(match):
        age = int(match.group(1) or match.group(3))
        gender_char = match.group(2) or match.group(4)
        
        if age < 18:
            gender = 'girl' if gender_char.upper() == 'F' else 'boy'
        else:
            gender = 'woman' if gender_char.upper() == 'F' else 'man'
            
        return f"a {age}-year-old {gender}"
    
    return re.sub(r'(\d+)([MF])\b|([MF])(\d+)\b', replace_match, text, flags=re.IGNORECASE)

def convert_time_format(text):
    """Convert time formats (e.g., 5pm, 10AM) to spoken form"""
    def replace_time(match):
        hour = match.group(1)
        meridiem = match.group(2).lower()
        return f"{hour} {meridiem}"
    
    return re.sub(r'(\d+)\s*(am|pm|AM|PM)', replace_time, text)

def preprocess_text(text):
    """Process Reddit shorthand and formatting"""
    # Filter YouTube-unfriendly content first
    text = filter_youtube_unfriendly_content(text)
    
    # Handle age/gender formats
    text = convert_age_gender(text)
    
    # Convert time formats
    text = convert_time_format(text)
    
    # Replace Reddit abbreviations
    for shorthand, full_text in REDDIT_MAPPINGS.items():
        text = re.sub(r'\b' + re.escape(shorthand) + r'\b', full_text, text, flags=re.IGNORECASE)
    
    # Clean up any extra spaces
    text = ' '.join(text.split())
    
    return text 