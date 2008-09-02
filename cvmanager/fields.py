"""
PT-specific Form helpers
"""

from django.forms import ValidationError
from django.forms.fields import Field, RegexField, Select, EMPTY_VALUES
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _
import re

phone_digits_re = re.compile(r'^(\d{9}|(00|\+)\d*)$')
		
class PTPhoneNumberField(Field):
    """
    Validate local Portuguese phone number (including international ones)
	It should have 9 digits (may include spaces) or start by 00 or + (international)
    """
    default_error_messages = {
        'invalid': u'Phone numbers must have 9 digits, or start by + or 00.',
    }

    def clean(self, value):
        super(PTPhoneNumberField, self).clean(value)
        if value in EMPTY_VALUES:
            return u''
        value = re.sub('(\.|\s)', '', smart_unicode(value))
        m = phone_digits_re.search(value)
        if m:
            return u'%s' % value
        raise ValidationError(self.error_messages['invalid'])