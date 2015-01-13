import sys
import random
import string
import pdb

guess_count = 0
answer = ''
list_of_words = []
word_dict = {}
category = {1:'COMPUTER_DEVICES', 2:'ANIMALS' , 3:'BIRDS' , 4:'SPORTS' }

for i,j in category.items():
    print "Category number for %s ===> %d\n" %(j,i)

category_input = input("\nSelect a Category number : ")

category_file = 'C:\\Python27\\'+category[category_input].lower()+'.txt'

word_file = open(category_file).readlines()

for data in word_file:
    list_of_words.append(data.strip('\n'))
    
word = list_of_words[random.randrange(len(list_of_words))]



word_len = len(word)

for i in range(word_len):
    word_dict[i] = '_'

while 1:
    if guess_count < 7:
        if '_' in word_dict.values():
            
            print "The word have %s characters\n" %word_len
            user_input = raw_input('Enter a character: ')
            user_input = user_input.upper()
            

            if user_input in word:
                for i,j in enumerate(word):
                    if j == user_input:
                        word_dict[i] = user_input
                print "\nThe Character %c is present in the word \n" %user_input 
               
                print "\n\n" ,word_dict.values(), "\n\n"
             
                   
                
           
            else:
                print "\nThe Character %c is not present in the word \n" %user_input
                guess_count += 1
        else:
            for i in word_dict.values():
                answer += i
            print "PERFECT!! \nAnswer is %s :)" %answer
            break
            
    
             
    else:
        print "No more chances :("
        break





sys.exit()    
