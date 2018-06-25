Convert open CEDict Mandarin-English data to sqlite database format

Chinese-English (中英辭典) works better because that is the intended direction
English-Chinese (英中辭典) works okay but misses many words, even common ones, because it is not the original intended direction

Features:
- Forwards and backwards dictionary tables, Mandarin-English and English-Mandarin
- Converts numerical pinyin markers to actual pinyin
- Pinyin conversion will allow through punctuation or English letter literals
- Convert definition column to format: <def1> | <def2> | <def3

Example entry:
```
天馬行空|天马行空|tiān mǎ xíng kōng|like a heavenly steed, soaring across the skies (idiom) | (of writing, calligraphy etc) bold and imaginative | unconstrained in style
```
