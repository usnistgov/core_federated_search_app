""" Instance model
"""
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator
from django.db import models, IntegrityError

from core_main_app.commons import exceptions
from core_main_app.commons.regex import NOT_EMPTY_OR_WHITESPACES


class Instance(models.Model):
    """Represents an instance of a remote project"""

    name = models.CharField(
        blank=False,
        unique=True,
        validators=[
            RegexValidator(
                regex=NOT_EMPTY_OR_WHITESPACES,
                message="Title must not be empty or only whitespaces",
                code="invalid_title",
            ),
        ],
        max_length=200,
    )
    endpoint = models.URLField(blank=False, unique=True)
    access_token = models.CharField(blank=False, max_length=200)
    refresh_token = models.CharField(blank=False, max_length=200)
    expires = models.DateTimeField(blank=False)

    @staticmethod
    def get_all():
        """Return all instances.

        Returns:
            instance collection

        """
        return Instance.objects.all()

    @staticmethod
    def get_by_id(instance_id):
        """Return the object with the given id.

        Args:
            instance_id:

        Returns:
            Instance (obj): Instance object with the given id

        """
        try:
            return Instance.objects.get(pk=str(instance_id))
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    @staticmethod
    def get_by_name(instance_name):
        """Return the object with the given name.

        Args:
            instance_name:

        Returns:
            Instance (obj): Instance object with the given name

        """
        try:
            return Instance.objects.get(name=str(instance_name))
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    @staticmethod
    def get_by_endpoint_starting_with(instance_endpoint):
        """Return the object with the given endpoint.

        Args:
            instance_endpoint:

        Returns:
            Instance (obj): Instance object with the given name

        """
        try:
            return Instance.objects.get(endpoint__startswith=str(instance_endpoint))
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    def save_object(self):
        """Custom save.

        Returns:

        """
        try:
            self.check_instance_name()
            return self.save()
        except IntegrityError:
            raise exceptions.NotUniqueError(
                "Unable to create the new repository: Not Unique"
            )
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    def check_instance_name(self):
        """Test if the name is the name of the local instance.

        Returns:

        """
        if self.name.upper() == settings.CUSTOM_NAME.upper():
            raise exceptions.ModelError(
                f'By default, the instance named "{settings.CUSTOM_NAME}" is the instance currently running.'
            )

    def clean(self):
        """Clean is called before saving

        Returns:

        """
        self.name = self.name.strip()

    def __str__(self):
        """Instance object as string.

        Returns:

        """
        return self.name
