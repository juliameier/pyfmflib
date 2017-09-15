class Meta_section(object):

    def __init__(self,name):
        self.name = name
        self.entries = []
        self.comments = []

    def initialize(*args):
        print args
        return Meta_section(name=None, entries=[], comments=[])

    def add_entry(self, key, value):

        for item in self.entries:
            if item.key == key:
                raise Exception('Key already exists')


        entry = Meta_section_entry(key, value)

        self.entries.append(entry)

        print len(self.entries)

        return entry

    def get_entry(self, key):
        print('key is:' , key)

        if key is not None:
            if self.entries is not None:
                for entry in self.entries:
                    if entry.key == key:
                        print ('key found')
                        return entry

                    else:
                        raise Exception('Key does not exist')

        else:
            if self.entries is not None:
                if len(self.entries) == 0:
                    raise Exception('No entries exist')


class Meta_section_entry:

    def __init__(self, key, value):

        self.key = key
        self.value = value


    def initialize(*args, **kwargs):

        print(args)
        print(kwargs)

        return Meta_section_entry(key=None, value=None)
