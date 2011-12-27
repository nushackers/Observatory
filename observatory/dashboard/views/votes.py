from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.contrib.auth.decorators import login_required

from voting.models import Vote
from dashboard.models import Contributor

VOTE_DIRECTIONS = (('up', 1), ('down', -1), ('clear', 0))

"""Views in this file are duplicated from Voting.views and then modified
for adding karma to Users
"""

def xmlhttprequest_vote_on_object(request, model, direction,
    object_id=None, slug=None, slug_field=None):
    """
    Generic object vote function for use via XMLHttpRequest.
    Duplicated from voting.views

    Properties of the resulting JSON object:
        success
            ``true`` if the vote was successfully processed, ``false``
            otherwise.
        score
            The object's updated score and number of votes if the vote
            was successfully processed.
        error_message
            Contains an error message if the vote was not successfully
            processed.
    """
    if request.method == 'GET':
        return json_error_response(
            'XMLHttpRequest votes can only be made using POST.')
    if not request.user.is_authenticated():
        return json_error_response('Not authenticated.')

    try:
        vote = dict(VOTE_DIRECTIONS)[direction]
    except KeyError:
        return json_error_response(
            '\'%s\' is not a valid vote type.' % direction)

    # Look up the object to be voted on
    lookup_kwargs = {}
    if object_id:
        lookup_kwargs['%s__exact' % model._meta.pk.name] = object_id
    elif slug and slug_field:
        lookup_kwargs['%s__exact' % slug_field] = slug
    else:
        return json_error_response('Generic XMLHttpRequest vote view must be '
                                   'called with either object_id or slug and '
                                   'slug_field.')
    try:
        obj = model._default_manager.get(**lookup_kwargs)
    except ObjectDoesNotExist:
        return json_error_response(
            'No %s found for %s.' % (model._meta.verbose_name, lookup_kwargs))

    try:
        userid = obj.user_id
        contributor = Contributor.objects.get(id = userid)
        contributor.karma = contributor.karma + vote
        contributor.save()
    except: # needto: make this more specific
        pass

    # Vote and respond
    Vote.objects.record_vote(obj, request.user, vote)
    return HttpResponse(simplejson.dumps({
        'success': True,
        'score': Vote.objects.get_score(obj),
    }))

def json_error_response(error_message):
    return HttpResponse(simplejson.dumps(dict(success=False,
                                              error_message=error_message)))