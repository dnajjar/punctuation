
import string
import re
from gutenberg.cleanup import strip_headers
from gutenberg.acquire import load_etext
import spacy
import spacy
import spacy.util

nlp = spacy.load('en_core_web_sm')
#infixes = nlp.Defaults.infixes + (r'(?<=\d)[-–](?=[A-Z])')
#nlp.tokenizer.infix_finditer = spacy.util.compile_infix_regex(infixes).finditer

#exclusion list Dr. Mr. 
#spacy
#apostrophes 
#outlier detection
#apostrophe vs quotation mark (how to differentiate)
#sub non stanard with double quotes
#extract x pages from beginning/end
#testing 

#include hyphens and em-dashes
#exclude apostrophes

PUNCTUATION = "..." + string.punctuation + '“' + "'" + '‘' + '—' + '’'+ "'" + "«"+ "»" + "¡" + "¿"+"''"
PUNC_EXCLUSION_LIST = [] 
WORD_EXCLUSION_LIST = ["Dr." "Mr."]

def load_text_and_strip_headers(gutenberg_id):
  text = strip_headers(load_etext(gutenberg_id)).strip()
  stripped_text = re.sub("\n", " ", text)
  return stripped_text

def unpunctuate_exluded_words(text):
  #for words like Dr. and Mr., remove the colon so it isn't counted
  for excluded_word in WORD_EXCLUSION_LIST: 
    text = re.sub(excluded_word)
  pass


def pad_punctuation(text):
  punctuation = PUNCTUATION
  for excluded_punctuation in PUNC_EXCLUSION_LIST: 
    punctuation = punctuation.replace(excluded_punctuation, "")
  return text.translate(str.maketrans({key: " {0} ".format(key) for key in punctuation}))

def get_punctuation_with_word_counts(text):
  #FIX COUNT DICT FOR ELLIPSES
  padded_text = pad_punctuation(text)
  split_text = padded_text.split(" ")
  tracker = ""
  counter = 0
  count_dict = {}
  for word_or_punc in split_text:
    if word_or_punc == "":
      continue
    if re.match("\w+", word_or_punc) or re.match("’\w+", word_or_punc): #if it's a word, increment counter
      counter += 1
    else: #if punctuation
      if count_dict.get(word_or_punc): #if it's already in the dict 
        count_dict[word_or_punc] += 1 #increment count by 1
      else:
        count_dict[word_or_punc] = 1 #otherwise add to dict
      if counter != 0: #and preceded by word 
        tracker += str(counter) #add num words to tracker
      tracker += word_or_punc #and punc to tracker
      counter = 0 #reset num_words counter to zero 
  return tracker, count_dict

def get_punctuation_with_word_counts_from_spacy(text_list):
  counter = 0
  tracker = ""
  for word_or_punc in text_list:
    if word_or_punc.text == "":
      continue
    if re.match("\w+", word_or_punc.text):
      counter += 1
    else:
      if counter != 0:
        tracker += str(counter)
      tracker += word_or_punc.text
      counter = 0
  return tracker

def get_freq_from_counts(count_dict):
  total = sum(count_dict.values())
  freq_dict = {}
  for punc, count in count_dict.items():
    freq_dict[punc] = count/total * 100
  return freq_dict

don_quixote_clean_text = load_text_and_strip_headers(996)
don_quixote_analysis, count_dict = get_punctuation_with_word_counts(don_quixote_clean_text)
english_freq_dict = get_freq_from_counts(count_dict)


don_quixote_clean_text_french = load_text_and_strip_headers(42524)
don_quixote_analysis, count_dict = get_punctuation_with_word_counts(don_quixote_clean_text_french)
french_freq_dict = get_freq_from_counts(count_dict)

don_quixote_clean_text_spanish = load_text_and_strip_headers(2000)
don_quixote_analysis, count_dict = get_punctuation_with_word_counts(don_quixote_clean_text_spanish)
print(count_dict)
spanish_freq_dict = get_freq_from_counts(count_dict)

don_quixote_clean_text_italian = load_text_and_strip_headers(46914)
don_quixote_analysis, count_dict = get_punctuation_with_word_counts(don_quixote_clean_text_italian)
print('italian')
print(count_dict)
spanish_freq_dict = get_freq_from_counts(count_dict)




#SIMPLE TEST
sentence = ("And I shall remain satisfied, and proud to have been the first who has ever enjoyed "
  "the fruit of his writings as fully as he could desire; for my desire has been no other than to deliver"
" over to the detestation of mankind the false and foolish tales of the books of chivalry, which, thanks to "
"that of my true Don Quixote, are even now tottering, and doubtless doomed to fall for ever. Farewell.")
expected_punctuation = ",;,,,,.."

