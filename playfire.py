import numpy
import math

# Removes any extra characters from the phrase
# while conserving the order of the elements.
def cleanPhrase(phrase):
	word = []
	for c in phrase:
		repeated = False
		i = 0
		while i < len(word) and not repeated:
			repeated = word[i] == c
			i = i + 1 
		if not repeated:
			word.append(c)
	return word

# Generate & returns the base or default key
# that needs to be combined with the keyword.
def generateDefaultKey():
	defaultKey = []
	for i in range(10):
		defaultKey.append(chr(ord('0') + i))
	for i in range(26):
		defaultKey.append(chr(ord('A') + i))
	defaultKey += list("!“#$%&‘()*+,-./:;<=>?@[\]^_|")
	return defaultKey

# Generates & return the specific key
# in accordance with the keyword given.
def generateKey(keyWord):
	defaultKey = generateDefaultKey()
	# Create a 4x4x4 3d matrix.
	key = numpy.chararray((4,4,4), unicode = True)
	# Default all values in the key to be empty. 
	key[:] = ''
	# For use with the defualtKey as index.
	l = 0
	# For use with the keyWord as index.
	m = 0
	# Fill in the 3d array with the characters from the default key,
	# first inserting the ones from the keyword and then the remaining ones.
	for i in range(4):
		for j in range(4):
			for k in range(4):
				if m < len(keyWord):
					key[i][j][k] = keyWord[m]
					m = m + 1
				else:
					repeated = False
					while l < len(defaultKey) and not repeated:
						w = 0
						while w < len(keyWord) and not repeated:
							repeated = defaultKey[l] == keyWord[w]
							w = w + 1
						if not repeated:
							key[i][j][k] = defaultKey[l]
						# If a character is repeated, we need a new candidate,
						# therefore we reset the value.
						# Likewise, if we need to exit the loop, we need to reset the value.
						repeated = not repeated
						l = l + 1
	return key

# Given a text and the type of text it is,
# generate a trigraph for it and return it.
def generateTrigraph(text, type):
	if type == "plain":
		return generateTrigraphFromPlainText(text)
	elif type == "cipher":
		return generateTrigraphFromCipherText(text)
	else:
		return []

# A plain text trigraph needs to consider repeated letters,
# as well as unfinished trigraphs.
def generateTrigraphFromPlainText(plainText):
	# The number of trigraphs is always the size of the plain text
	# divided by 3 rounded up.
	size = math.ceil(len(plainText) / 3)
	# Create a sizex3 matrix.
	trigraphs = numpy.chararray((size,3), unicode = True)
	# Set all values in the matrix to be empty.
	trigraphs[:] = ''
	# For use with the plainText as index.
	p = 0
	# Depending on the position of the character in the trigraph,
	# different consideration need to be taken, but in general
	# we look to add the plainText in order.
	for i in range(size):
		# Number of special characters ('X', 'Z') to insert;
		# everytime we begin the loop we reset it, and
		# always add the character to the trigraph.
		insert = 0
		for j in range(3):
			# If the character is the second or third position,
			# make sure no letters are repeated or index is out of bounds.
			if j > 0:
				if p >= len(plainText) or trigraphs[i][j - 1] == plainText[p]:
					insert = insert + 1
			# If no additional characters are needed, simply add the next
			# character to the current trigraph.
			if insert == 0:
				trigraphs[i][j] = plainText[p]
				p = p + 1
			# Otherwise, depeding on the character padding needed,
			# add the appropiate one.s
			if insert == 1:
				trigraphs[i][j] = 'X'
			if insert == 2:
				trigraphs[i][j] = 'Z'
	return trigraphs

# A plain cipher trigraph only needs to divide the text
# into sets of three characters.
def generateTrigraphFromCipherText(cipherText):
	# The number of trigraphs is always the size of the plain text
	# divided by 3 rounded up.
	size = math.ceil(len(cipherText) / 3)
	# Create a sizex3 matrix.
	trigraphs = numpy.chararray((size,3), unicode = True)
	# Set all values in the matrix to be empty.
	trigraphs[:] = ''
	# For use with the plainText as index.
	p = 0
	# Iterate over the trigraph array and add the characters
	# from the cipher text.
	for i in range(size):
		for j in range(3):
			trigraphs[i][j] = cipherText[p]
			p = p + 1
	return trigraphs

