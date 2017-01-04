
def main():
    """Entry point for the application script"""
    print("Call your main application code here")


def is_stringset(x):
    ss = set(x)
    return ss

def _is_map(x):
    m = {}
    for key, value in x.items():
        if value:
            if value.keys()[0] == 'S':
                m[key] = value.values()[0]
            if value.keys()[0] == 'N':
                m[key] = int(value.values()[0])
            if value.keys()[0] == 'M':
                m[key] = _is_map()
    return m

def _is_list(x):
    l = []
    for i in x.values()[0]:
        if i.keys()[0] == 'S':
            l.append(i.values()[0])
        elif i.keys()[0] == 'M':
            y = _is_map(i.values()[0])
            l.append(y)
        elif x[1].keys()[0] == 'L':
            y = _is_list(x[1])
            l.append(y)
    return l

def _is_str(x):
    if x[1].keys()[0] == 'S':
        # dic[x[0]] = x[1].values()[0]
        return (x[0], x[1].values()[0])
    elif x[1].keys()[0] == 'N':
        return (x[0], int(x[1].values()[0]))
    elif x[1].keys()[0] == 'M':
        y = _is_map(x[1])
        return(x[0], y)
    elif x[1].keys()[0] == 'L':
        y = _is_list(x[1])
        return(x[0], y)
    elif x[1].keys()[0] == 'SS':
        y = is_stringset(x[1]['SS'])
        return(x[0],y)
    else:
        print('unparsable attribute')
        print(x)
        return False


def parse_json(image):
    dic = {}
    unparsable = False
    for x in image.items():
        tup = _is_str(x)
        if tup:
            dic[tup[0]] = tup[1]
        else:
            unparsable = True
            pass
    if unparsable:
        print('unparsable')
        print(image)
    return dic

def get_new_and_old_images(record):
    images = {}
    images['new'] = parse_json(record['dynamodb']['NewImage'])
    images['old'] = parse_json(record['dynamodb']['OldImage'])
    return images