#spacy_tokenizer = list(nlp.tokenizer(sentence))
expected_punctuation_with_word_counts = "5,22;26,1,8,4,7.1."
actual_punctuation_with_word_counts, _count_dic = get_punctuation_with_word_counts(sentence)
print("Simple test")
print(expected_punctuation_with_word_counts == actual_punctuation_with_word_counts)
#punctuation_with_word_counts_from_spacy = get_punctuation_with_word_counts_from_spacy(spacy_tokenizer)

#LONGER TEST CHAPTER I
sentence_1 = ("In a village of La Mancha, the name of which I have no desire to call to mind, there lived not "
  "long since one of those gentlemen that keep a lance in the lance-rack, an old buckler, a lean hack, and a greyhound "
  "for coursing. An olla of rather more beef than mutton, a salad on most nights, scraps on Saturdays, lentils on Fridays, "
  "and a pigeon or so extra on Sundays, made away with three-quarters of his income. The rest of it went in a doublet of "
  "fine cloth and velvet breeches and shoes to match for holidays, while on week-days he made a brave figure in his best homespun. "
  "He had in his house a housekeeper past forty, a niece under twenty, and a lad for the field and market-place, who used to saddle "
  "the hack as well as handle the bill-hook. The age of this gentleman of ours was bordering on fifty; he was of a hardy habit, "
  "spare, gaunt-featured, a very early riser and a great sportsman. They will have it his surname was Quixada or Quesada "
  "(for here there is some difference of opinion among the authors who write on the subject), although from reasonable conjectures "
  "it seems plain that he was called Quexana. This, however, is of but little importance to our tale; it will be enough not to stray a "
  "hair’s breadth from the truth in the telling of it. You must know, then, that the above-named gentleman whenever he was at leisure "
  "(which was mostly all the year round) gave himself up to reading books of chivalry with such ardour and avidity that he almost "
  "entirely neglected the pursuit of his field-sports, and even the management of his property; and to such a pitch did his eagerness "
  "and infatuation go that he sold many an acre of tillageland to buy books of chivalry to read, and brought home as many of them "
  "as he could get.") 
expected_punctuation_with_word_counts = "6,12,16-1,3,3,5.8,5,3,3,8,4-4.20,3-10.9,4,8-1,12-1.11;6,1,1-1,8.10(16),12.1,1,8;9’10.3,1,3-7(7)23-1,7;26,11."
actual_punctuation_with_word_counts, _count_dic = get_punctuation_with_word_counts(sentence_1)
print("longer test")
print(expected_punctuation_with_word_counts == actual_punctuation_with_word_counts)

#EM DASH TEST
em_dash_sentence = ("There was, so the story goes, in a village near his own a very good-looking farm-girl with whom he had been at one time in love,"
" though, so far as is known, she never knew it nor gave a thought to the matter. Her name was Aldonza Lorenzo, and upon her he thought fit to confer "
"the title of Lady of his Thoughts; and after some search for a name which should not be out of harmony with her own, and should suggest and indicate that "
"of a princess and great lady, he decided upon calling her Dulcinea del Toboso—she being of El Toboso—a name, to his mind, musical, uncommon, and significant,"
" like all those he had already bestowed upon himself and the things belonging to him.")

expected_punctuation_with_word_counts = "2,4,9-2-11,1,5,11.5,15;17,12,8—5—2,3,1,1,2,15."

spacy_tokenizer = list(nlp.tokenizer(em_dash_sentence))
actual_punctuation_with_word_counts, _count_dic = get_punctuation_with_word_counts(em_dash_sentence)
punctuation_with_word_counts_from_spacy = get_punctuation_with_word_counts_from_spacy(spacy_tokenizer)
print("em dash test")
print(actual_punctuation_with_word_counts == expected_punctuation_with_word_counts)

#QUOTATION_TEST
quotation_sentence = ('“Hold!” said he, “for I am badly wounded through my horse’s fault; carry me to bed, and if possible send for the'
' wise Urganda to cure and see to my wounds.”')

expected_punctuation_with_word_counts = "“1!”2,“8’2;4,15.”"
actual_punctuation_with_word_counts, _count_dic = get_punctuation_with_word_counts(quotation_sentence)
print("quotation test")
print(actual_punctuation_with_word_counts == expected_punctuation_with_word_counts)

