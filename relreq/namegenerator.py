import re


def auto_gen_name(name):
    init_name = re.search('[a-z][^A-Z]*', name)
    splitstring = [init_name.group(0)]
    splitstring.extend(re.findall('[A-Z][^A-Z]*', name))
    splitstring[0] = splitstring[0].title()
    joinstring = " ".join(splitstring)
    return joinstring
