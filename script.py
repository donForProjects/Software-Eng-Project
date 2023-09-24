import glob

rootdir = 'img'
for path in glob.glob(f'{rootdir}/*/**/', recursive=True):
	print(path)
