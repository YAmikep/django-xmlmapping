# Django
from django.db import models


class ModelDoesNotExist(Exception):
    pass


class ModelFactory(object):
    """Factory to create an object given a Model name."""

    # Cache of the Models to not look for them every time it is needed.
    models_factory = {}

    @classmethod
    def get_model_class(cls, app_model):
        """Gets the Model matching the given app_model (app_label.model_name).

        Returns:
            The Model class.

        Raises:
            A ModelDoesNotExist if it cannot find the Model.
        """
        if app_model in cls.models_factory:
            return cls.models_factory[app_model]

        m_class = None
        try:
            m_class = models.get_model(*app_model.split('.'))
        except:
            pass

        if m_class is None:
            raise ModelDoesNotExist('Cannot found the model %s. It must be defined by app_label.model_name' % (app_model,))

        cls.models_factory[app_model] = m_class
        return m_class


    @classmethod
    def create(cls, app_model, **kwargs):
        """Creates an instance of the Model matching the given app_model (app_label.model_name) with its parameters.

        Returns:
            An object. The returned object has not been saved in the DB yet. It is up to you to do so.

        Raises:
            A ModelDoesNotExist if it cannot find the Model.
        """
        return cls.get_model_class(app_model)(**kwargs)
