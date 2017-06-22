class Meta_section(object):

    def __int__(self, name, entries, comments):

        self.name = name
        self.entries = entries
        self.comments = comments


    def initialize(*args):
        print args
        return Meta_section(name=None, entries=[], comments=[])


class Meta_section_entry():

    def __int__(self, key, value):

        self.key = key
        self.value = value


    def initialize(*args, **kwargs):

        print(args)
        print(kwargs)

        return Meta_section_entry(key=None, value=None)
