import django.db.models

import streetsport.models
import users.models

__all__ = []


def delete_or_set_next_lead(collector, field, sub_objs, using):
    delete = []
    user_ids = (user.id for user in collector.data[users.models.User])
    teams = sub_objs.prefetch_related(
        django.db.models.Prefetch(
            streetsport.models.Team.teammates.field.name,
            queryset=users.models.User.objects.only(
                users.models.User.id.field.name,
            ),
        ),
    ).annotate(
        count_teammates=django.db.models.Count(
            streetsport.models.Team.teammates.field.name,
            filter=~django.db.models.Q(
                django.db.models.Q(
                    teammates__id=django.db.models.F(
                        streetsport.models.Team.lead.field.name,
                    )
                )
                | django.db.models.Q(
                    teammates__id__in=user_ids,
                )
            ),
        )
    )
    for team in teams:
        if not team.count_teammates:
            delete.append(team)
        else:
            team.lead = team.teammates.filter(
                ~django.db.models.Q(id=team.lead.id)
            ).first()
            team.save()

    return django.db.models.CASCADE(collector, field, delete, using)
