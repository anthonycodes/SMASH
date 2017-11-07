# Imports
import random
import sys
import argparse

# Variables
int_to_alpha_r1 = {
	"0": "a",
	"1": "b",
	"2": "c",
	"3": "d",
	"4": "e",
	"5": "f"
}

int_to_alpha_r2 = {
	"6": "0",
	"7": "1",
	"8": "2",
	"9": "3"
}

# Functions
def translate(istr, dictionary):
	olist = []

	for letter in istr:
		translation = dictionary.get(letter)
		olist.append(str(translation) if translation else str(letter))

	return "".join(olist)

def shift(l, n):
    if n < 0:
        raise ValueError("[ERROR] 'n' must be a positive integer.")
    if n > 0:
        l.insert(0, l.pop(-1))
        shift(l, n - 1)

def hash(source):
	source = str(source)

	primary_hash = []
	secondary_hash = []

	sseed = random.seed(source)
	rint = list(str(random.randint(10000000000000000000000000000000, 99999999999999999999999999999999)))
	
	for k, v in enumerate(rint):
		primary_hash.append(translate(v, int_to_alpha_r1))
		secondary_hash.append(translate(v, int_to_alpha_r2))

	hash_table = list("".join(primary_hash) + "".join(secondary_hash))
	ph = len(primary_hash)
	sh = len(secondary_hash)

	random.seed(source + str(ph) + str(sh))

	shift_by = int((ph / sh) + (random.randint(1000, 9999) / (ph + sh)))
	shift(hash_table, shift_by)

	return "".join(hash_table)

# Main
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = "Hash a string with SMASH", prog = "smash", epilog = "More help and source code available here: https://github.com/anthonycodes/SMASH")
	mode = parser.add_mutually_exclusive_group()

	parser.add_argument("source", type = str, nargs = "+", help = "The source of what to hash. Either a string or a file name.")
	mode.add_argument("-f", "--file", help = "indicates if what you want to hash is a file", action = "store_true")
	mode.add_argument("-b", "--bytes", help = "indicates if what you want to hash is a bytes file", action = "store_true")

	args = parser.parse_args()
	source = " ".join(args.source)

	if args.file or args.bytes:
		file_contents = []
		try:
			if args.bytes:
				with open(source, "rb") as file:
					rawfile = str(file.read())
				
				rawfile = "".join(file_contents)

			elif args.file:
				with open(source, "r") as file:
					rawfile = str(file.read())
			source = rawfile

		except Exception as err:
			print("There was a problem opening the file.")
			print("[\n{}\n]".format(err))

			sys.exit()

	print(hash(source))
