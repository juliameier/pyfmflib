class Meta_section(object):

    def __init__(self,name):
        self.name = name
        self.entries = []
        self.comments = []

    def initialize(*args):
        print args
        return Meta_section(name=None, entries=[], comments=[])


class Meta_section_entry:

    def __init__(self, key, value):

        self.key = key
        self.value = value


    def initialize(*args, **kwargs):

        print(args)
        print(kwargs)

        return Meta_section_entry(key=None, value=None)
