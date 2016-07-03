def break_words(stuff):
  """this function will break up words for us."""
  words = stuff.split(' ')
  return words
  
def sort_words(words):
  """sorts the words."""
  return sorted(words)
  
def print_first_word(words):
  """prints the 1st word after popping it off."""
  word = words.pop(0)#因为pop()是移除函数w
  print(word)
 
def print_last_word(words):
  """prints the last."""
  word = words.pop(-1)
  print(word)
  
def sort_sentence(sentence):
  """takes in a full sentence and return the sorted words."""
  words = break_words(sentence)
  return sort_words(words)
  
def print_first_and_last(sentence):
  """print the first and last."""
  words = break_words(sentence)
  print_first_word(words)  
  print_last_word(words)
  
def print_first_and_last_sorted(sentence):
  """sorts the  words then first and last."""  
  words = sort_sentence(sentence)
  print_first_word(words)
  print_last_word(words)
  