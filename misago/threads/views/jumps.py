from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template import RequestContext
from misago.acl.utils import ACLError403, ACLError404
from misago.forums.models import Forum
from misago.readstracker.trackers import ThreadsTracker
from misago.threads.models import Thread, Post
from misago.threads.views.base import BaseView
from misago.views import error403, error404
from misago.utils import make_pagination

class JumpView(BaseView):
    def fetch_thread(self, thread):
        self.thread = Thread.objects.get(pk=thread)
        self.forum = self.thread.forum
        self.request.acl.forums.allow_forum_view(self.forum)
        self.request.acl.threads.allow_thread_view(self.request.user, self.thread)
        
    def redirect(self, post):
        pagination = make_pagination(0, self.request.acl.threads.filter_posts(self.request, self.thread, self.thread.post_set.filter(date__lt=post.date)).count() + 1, self.request.settings.posts_per_page)
        if pagination['total'] > 1:
            return redirect(reverse('thread', kwargs={'thread': self.thread.pk, 'slug': self.thread.slug, 'page': pagination['total']}) + ('#post-%s' % post.pk))
        return redirect(reverse('thread', kwargs={'thread': self.thread.pk, 'slug': self.thread.slug}) + ('#post-%s' % post.pk))
        
    def make_jump(self):
        raise NotImplementedError('JumpView cannot be called directly.')
        
    def __call__(self, request, slug=None, thread=None):
        self.request = request
        try:
            self.fetch_thread(thread)
            return self.make_jump()
        except Thread.DoesNotExist:
            return error404(self.request)
        except ACLError403 as e:
            return error403(request, e.message)
        except ACLError404 as e:
            return error404(request, e.message)
        

class LastReplyView(JumpView):
    def make_jump(self):
        return self.redirect(self.thread.post_set.order_by('-id')[:1][0])


class NewReplyView(JumpView):
    def make_jump(self):
        if not self.request.user.is_authenticated():
            return self.redirect(self.thread.post_set.order_by('-id')[:1][0])
        tracker = ThreadsTracker(self.request.user, self.forum)
        read_date = tracker.get_read_date(self.thread)
        post = self.thread.post_set.filter(date__gt=read_date).order_by('id')[:1]
        if not post:
            return self.redirect(self.thread.post_set.order_by('-id')[:1][0])
        return self.redirect(post[0])


class FirstModeratedView(JumpView):
    def make_jump(self):
        if not self.request.acl.threads.can_approve(self.forum):
            raise ACLError404()
        try:
            return self.redirect(
                self.thread.post_set.get(moderated=True))
        except Post.DoesNotExist:
            return error404(self.request)


class FirstReportedView(JumpView):
    def make_jump(self):
        if not self.request.acl.threads.can_mod_posts(self.forum):
            raise ACLError404()
        try:
            return self.redirect(
                self.thread.post_set.get(reported=True))
        except Post.DoesNotExist:
            return error404(self.request)