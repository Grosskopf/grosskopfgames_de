from cms.admin.pageadmin import PageAdmin
from cms.models import CMSPlugin
from cms.utils import page_permissions
from django.core.exceptions import PermissionDenied
from django.views.generic import UpdateView

from .forms import UpdateCSSForm


class UpdateCSSFormView(UpdateView):
    form_class = UpdateCSSForm
    model = CMSPlugin

    def get_success_url(self):
        return self.request.GET.get('cms_path')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff or not request.user.has_perm('change_page_permissions'):
            raise PermissionDenied("No permission for editing advanced settings")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        css_key = form.cleaned_data.get('css__key')
        css_value = form.cleaned_data.get('css__value')
        plugin = self.object.get_bound_plugin()
        if hasattr(plugin, 'attributes'):
            style_string = plugin.attributes.get('style')
            style_dict = {}
            if style_string:
                for elem in style_string.split(';'):
                    key = elem.split(':')[0].strip()
                    value = (':'.join(elem.split(':')[1:])).strip()
                    style_dict[key] = value
            style_dict[css_key] = css_value
            style_string = ';'.join([key + ': ' + value for key, value in style_dict.items()])
            plugin.attributes['style'] = style_string
            plugin.save()
        return super().form_valid(form)
