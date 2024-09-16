# converts from pinyin with the tone represented as number at the end of the
# string i.e (yang2) to the tone above the appropriate vowel i.e (yang2) -> (yáng)
def convert_pinyin(pinyin):
    vowels = ['ai', 'ao', 'ei', 'ia', 'iao', 'ie', 'io', 'iu', 'ou', 'ua', 
              'uai', 'ue', 'ui', 'uo', 'üa', 'üe', 'a', 'e', 'i', 'o', 'u', 'ü']


    vowel = { 'a' : ['', 'ā', 'á', 'ǎ', 'à'],
              'e' : ['', 'ē', 'é', 'ě', 'è'],
              'i' : ['', 'ī', 'í', 'ǐ', 'ì'],
              'o' : ['', 'ō', 'ó', 'ǒ', 'ò'],
              'u' : ['', 'ū', 'ú', 'ǔ', 'ù'],
              'ü' : ['', 'ǖ', 'ǘ', 'ǚ', 'ǜ']}


    replacement = {'uai': 'a', 'iao': 'a', 'ai' : 'a', 'ao' : 'a', 'ei' : 'e', 
                   'ia' : 'a', 'ie' : 'e', 'io' : 'o', 'iu' : 'u', 'ou' : 'o', 
                   'ua' : 'a', 'ue' : 'e', 'ui' : 'i', 'uo' : 'o', 'üa' : 'a', 
                   'üe' : 'e', 'a'  : 'a', 'e'  : 'e', 'i'  : 'i', 'o'  : 'o',
                   'u'  : 'u', 'ü'  : 'ü'}

    # copy the tone number and remove 
    # it from the end of the pinyin
    tone = pinyin[-1]
    pinyin = pinyin[0:-1]

    if tone == 5:
        return pinyin

    found_v = None
    for v in vowels:
        if v in pinyin: 
            found_v = v
            break

    if found_v is not None:
        pinyin = pinyin.replace(replacement[v], vowel[replacement[v]][int(tone)])

    return pinyin

if __name__ == "__main__":

    examples = ["yang3", "xie4", "feng1", "qian4", 
                "song4", "guan4", "cao3", "xi3", "wu4"]

    for e in examples:
        print(convert_pinyin(e))
