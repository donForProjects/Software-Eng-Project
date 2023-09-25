import glob

rootdir = 'img'
for path in glob.glob(f'{rootdir}/*/**/', recursive=True):
	print(path)




a_string = "!(Hello World)@"

remove = "!()@"

for char in remove:
    a_string = a_string.replace(char, "")

print(a_string)