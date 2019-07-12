def link_starts_with(link):
    for variant in link_start:
        if variant in link:
            return True
    return False


def is_correct(link):
    if link_starts_with(link) and ('peers=' in link or 'sel' in link):
        need_to_check_ids[link] = []
        return True
    unused_links.append(link)
    return False


def has_peer_or_sel(line, tag):
    if tag in line:
        line = line.strip()
        print(line) # checking print
        line_tag = line[(len(tag)):].split('_')
        print(line_tag) #checking print
        for element in line_tag:
            print(element) #checking print
            if not (element == '' or element[0].isalpha()) and element[1:].isdigit():
                used_ids.add(int(element))


def check_user_type(id_number):
    if id_number < 0:
        user_type.append('группа')
        a = 'club'
    elif id_number > 0:
        user_type.append('пользователь')
        a = 'id'
    user_id.append(abs(id_number))
    user_link.append(f'http://vk.com/{a}{abs(id_number)}')


used_ids = set()
unused_links = []
need_to_check_ids = {}
user_type = []
user_id = []
user_link = []
link_start = ["https://new.vk.com", "https://vk.com", "http://new.vk.com", "http://vk.com"]

with open("links.txt") as resourse:
    for line in resourse:
        if is_correct(line):
            newline = line.split('?')[1]
            content = newline.split('&amp;')
            for elem in content:
                has_peer_or_sel(elem, 'peers=')
                has_peer_or_sel(elem, 'sel=')
                need_to_check_ids[line].append(elem)

data = sorted(list(used_ids))
print(data) #checking print
for value in data:
    check_user_type(value)

with open('report.html', 'w') as report:
    report.write('<html>')
    for i in range(len(data)):
        report.write(f'<a href={user_link[i]}>Тип - {user_type[i]}, id - {user_id[i]}</a><br>')
    report.write('</html>')

with open('reject.txt', 'w') as reject:
    for i in range(len(unused_links)):
        reject.write(unused_links[i])

print("\nReport is ready")