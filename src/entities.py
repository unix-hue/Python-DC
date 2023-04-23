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

    def __init__():
        pass

    def set_value():
        pass

    def print_report():
        pass