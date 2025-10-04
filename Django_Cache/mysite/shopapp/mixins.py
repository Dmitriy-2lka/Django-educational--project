from django.contrib.auth.mixins import UserPassesTestMixin

class OwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return (self.request.user.is_superuser or getattr(obj, 'created_by', None) == self.request.user)