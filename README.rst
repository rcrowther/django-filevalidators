Django file validators
=======================
A module, but barely anything at all. You probably want it.

These are server-side protections (you could use Javascript too, but that's another story). Be nice, see what the user is giving you, then reply. Django has functionality to do this. 

 
Limitations
-----------
Both validators will only deal with a single file (like Django's FileField).

Not to do with the module, but bear in mind that file validators are limited protection against determined attacks on upload mechanisms. File extensions do not always have much bearing on how an OS communicates with a server (but if they do, a validation will limit some kinds of attack). MIME types are not carried in the file, a server/OS guesses them (though if Django guesses the same as the server, this is some protection). If a server is not throttled, it will go down under heavy uploads (but at least Django will not be participating) etc.
 
 
Alternatives
------------
This code has probably been written 50 times before, and better. Somewhere.


Installation/dependencies
--------------------------
Download into your environment, rename the top folder by removing the 'django-' prefix.

No dependencies. No Django installation. It's a module of code.


Use of FileValidators
---------------------

File extension validation
~~~~~~~~~~~~~~~~~~~~~~~~~
If you want a FileExtensionValidator, Django has one already. 

For a non-model form, add directly to the field. The extension validator lowercases input, so no need for huge lists, ::

    from django.core.validators import FileExtensionValidator

    class MyForm(forms.Form):
        file = forms.FileField(validators=[
            FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])
            ])
    
For a ModelForm, override __init__() ::

    from django.core.validators import FileExtensionValidator

    class FileForm(ModelForm):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)     
            self.fields["file"].validators.extend([
                FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])
            ])
    
        class Meta:
             model = File
             fields = ['name', 'file', 'description', 'author']


File MIME validation
~~~~~~~~~~~~~~~~~~~~
This one is ours. It also lowercases input e.g. ::

    from filevalidators.validators import MimeValidator

    class FileForm(ModelForm):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)     
            self.fields["file"].validators.extend([
                MimeValidator(allowed_extensions=['text/plain', 'text/richtext'])
            ])
    
        class Meta:
             model = File
             fields = ['name', 'file', 'description', 'author']


File MIME validation
~~~~~~~~~~~~~~~~~~~~
This is ours too. 'max_size' is in bytes. 'base' changes the message to a user, 'B' reports in bytes (the default), 'kB' in kilobytes, MB in megabytes, GB in gigabytes. Reports are to one point of precision  e.g. ::

    from filevalidators.validators import FileSizeValidator

    class FileForm(ModelForm):
    
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)     
            self.fields["file"].validators.extend([
                FileSizeValidator(max_size=80000, base='kB')
            ])
            
        class Meta:
             model = File
             fields = ['name', 'file', 'description', 'author']
