class BmsException(Exception):
    def __init__(self, section, cause):
        super().__init__(
            f"Something went wrong during the exchange with the battery at {section} because {cause}"
        )
        self.section = section
        self.cause = cause
