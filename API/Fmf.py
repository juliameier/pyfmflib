from API import Reference_section, Table, Meta_section

class FMF(object):

    def __init__(self, header, meta_sections, tables, global_comments, compliance_level):

        self.header = header
        self.meta_sections = meta_sections
        self.table_sections = tables
        self.global_comments = global_comments
        self.compliance_level = compliance_level


    def initialize(*args, **kwargs):

        # args represents the regular arguments
        # kwargs represents the keyword arguments
        print args, kwargs
        print (len(args))
        print (len(kwargs))

        return FMF(header=None, meta_sections=[], tables=[], global_comments=[], compliance_level=None)


    def set_reference(title, creator, place, created, contact):

        return Reference_section.create_reference_section(title, creator, created, place, contact)


    def add_table(name, symbol):

        return Table.create_table_object('Name', 'Symbol')

    def add_meta_section(name):

        return Meta_section.initialize('Name')