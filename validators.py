from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ImproperlyConfigured
import math

#! and if is multiple?

#class FileExtensionValidator(allowed_mimes, message, code)

#def validate_even(value):
    #if value % 2 != 0:
        #raise ValidationError(
            #_('%(value)s is not an even number'),
            #params={'value': value},
        #)
        

@deconstructible
class MimeValidator:
    '''
    Raise a ValidationError with a code of 'invalid_mime' if the MIME is not found in allowed_mimes. 
    The MIME type is sought in value.content_type (works if value is a UploadFile). 
    The MIME type is compared case-insensitively with allowed_extensions.
    '''
    message = _(
        "MIME type '%(mime)s' is not allowed. "
        "Allowed types are: '%(allowed_mimes)s'."
    )
    code = 'invalid_mime'

    def __init__(self, allowed_mimes=None, message=None, code=None):
        if allowed_mimes is not None:
            allowed_mimes = [allowed_mime.lower() for allowed_mime in allowed_mimes]
        self.allowed_mimes = allowed_mimes
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        # for uploadfile
        print('validator value: ' +str(value))
        mime = value.content_type.lower()
        if self.allowed_mimes is not None and mime not in self.allowed_mimes:
            raise ValidationError(
                self.message,
                code=self.code,
                params={
                    'mime': mime,
                    'allowed_mimes': ', '.join(self.allowed_mimes)
                }
            )

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.allowed_mimes == other.allowed_mimes and
            self.message == other.message and
            self.code == other.code
        )


@deconstructible
class FileSizeValidator:
    '''
    Raise a ValidationError with a code of 'invalid_size' if a file size is above a allowed_size. 
    The size type is sought in value.size (works if value is a UploadFile).
    max_size is in bytes. 
    The display can be altered to other number bases using the argument 
    'base'. 'kB', 'MB', and 'GB' are available. If one of these options 
    are used, the display is always truncated to one decimal place (this
    will produce nonsense if the stting is too high. e.g. '0.1GB but max 
    size is 0.1GB')
    '''
    BASES = {
    'B' : lambda v : v,
    'kB' : lambda v : math.ceil(v / 100)/10,
    'MB' : lambda v : math.ceil(v / 10000) / 10,
    'GB' : lambda v : math.ceil(v / 100000000) /10
    }
    base = 'B'
    message = _(
        "Size %(size)s %(base_mark)s is too large. "
        "Max size is %(max_size)s %(base_mark)s."
    )
    code = 'invalid_size'

    def __init__(self, max_size=None, message=None, code=None, base='B'):
        if not max_size:
                raise ImproperlyConfigured(
                    "'max_size' argument must be stated (in bytes)"
                  )          
        self.max_size = max_size
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
        if base != 'B':
            try:
               self.base = self.BASES[base]
            except KeyError:
                raise ImproperlyConfigured(
                    "Value for 'base' attribute not recognized. Allowed values are '{}'".format(', '.join(self.BASES.keys()))
                  )
            self.base = base
            
    def __call__(self, value):
        print('size validation call value:' + str(value))
        print('size validation base:' + str(self.base))
        # This is mainly for uploadfile
        # ...in bytes
        size = value.size

        if ((self.max_size is not None) and (size > self.max_size)):
            raise ValidationError(
                self.message,
                code=self.code,
                params={
                    'size': self.BASES[self.base](size),
                    'base_mark': self.base,
                    'max_size': self.BASES[self.base](self.max_size)
                }
            )

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.max_size == other.max_size and
            self.message == other.message and
            self.code == other.code
        )
