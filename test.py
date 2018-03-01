import numpy
import math

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

def generateDefaultKey():
	defaultKey = []
	for i in range(10):
		defaultKey.append(chr(ord('0') + i))
	for i in range(26):
		defaultKey.append(chr(ord('A') + i))
	defaultKey += list("!“#$%&‘()*+,-./:;<=>?@[\]^_|")
	return defaultKey

def generateKey(keyWord):
	defaultKey = generateDefaultKey()
	key = numpy.chararray((4,4,4), unicode = True)
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

def generateTrigraph(text, type):
	if type == "plain":
		return generateTrigraphFromPlainText(text)
	elif type == "cipher":
		return generateTrigraphFromCipherText(text)
	else:
		return []

def generateTrigraphFromPlainText(plainText):
	size = math.ceil(len(plainText) / 3)
	trigraphs = numpy.chararray((size,3), unicode = True)
	trigraphs[:] = ''
	# For use with the plainText as index.
	p = 0
	for i in range(size):
		for j in range(3):
			if j == 0:
				# Number of special characters ('X', 'Z') to insert.
				insert = 0
			if j == 1:
				if p >= len(plainText) or trigraphs[i][j - 1] == plainText[p]:
					insert = insert + 1
			if j == 2:
				if p >= len(plainText) or trigraphs[i][j - 1] == plainText[p]:
					insert = insert + 1
			if insert == 0:
				trigraphs[i][j] = plainText[p]
				p = p + 1
			if insert == 1:
				trigraphs[i][j] = 'X'
			if insert == 2:
				trigraphs[i][j] = 'Z'
	return trigraphs

def generateTrigraphFromCipherText(cipherText):
	size = math.ceil(len(cipherText) / 3)
	trigraphs = numpy.chararray((size,3), unicode = True)
	trigraphs[:] = ''
	# For use with the plainText as index.
	p = 0
	for i in range(size):
		for j in range(3):
			trigraphs[i][j] = cipherText[p]
			p = p + 1
	return trigraphs

def indexOf(key, char):
	i = j = k = 0
	found = False
	while i < 4 and not found:
		found = char == key[i][j][k]
		if found:
			break
		k = k + 1
		if k == 4:
			j = j + 1
			k = 0
			if j == 4:
				i = i + 1
				j = 0
	return {'i': i, 'j': j, 'k': k}

def toString(array):
	string = ""
	for a in array:
		for b in a:
			for c in b:
				string += c
	return string

def encrypt(plainText, keyPhrase):
	keyWord = cleanPhrase(keyPhrase)
	key = generateKey(keyWord)
	trigraphs = generateTrigraph(plainText, "plain")
	for i in range(len(trigraphs)):
		indices = []
		indices.append(indexOf(key, trigraphs[i][0]))
		indices.append(indexOf(key, trigraphs[i][1]))
		indices.append(indexOf(key, trigraphs[i][2]))
		# i == floor, j == row, k == column.
		for j in range(3):
			if j == 0:
				trigraphs[i][j] = key[indices[2]['i']][indices[0]['j']][indices[1]['k']]
			if j == 1:
				trigraphs[i][j] = key[indices[0]['i']][indices[1]['j']][indices[2]['k']]
			if j == 2:
				trigraphs[i][j] = key[indices[1]['i']][indices[2]['j']][indices[0]['k']]
	return toString(trigraphs)

def decrypt(cipherText, keyPhrase):
	keyWord = cleanPhrase(keyPhrase)
	key = generateKey(keyWord)
	trigraphs = generateTrigraph(cipherText, "cipher")
	for i in range(len(trigraphs)):
		indices = []
		indices.append(indexOf(key, trigraphs[i][0]))
		indices.append(indexOf(key, trigraphs[i][1]))
		indices.append(indexOf(key, trigraphs[i][2]))
		# i == floor, j == row, k == column.
		for j in range(3):
			if j == 0:
				trigraphs[i][j] = key[indices[1]['i']][indices[0]['j']][indices[2]['k']]
			if j == 1:
				trigraphs[i][j] = key[indices[2]['i']][indices[1]['j']][indices[0]['k']]
			if j == 2:
				trigraphs[i][j] = key[indices[0]['i']][indices[2]['j']][indices[1]['k']]
			
	return toString(trigraphs)

keyPhrase = "FRIENDS4V@TJ_201.C"
plainText = "M.TECH@THESIS"
cipherText = encrypt(plainText, keyPhrase)
print(cipherText)
decipheredText = decrypt(cipherText, keyPhrase)
print(decipheredText)