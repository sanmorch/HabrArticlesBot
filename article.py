class Article:
    # attributes
    author = ""
    time_added = ""
    title = ""
    complexity = ""
    minutes_to_read = 0
    #hubs = []
    # description = ""
    url = ""

    # constructor
    def __init__(self
                 , author
                 , time_added
                 , title
                 , complexity
                 , minutes_to_read
                 # , hubs
                 # , description
                 , url):
        self.author = author
        self.time_added = time_added
        self.title = title
        self.complexity = complexity
        self.minutes_to_read = minutes_to_read
        # self.hubs = hubs
        # self.description = description
        self.url = url
