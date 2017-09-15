class Reference_section(object):

    def __init__(
            self,
            title,
            creator,
            created,
            place,
            contact
    ):

        self.title = title
        self.creator = creator
        self.created = created
        self.place = place
        self.contact = contact


    def initialize(*args):

        # args represents the regular arguments
        # kwargs represents the keyword arguments
        print args

        print len(args)

        if len(args) > 0 and len(args) < 4:
            raise Exception('Number of arguments specified is invalid')

        return Reference_section(title=None, creator=None, created=None, place=None, contact=None)