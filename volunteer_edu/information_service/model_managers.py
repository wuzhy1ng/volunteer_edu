from django.db.models import Manager


class VolunteerManager(Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class StudentManager(Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class SubjectManager(Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class AreaManager(Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)
