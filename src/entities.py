class Metadata:

    def __init__(self):
        self._time_analysis = None
        self._user_analysis = None
        self._os_analysis = None
        self._dc_version = None
        self._dc_name = None

    def print_report(self):
        pass

class Project:

    def __init__(self):
        self.name = None
        self.version = None
        self.description = None
        self.authors = None
        self.license = None

    def print_report(self):
        print(self.name, self.version, self.description, self.authors, self.license)

class Dependency:

    def __init__(self):
        self.installer = None
        
        self.name = None
        self.version = None
        self.summary = None
        self.homepage = None
        self.author = None
        self.author_email = None
        self.license = None
        self.platform = None
        self.requires_python = None
        self.requires_dist = None

    def print_report(self):
        pass