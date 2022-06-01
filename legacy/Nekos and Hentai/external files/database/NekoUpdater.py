import urllib.request

url = 'https://ln.topdf.de/files/'
name_names = 'all_files'
names_external_files = []

with urllib.request.urlopen(url + name_names) as table:
    for row in table:
        names_external_files.append(row.decode('utf-8').rstrip('\n'))

print(names_external_files)

def install():
    print('download stuff please hold on')
    urllib.request.urlretrieve(url + names_external_files[0], names_external_files[0])
    print(url + names_external_files[0], names_external_files[0])
    try:
        with open(names_external_files[1]):
            pass
    except:
        urllib.request.urlretrieve(url + names_external_files[1], names_external_files[1])

    for i in range(len(names_external_files) - 2):
        try:
            urllib.request.urlretrieve(url + names_external_files[i + 2], names_external_files[i + 2])
            print(url + names_external_files[i + 2], names_external_files[i + 2])
        except:
            print('faieled')
            print(url + names_external_files[i + 2], names_external_files[i + 2])


install()
