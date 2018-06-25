from pinyin import decode_pinyin

def test_decode():
    assert 'tái' == decode_pinyin('tai2')
    assert 'nán' == decode_pinyin('nan2')
    assert 'táinán' == decode_pinyin('tai2nan2')
    assert 'nǎi jīng' == decode_pinyin('nai3 jing1')
    assert 'cloud9' == decode_pinyin('cloud9')
    assert 'Mǎ kè sī · Liè níng zhǔ yì' == decode_pinyin('Ma3 ke4 si1 · Lie4 ning2 zhu3 yi4')
