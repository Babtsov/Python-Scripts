from math import factorial
permutations = 0;


def recursive_permute(acc,split_str):
	if len(split_str) == 1:
		print(acc,split_str,sep='') # print the entire permutation
		global permutations
		permutations += 1
		return
	for index, char in enumerate(split_str):
		recursive_permute(acc + char , split_str[:index] + split_str[index + 1:])


def permute(string):
	recursive_permute('',string)


string = input('Enter a string to permute:')
permute(string)
assert(permutations == factorial(len(string))) # sanity check
