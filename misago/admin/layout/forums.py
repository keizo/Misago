from django.conf.urls import patterns, include, url
from django.utils.translation import ugettext_lazy as _
from misago.admin import AdminAction
from misago.forums.models import Forum

ADMIN_ACTIONS=(
   AdminAction(
               section='forums',
               id='forums',
               name=_("Forums List"),
               help=_("Create, edit and delete forums."),
               icon='comment',
               model=Forum,
               actions=[
                        {
                         'id': 'list',
                         'name': _("Forums List"),
                         'help': _("All existing forums"),
                         'route': 'admin_forums'
                         },
                        {
                         'id': 'new_category',
                         'name': _("New Category"),
                         'help': _("Create new category"),
                         'route': 'admin_forums_new_category'
                         },
                        {
                         'id': 'new_forum',
                         'name': _("New Forum"),
                         'help': _("Create new forum"),
                         'route': 'admin_forums_new_forum'
                         },
                        {
                         'id': 'new_redirect',
                         'name': _("New Redirect"),
                         'help': _("Create new redirect"),
                         'route': 'admin_forums_new_redirect'
                         },
                        ],
               route='admin_forums',
               urlpatterns=patterns('misago.forums.views',
                        url(r'^$', 'List', name='admin_forums'),
                        url(r'^new/category/$', 'NewCategory', name='admin_forums_new_category'),
                        url(r'^new/forum/$', 'NewForum', name='admin_forums_new_forum'),
                        url(r'^new/redirect/$', 'NewRedirect', name='admin_forums_new_redirect'),
                        url(r'^up/(?P<slug>([a-z0-9]|-)+)-(?P<target>\d+)/$', 'Up', name='admin_forums_up'),
                        url(r'^down/(?P<slug>([a-z0-9]|-)+)-(?P<target>\d+)/$', 'Down', name='admin_forums_down'),
                        url(r'^edit/(?P<slug>([a-z0-9]|-)+)-(?P<target>\d+)/$', 'Edit', name='admin_forums_edit'),
                        url(r'^delete/(?P<slug>([a-z0-9]|-)+)-(?P<target>\d+)/$', 'Delete', name='admin_forums_delete'),
                    ),
               ),
   AdminAction(
               section='forums',
               id='moderators',
               name=_("Moderators"),
               help=_("Assign forums moderators."),
               icon='eye-open',
               route='admin_forums_moderators',
               urlpatterns=patterns('misago.admin.views',
                        url(r'^$', 'todo', name='admin_forums_moderators'),
                    ),
               ),
   AdminAction(
               section='forums',
               id='tests',
               name=_("Tests"),
               help=_("Tests that new messages have to pass"),
               icon='filter',
               route='admin_forums_tests',
               urlpatterns=patterns('misago.admin.views',
                        url(r'^$', 'todo', name='admin_forums_tests'),
                    ),
               ),
   AdminAction(
               section='forums',
               id='badwords',
               name=_("Words Filter"),
               help=_("Forbid usage of words in messages"),
               icon='volume-off',
               route='admin_forums_badwords',
               urlpatterns=patterns('misago.admin.views',
                        url(r'^$', 'todo', name='admin_forums_badwords'),
                    ),
               ),
   AdminAction(
               section='forums',
               id='attachments',
               name=_("Attachments"),
               help=_("Manage allowed attachment types."),
               icon='download-alt',
               route='admin_forums_attachments',
               urlpatterns=patterns('misago.admin.views',
                        url(r'^$', 'todo', name='admin_forums_attachments'),
                    ),
               ),
)