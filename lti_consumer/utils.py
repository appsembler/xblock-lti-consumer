# -*- coding: utf-8 -*-
"""
Make '_' a no-op so we can scrape strings
"""


def _(text):
    """
    :return text
    """
    return text


def get_cohort(course_key, user):
    try:
        from openedx.core.djangoapps.course_groups import cohorts
        from opaque_keys.edx.keys import CourseKey
    except ImportError:
        return None, None

    cohort = cohorts.get_cohort(course_key=CourseKey.from_string(course_key), user=user)
    if cohort.name:
        return unicode(cohort.pk), cohort.name
    else:
        return None, None


def get_team(course_key, user):
    from django.conf import settings
    features = getattr(settings, 'FEATURES', {})

    if not features.get('ENABLE_TEAMS'):
        return None, None

    # No need for handling ImportError, since `ENABLE_TEAMS` is set to True.
    from lms.djangoapps.teams.models import CourseTeamMembership
    from opaque_keys.edx.keys import CourseKey

    try:
        membership = CourseTeamMembership.objects.get(
            user=user,
            team__course_id=CourseKey.from_string(course_key),
        )
    except CourseTeamMembership.DoesNotExist:
        return None, None

    return unicode(membership.team.team_id), membership.team.name
