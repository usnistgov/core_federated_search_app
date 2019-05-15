""" Instance model
"""
from django_mongoengine import fields, Document
from mongoengine import errors as mongoengine_errors

from core_main_app.commons import exceptions
from core_main_app.commons.regex import NOT_EMPTY_OR_WHITESPACES


class Instance(Document):
    """ Represents an instance of a remote project
    """
    name = fields.StringField(blank=False, unique=True, regex=NOT_EMPTY_OR_WHITESPACES)
    endpoint = fields.URLField(blank=False, unique=True)
    access_token = fields.StringField(blank=False)
    refresh_token = fields.StringField(blank=False)
    expires = fields.DateTimeField(blank=False)

    @staticmethod
    def get_all():
        """ Return all instances.

        Returns:
            instance collection

        """
        return Instance.objects().all()

    @staticmethod
    def get_by_id(instance_id):
        """ Return the object with the given id.

        Args:
            instance_id:

        Returns:
            Instance (obj): Instance object with the given id

        """
        try:
            return Instance.objects.get(pk=str(instance_id))
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(e.message)
        except Exception as ex:
            raise exceptions.ModelError(ex.message)

    @staticmethod
    def get_by_name(instance_name):
        """ Return the object with the given name.

        Args:
            instance_name:

        Returns:
            Instance (obj): Instance object with the given name

        """
        try:
            return Instance.objects.get(name=str(instance_name))
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(e.message)
        except Exception as ex:
            raise exceptions.ModelError(ex.message)

    @staticmethod
    def get_by_endpoint_starting_with(instance_endpoint):
        """ Return the object with the given endpoint.

        Args:
            instance_endpoint:

        Returns:
            Instance (obj): Instance object with the given name

        """
        try:
            return Instance.objects.get(endpoint__startswith=str(instance_endpoint))
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(e.message)
        except Exception as ex:
            raise exceptions.ModelError(ex.message)

    def save_object(self):
        """ Custom save.

        Returns:

        """
        try:
            self.check_instance_name()
            return self.save()
        except mongoengine_errors.NotUniqueError as e:
            raise exceptions.NotUniqueError("Unable to create the new repository: Not Unique")
        except Exception as ex:
            raise exceptions.ModelError(ex.message)

    def check_instance_name(self):
        """ Test if the name is 'Local'.

        Returns:

        """
        if self.name.upper() == "LOCAL":
            raise exceptions.ModelError("By default, the instance named Local is the instance currently running.")

    def clean(self):
        """ Clean is called before saving

        Returns:

        """
        self.name = self.name.strip()
