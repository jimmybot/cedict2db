import re

PINYIN_TONE_MARK = {
    0: 'aoeiuvü',
    1: 'āōēīūǖǖ',
    2: 'áóéíúǘǘ',
    3: 'ǎǒěǐǔǚǚ',
    4: 'àòèìùǜǜ'
}

PUNCTUATION = {
    ' ',
    '-',    # hyphen
    '–',    # endash
    '—',    # emdash
    '\t',
    '\n',
    '.',
    ',',
    '?',
    '!',
    ':',
    ';',
    '。',
    ',',
    '？',
    '！',
    '：',
    '；',
}

def decode_pinyin(pinyin_numerical):
    r = ""
    t = ""
    for c in pinyin_numerical:
        # convenience for ü
        if c == 'v':
            t += 'ü'
        # another convenience for ü
        elif c == ':' and len(t) >= 1 and t[-1] == 'u':
            t = t[:-1] + "\u00fc"
        elif c >= '0' and c <= '5' or c in PUNCTUATION:
            if c >= '0' and c <= '5':
                tone = int(c) % 5
                if tone != 0:
                    m = re.search("[aoeiuv\u00fc]+", t)
                    if m is None:
                        t += c
                    elif len(m.group(0)) == 1:
                        t = t[:m.start(0)] + PINYIN_TONE_MARK[tone][PINYIN_TONE_MARK[0].index(m.group(0))] + t[m.end(0):]

                    # more than one match so we need to figure out which vowel to mark
                    else:
                        before = t
                        if 'a' in t:
                            t = t.replace("a", PINYIN_TONE_MARK[tone][0])
                        elif 'o' in t:
                            t = t.replace("o", PINYIN_TONE_MARK[tone][1])
                        elif 'e' in t:
                            t = t.replace("e", PINYIN_TONE_MARK[tone][2])
                        elif t.endswith("ui"):
                            t = t.replace("i", PINYIN_TONE_MARK[tone][3])
                        elif t.endswith("iu"):
                            t = t.replace("u", PINYIN_TONE_MARK[tone][4])
            else:
                t += c
            r += t
            t = ""
        else:
            t += c
    r += t
    #print("%s | %s" % (pinyin_numerical, r))
    return r
