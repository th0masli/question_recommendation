
from django.conf import settings


class db_router(object):
    """
        A router to control all database operations on models in the
        question application.
        """

    def db_for_read(self, model, **hints):
        """
        Attempts to read question models go to galaxy database.
        """
        if model._meta.app_label == 'galaxy':
            return 'galaxy'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write question models go to galaxy databases.
        """
        if model._meta.app_label == 'galaxy':
            return 'galaxy'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the question app is involved.
        """
        if obj1._meta.label == 'galaxy' or \
                        obj2._meta.label == 'galaxy':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the uploaded images and returned ids only appears in the 'galaxy'
        database.
        """
        if app_label == 'galaxy':
            return db == 'galaxy'
        elif app_label == 'question':
            return False
        return None

    def allow_syncdb(self, db, model):
        if db == 'galaxy' or model._meta.app_label == "galaxy":
            return False  # we're not using syncdb on our hvdb database
        else:  # but all other models/databases are fine
            return True
        return None