# Obtain the coordinates (index) of a character
# in a given key.
def indexOf(key, char):
	# Initialize all indices to 0.
	i = j = k = 0
	found = False
	while i < 4 and not found:
		found = char == key[i][j][k]
		if found:
			break
		# Loop over the matrix.
		k = k + 1
		if k == 4:
			j = j + 1
			k = 0
			if j == 4:
				i = i + 1
				j = 0
	return {'i': i, 'j': j, 'k': k}

# Given a 3x3x3 matrix, add all the characters
# into a string.
def toString(array):
	string = ""
	for a in array:
		for b in a:
			for c in b:
				string += c
	return string

# Given a plain text and a keyphrase,
# encrypt the text using a Playfire algorithm.
def encrypt(plainText, keyPhrase):
	# Obtain a clean keyword from the keyphrase
	# with no repeated characters.
	keyWord = cleanPhrase(keyPhrase)
	# Obtain the corresponding key using the given keyword.
	key = generateKey(keyWord)
	# Divide the plain text into trigraphs.
	trigraphs = generateTrigraph(plainText, "plain")
	# Iterate over the trigraph, swaping characters
	# with its corresponding value given the current key.
	for i in range(len(trigraphs)):
		# Obtain the indices for all the characters in the trigraph.
		indices = []
		indices.append(indexOf(key, trigraphs[i][0]))
		indices.append(indexOf(key, trigraphs[i][1]))
		indices.append(indexOf(key, trigraphs[i][2]))
		# Encryption proccess was found through trial and error
		# based on the original algorithm to match it.
		for j in range(3):
			if j == 0:
				trigraphs[i][j] = key[indices[2]['i']][indices[0]['j']][indices[1]['k']]
			if j == 1:
				trigraphs[i][j] = key[indices[0]['i']][indices[1]['j']][indices[2]['k']]
			if j == 2:
				trigraphs[i][j] = key[indices[1]['i']][indices[2]['j']][indices[0]['k']]
	# Return the cipherText in trigraph format as a string.
	return toString(trigraphs)

# Given a cipher text and a key phrase,
# decrypt the text using a Playfire algorithm.
def decrypt(cipherText, keyPhrase):
	# Obtain a clean keyword from the keyphrase
	# with no repeated characters.
	keyWord = cleanPhrase(keyPhrase)
	# Obtain the corresponding key using the given keyword.
	key = generateKey(keyWord)
	# Divide the cipher text into trigraphs.
	trigraphs = generateTrigraph(cipherText, "cipher")
	# Iterate over the trigraph, swaping characters
	# with its corresponding value given the current key.
	for i in range(len(trigraphs)):
		# Obtain the indices for all the characters in the trigraph.
		indices = []
		indices.append(indexOf(key, trigraphs[i][0]))
		indices.append(indexOf(key, trigraphs[i][1]))
		indices.append(indexOf(key, trigraphs[i][2]))
		# Decryption proccess was found through trial and error
		# based on the original algorithm to match it.
		for j in range(3):
			if j == 0:
				trigraphs[i][j] = key[indices[1]['i']][indices[0]['j']][indices[2]['k']]
			if j == 1:
				trigraphs[i][j] = key[indices[2]['i']][indices[1]['j']][indices[0]['k']]
			if j == 2:
				trigraphs[i][j] = key[indices[0]['i']][indices[2]['j']][indices[1]['k']]
	# Return the cipherText in trigraph format as a string.
	return toString(trigraphs)

# Key phrase and plain text to test the algorith with.
keyPhrase = "FRIENDS4V@TJ_201.C"
plainText = "M.TECH@THESIS"

# Obtain the matching key and print it.
keyWord = cleanPhrase(keyPhrase)
key = generateKey(keyWord)
print(key)

# Obtain the ciphered and print it.
cipherText = encrypt(plainText, keyPhrase)
print(cipherText)

# Obtain the deciphered and print it.
decipheredText = decrypt(cipherText, keyPhrase)
print(decipheredText)