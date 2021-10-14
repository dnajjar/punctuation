#sources:
#English: https://almabooks.com/wp-content/uploads/2016/10/Little-Prince-final-text.pdf
#French: https://gutenberg.net.au/ebooks03/0300771h.html?fbclid=IwAR2x-93AH_qrAA_ZMBH9ilAZEpSYQ-FzeJphnkrTWf862wvNMuTRChrXUA0
#Spanish: http://www.agirregabiria.net/g/sylvainaitor/principito.pdf
#Italian: https://portalebambini.it/wp-content/uploads/2017/11/Il-piccolo-principe.pdf
#Portuguese: https://www.sesirs.org.br/sites/default/files/paragraph--files/o_pequeno_principe_-_antoine_de_saint-exupery_0.pdf
import string 
import re 
PUNCTUATION = "…" + string.punctuation + '“' + "'" + '‘' + '—' + '’'+ "'" + "«"+ "»" + "¡" + "¿"+"''"
PUNC_EXCLUSION_LIST = ['\n', "«", "»", '"', '“', '”'] 

#Graf 1: First sentence to drawing of a hat
petit_prince_para_1 = {
'English':"""Once, when I was six years old, I saw a marvellous picture in a
book on rainforests called Real-Life Stories. It depicted a boa
  constrictor swallowing a wild animal. Here is a replica of the picture.
  In the book it said: “Boa constrictors swallow their prey whole, without 
  chewing. Afterwards they cannot move, and sleep for six months digesting.” I
  thought a great deal about goings-on in the jungle and, in turn, with a
  crayon, managed to produce my first drawing. My drawing number 1. It was 
  like this:""", 
'French': """Lorsque j'avais six ans j'ai vu, une fois, une magnifique image,
  dans un livre sur la Forêt Vierge qui s'appelait "Histoires Vécues". Ça 
  représentait un serpent boa qui avalait un fauve. Voilà la copie du dessin.
  On disait dans le livre: "Les serpents boas avalent leur proie tout entière, 
  sans la mâcher. Ensuite ils ne peuvent plus bouger et ils dorment pendant les
  six mois de leur digestion". J'ai alors beaucoup réfléchi sur les aventures de
  la jungle et, à mon tour, j'ai réussi, avec un crayon de couleur, à tracer mon
  premier dessin. Mon dessin numéro 1. Il était comme ça:""",
'Spanish': """Cuando yo tenía seis años vi en un libro sobre la selva virgen
  que se titulaba "Historias vividas", una magnífica lámina. Representaba una
  serpiente boa que se tragaba a una fiera. En el libro se afirmaba: "La serpiente
  boa se traga su presa entera, sin masticarla. Luego ya no puede moverse y duerme
  durante los seis meses que dura su digestión". Reflexioné mucho en ese momento sobre
  las aventuras de la jungla y a mi vez logré trazar conun lápiz de colores mi primer 
  dibujo. Mi dibujo número 1 era de esta manera:""",
'Portuguese':"""Certa vez, quando tinha seis anos, vi num livro sobre a Floresta
  Virgem, "Histórias Vividas", uma imponente gravura. Representava ela uma
  jibóia que engolia uma fera. Eis a cópia do desenho. Dizia o livro: "As
  jibóias engolem, sem mastigar, a presa inteira. Em seguida, não podem
  mover-se e dormem os seis meses da digestão." Refleti muito então sobre as
  aventuras da selva, e fiz, com lápis de cor, o meu primeiro desenho. 
  Meu desenho número 1 era assim:""",
'Italian':"""Un tempo lontano, quando avevo sei anni, in un libro sulle
  foreste primordiali, intitolato «Storie vissute della natura», vidi
  un magnifico disegno. Rappresentava un serpente boa nell'atto
  di inghiottire un animale. Eccovi la copia del disegno. C'era
  scritto: «I boa ingoiano la loro preda Tutta intera, senza
  masticarla. Dopo di che non riescono più a muoversi e
  dormono durante i sei mesi che la digestione richiede».
  Meditai a lungo sulle avventure della jungla. E a mia volta
  riuscii a tracciare il mio primo disegno. Il mio disegno numero
  uno. Era così:""",
}

def pad_text(text): 
  #adds spaces around each punctuation mark so that we can later split on them
  #see test_pad_text for example
  punctuation = PUNCTUATION
  text = re.sub('\.\.\.','…',text) #takes care of cases where ellipses are ... not … so that they aren't treated as 3 separate dots
  return text.translate(str.maketrans({key: " {0} ".format(key) for key in punctuation}))

def get_punctuation_counts(text):
  #returns a dictionary of unique punctuation marks with their counts
  #see test_get_punctuation_counts()
  split_text = text.split(" ")
  count_dict = {}
  for word_or_punc in split_text:
    if word_or_punc == "":
      continue
    elif not re.match("\w+", word_or_punc) or re.match("’\w+", word_or_punc):
      if word_or_punc not in PUNC_EXCLUSION_LIST:
        if count_dict.get(word_or_punc): #if it's already in the dict 
          count_dict[word_or_punc] += 1 #increment count by 1
        else:
          count_dict[word_or_punc] = 1 #otherwise add to dict
  return count_dict

for language, text in petit_prince_para_1.items(): 
  padded_text = pad_text(text)
  counts = get_punctuation_counts(padded_text)
  print(language, counts)

#############################TESTS########################################
def test_pad_text():
  test_string = "Grown-ups never understand anything on their own, and it’s tiring, for children, to be for ever and ever explaining…"
  actual_padding = pad_text(test_string)
  expected_padding = "Grown - ups never understand anything on their own ,  and it ’ s tiring ,  for children ,  to be for ever and ever explaining … "
  print(actual_padding == expected_padding)

def test_pad_text_with_ellipses():
  test_string = "Grown-ups never understand anything on their own, and it’s tiring, for children, to be for ever and ever explaining..."
  actual_padding = pad_text(test_string)
  expected_padding = "Grown - ups never understand anything on their own ,  and it ’ s tiring ,  for children ,  to be for ever and ever explaining … "
  print(actual_padding == expected_padding)

def test_get_punctuation_counts():
  test_padded_string = "Grown - ups never understand anything on their own ,  and it ’ s tiring ,  for children ,  to be for ever and ever explaining … "
  actual_count_dict = get_punctuation_counts(test_padded_string)
  expected_count_dict = {'-': 1, ',': 3, '’': 1, "…": 1}
  print(actual_count_dict == expected_count_dict)

test_pad_text()
test_pad_text_with_ellipses()
test_get_punctuation_counts()