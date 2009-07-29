from django import forms
from django.forms.widgets import flatatt
from django.forms.util import smart_unicode
from django.utils.html import escape
from django.utils.simplejson import JSONEncoder

class JQueryAutoComplete(forms.TextInput):
    def __init__(self, source, options={}, attrs={}):
        """source can be a list containing the autocomplete values or a
        string containing the url used for the XHR request.
        
        For available options see the autocomplete sample page::
        http://jquery.bassistance.de/autocomplete/"""
        
        self.options = None
        self.attrs = {'autocomplete': 'off'}
        self.source = source
        if len(options) > 0:
            self.options = JSONEncoder().encode(options)
        
        self.attrs.update(attrs)
    
    def render_js(self, field_id):
        if isinstance(self.source, list):
            source = JSONEncoder().encode(self.source)
        elif isinstance(self.source, str):
            source = "'%s'" % escape(self.source)
        else:
            raise ValueError('source type is not valid')
        
        options = ''
        if self.options:
            options += ',%s' % self.options

        return u'$(\'#%s\').autocomplete(%s%s);' % (field_id, source, options)

    def render(self, name, value=None, attrs=None):
        final_attrs = self.build_attrs(attrs, name=name)
        if value:
            final_attrs['value'] = escape(smart_unicode(value))

        if not self.attrs.has_key('id'):
            final_attrs['id'] = 'id_%s' % name    
        
        return u'''<input type="text" %(attrs)s/>
        <script type="text/javascript"><!--//
        %(js)s//--></script>
        ''' % {
            'attrs' : flatatt(final_attrs),
            'js' : self.render_js(final_attrs['id']),
        }

# views.py - sample view

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.cache import cache_page
from apps.foo.models import Foo

def autocomplete(request):
    def iter_results(results):
        if results:
            for r in results:
                yield '%s|%s\n' % (r.name, r.id)
    
    if not request.GET.get('q'):
        return HttpResponse(mimetype='text/plain')
    
    q = request.GET.get('q')
    limit = request.GET.get('limit', 15)
    try:
        limit = int(limit)
    except ValueError:
        return HttpResponseBadRequest() 

    foos = Foo.objects.filter(name__startswith=q)[:limit]
    return HttpResponse(iter_results(foos), mimetype='text/plain')

autocomplete = cache_page(autocomplete, 60 * 60)