#ELLIPSES TEST
ellipses_sentence = ("Est-il possible? s'écria don Quichotte. Par ma foi, je n'y comprends rien, ou ce château est enchanté. "
  "Écoute bien ce que je vais te dire... mais avant tout jure-moi de ne révéler ce secret qu'après ma mort.")                   
expected_punctuation_with_word_counts = "1-2?1'3.3,2'3,5.8...4-7'3."
actual_punctuation_with_word_counts, _count_dic = get_punctuation_with_word_counts(ellipses_sentence)

print("ellipses test")
print(actual_punctuation_with_word_counts == expected_punctuation_with_word_counts)

ellipses_sentence_spanish = ("Tenga vuestra merced cuenta en las cabras que el pescador va pasando, porque si se pierde una de "
  "la memoria, se acabará el cuento y no será posible contar más palabra dél. «Sigo, pues, y digo que el desembarcadero de la otra parte estaba "
  "lleno de cieno y resbaloso, y tardaba el pescador mucho tiempo en ir y volver. Con todo esto, volvió por otra cabra, y otra, y otra...»")




#WORD EXCLUSION LIST TEST

  #"But of all there were none he liked so well as those of the famous Feliciano de Silva’s composition, for their "
#   "lucidity of style and complicated conceits were as pearls in his sight, particularly when in his reading he came upon courtships and "
#   "cartels, where he often found passages like “the reason of the unreason with which my reason is afflicted so weakens my reason that with "
#   "reason I murmur at your beauty;” or again, “the high heavens, that of your divinity divinely fortify you with the stars, render you deserving "
#   "of the desert your greatness deserves.” Over conceits of this sort the poor gentleman lost his wits, and used to lie awake striving to understand "
#   "them and worm the meaning out of them; what Aristotle himself could not have made out or extracted had he come to life again for that special purpose. "
#   "He was not at all easy about the wounds which Don Belianis gave and took, because it seemed to him that, great as were the surgeons who had cured him, "
#   "he must have had his face and body covered all over with seams and scars. He commended, however, the author’s way of ending his book with the promise "
#   "of that interminable adventure, and many a time was he tempted to take up his pen and finish it properly as is there proposed, which no doubt he would have "
#   "done, and made a successful piece of work of it too, had not greater and more absorbing thoughts prevented him. Many an argument did he have with "
#   "the curate of his village (a learned man, and a graduate of Siguenza) as to which had been the better knight, Palmerin of England or Amadis of Gaul. Master "
#   "Nicholas, the village barber, however, used to say that neither of them came up to the Knight of Phœbus, and that if there was any that could compare with him "
#   "it was Don Galaor, the brother of Amadis of Gaul, because he had a spirit that was equal to every occasion, and was no finikin knight, nor lachrymose "
#   "like his brother, while in the matter of valour he was not a whit behind him. In short, he became so absorbed in his books that he spent his nights "
#   "from sunset to sunrise, and his days from dawn to dark, poring over them; and what with little sleep and much reading his brains got so dry that he lost "
#   "his wits. His fancy grew full of what he used to read about in his books, enchantments, quarrels, battles, challenges, wounds, wooings, loves, agonies, "
#   "and all sorts of impossible nonsense; and it so possessed his mind that the whole fabric of invention and fancy he read of was true, that to him no history "
#   "in the world had more reality in it. He used to say the Cid Ruy Diaz was a very good knight, but that he was not to be compared with the Knight of the Burning "
#   "Sword who with one back-stroke cut in half two fierce and monstrous giants. He thought more of Bernardo del Carpio because at Roncesvalles he slew Roland in "
#   "spite of enchantments, availing himself of the artifice of Hercules when he strangled Antæus the son of Terra in his arms. He approved highly of the giant "
#   "Morgante, because, although of the giant breed which is always arrogant and ill-conditioned, he alone was affable and well-bred. But above all he admired "
#   "Reinaldos of Montalban, especially when he saw him sallying forth from his castle and robbing everyone he met, and when beyond the seas he stole that image "
#   "of Mahomet which, as his history says, was entirely of gold. To have a bout of kicking at that traitor of a Ganelon he would have given his housekeeper, "
#   "and his niece into the bargain. In short, his wits being quite gone, he hit upon the strangest notion that ever madman in this world hit upon, and that was that "
#   "he fancied it was right and requisite, as well for the support of his own honour as for the service of his country, that he should make a knight-errant of himself, "
#   "roaming the world over in full armour and on horseback in quest of adventures, and putting in practice himself all that he had read of as being the usual practices "
#   "of knights-errant; righting every kind of wrong, and exposing himself to peril and danger from which, in the issue, he was to reap eternal renown and fame. Already "
#   "the poor man saw himself crowned by the might of his arm Emperor of Trebizond at least; and so, led away by the intense enjoyment he found in these pleasant fancies, "
#   "he set himself forthwith to put his scheme into execution. The first thing he did was to clean up some armour that had belonged to his great-grandfather, and had been for "
#   "ages lying forgotten in a corner eaten with rust and covered with mildew. He scoured and polished it as best he could, but he perceived one great defect in it, that it had "
#   "no closed helmet, nothing but a simple morion. This deficiency, however, his ingenuity supplied, for he contrived a kind of half-helmet of pasteboard which, fitted on to the "
#   "morion, looked like a whole one. It is true that, in order to see if it was strong and fit to stand a cut, he drew his sword and gave it a couple of slashes, the first of "
#   "which undid in an instant what had taken him a week to do. The ease with which he had knocked it to pieces disconcerted him somewhat, and to guard against that danger he set "
#   "to work again, fixing bars of iron on the inside until he was satisfied with its strength; and then, not caring to try any more experiments with it, he passed it and adopted "
#   "it as a helmet of the most perfect construction. He next proceeded to inspect his hack, which, with more quartos than a real and more blemishes than the steed of Gonela, that "
#   "“tantum pellis et ossa fuit,” surpassed in his eyes the Bucephalus of Alexander or the Babieca of the Cid. Four days were spent in thinking what name to give him, because "
#   "(as he said to himself) it was not right that a horse belonging to a knight so famous, and one with such merits of his own, should be without some distinctive name, and he strove "
#   "to adapt it so as to indicate what he had been before belonging to a knight-errant, and what he then was; for it was only reasonable that, his master taking a new character, he should "
#   "take a new name, and that it should be a distinguished and full-sounding one, befitting the new order and calling he was about to follow. And so, after having composed, struck out, "
#   "rejected, added to, unmade, and remade a multitude of names out of his memory and fancy, he decided upon calling him Rocinante, a name, to his thinking, lofty, sonorous, and significant "
#   "of his condition as a hack before he became what he now was, the first and foremost of all the hacks in the world. Having got a name for his horse so much to his taste, he was anxious "
#   "to get one for himself, and he was eight days more pondering over this point, till at last he made up his mind to call himself “Don Quixote,” whence, as has been already said, the authors "
#   "of this veracious history have inferred that his name must have been beyond a doubt Quixada, and not Quesada as others would have it. Recollecting, however, that the valiant Amadis was "
#   "not content to call himself curtly Amadis and nothing more, but added the name of his kingdom and country to make it famous, and called himself Amadis of Gaul, he, like a good knight, "
#   "resolved to add on the name of his, and to style himself Don Quixote of La Mancha, whereby, he considered, he described accurately his origin and country, and did honour to it in taking "
#   "his surname from it. So then, his armour being furbished, his morion turned into a helmet, his hack christened, and he himself confirmed, he came to the conclusion that nothing more was "
#   "needed now but to look out for a lady to be in love with; for a knight-errant without love was like a tree without leaves or fruit, or a body without a soul. As he said to himself, “If, "
#   "for my sins, or by my good fortune, I come across some giant hereabouts, a common occurrence with knights-errant, and overthrow him in one onslaught, or cleave him asunder to the waist, or, "
#   "in short, vanquish and subdue him, will it not be well to have someone I may send him to as a present, that he may come in and fall on his knees before my sweet lady, and in a humble, submissive "
#   "voice say, ‘I am the giant Caraculiambro, lord of the island of Malindrania, vanquished in single combat by the never sufficiently extolled knight Don Quixote of La Mancha, who has commanded "
#   "me to present myself before your Grace, that your Highness dispose of me at your pleasure’?” Oh, how our good gentleman enjoyed the delivery of this speech, especially when he had thought "
#   "of someone to call his Lady! There was, so the story goes, in a village near his own a very good-looking farm-girl with whom he had been at one time in love, though, so far as is known, "
#   "she never knew it nor gave a thought to the matter. Her name was Aldonza Lorenzo, and upon her he thought fit to confer the title of Lady of his Thoughts; and after some search for a name "
#   "which should not be out of harmony with her own, and should suggest and indicate that of a princess and great lady, he decided upon calling her Dulcinea del Toboso—she being of El "
#   "Toboso—a name, to his mind, musical, uncommon, and significant, like all those he had already bestowed upon himself and the things belonging to him.)"
