import random
import string
from django.template import Context, loader, Library
from django.contrib.comments.models import Comment
from django.contrib.contenttypes.models import ContentType

from annotatetext.models import Annotation
register = Library()

@register.inclusion_tag('auxiliary/_bar.html')
def bar(weight, bar_class, norm_factor=1.2, baseline=0, id=""):
    """ Draws a bar.
        weight - translates to bar length
        bar_class - class attribute of the bar element, used for css capture
    """
    if not weight:
        weight = 0
    weight=abs(weight)
    if norm_factor:
        width = round((weight-baseline)/norm_factor,1)
    else:
        width = 0
    
    if not id:
        bar_id = ''.join(random.sample(string.ascii_uppercase + string.digits,5))
    else:
        bar_id = id
    return {'width': width, 'bar_class':bar_class, "bar_id":bar_id}

@register.simple_tag
def object_stamp(obj):
    obj_type = ContentType.objects.get_for_model(obj)
    if obj_type == ContentType.objects.get_for_model(Annotation):
        t = loader.get_template('annotatetext/_stamp.html')
        r = t.render(Context({'annotation': obj}))
    elif obj_type == ContentType.objects.get_for_model(Comment):
        t = loader.get_template('comments/_stamp.html')
        previous_comments = Comment.objects.filter(object_pk=obj.object_pk,
                                 content_type=obj.content_type,
                                 submit_date__lt=obj.submit_date)
        r = t.render(Context({'comment': obj, 'previous_comments': previous_comments}))
    else:
        t = loader.get_template('auxiliary/default_object_stamp.html')
        r = t.render(Context({'object': obj}))
    return r

