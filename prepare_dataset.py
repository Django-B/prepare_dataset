import glob, os
from math import *
import shutil

INPUT_FOLDERS = [
	'flower_photos/daisy/',
	'flower_photos/dandelion/',
	'flower_photos/roses/',
	'flower_photos/sunflowers/',
	'flower_photos/tulips/',
]

BASE_DIR_ABSOLUTE = '/home/django/code/prepare_dataset'
OUT_DIR = './prepared_flowers/'

OUT_TRAIN = OUT_DIR+'train/'
OUT_VAL = OUT_DIR+'test/'

COEFF = [80, 20] # train/test
EXCEPTIONS = ['classes']

if int(COEFF[0]) + int(COEFF[1]) > 100:
	print('COEFF can\'t exceed 100%')
	exit(1)

def chunker(seq, size):
	return (seq[pos:pos+size] for pos in range(0, len(seq), size))

source = {}
for sf in INPUT_FOLDERS:
	source.setdefault(sf, [])

	os.chdir(BASE_DIR_ABSOLUTE)
	os.chdir(sf)

	for filename in glob.glob('*.jpg'):
		source[sf].append(filename)

print(f'Source:\n{source}')

train = {}
val = {}
for sk, sv in source.items():
	chunks = 10
	train_chunk = floor(chunks * (COEFF[0]/100))
	val_chunk = chunks - train_chunk

	train.setdefault(sk, [])
	val.setdefault(sk, [])
	for item in chunker(sv, chunks):
		train[sk].extend(item[0:train_chunk])
		val[sk].extend(item[train_chunk:])

train_sum = 0
val_sum = 0

for sk, sv in train.items():
	train_sum += len(sv)

for sk, sv in val.items():
	val_sum += len(sv)

os.chdir(BASE_DIR_ABSOLUTE)
for sk, sv in train.items():
	for item in sv:
		imgfile_source = sk + item
		imgfile_dest = OUT_TRAIN + sk.split('/')[-2] + '/'

		os.makedirs(imgfile_dest, exist_ok=True)
		shutil.copyfile(imgfile_source, imgfile_dest+item)

os.chdir(BASE_DIR_ABSOLUTE)
for sk, sv in val.items():
	for item in sv:
		imgfile_source = sk + item
		imgfile_dest = OUT_VAL + sk.split('/')[-2] + '/'

		os.makedirs(imgfile_dest, exist_ok=True)
		shutil.copyfile(imgfile_source, imgfile_dest+item)

print('\nDONE!')
