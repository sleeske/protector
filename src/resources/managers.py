from django.db.models import Count, F, Func, QuerySet, Value
from django.db.models.expressions import Q

from resources.constants import TYPE_FILE, TYPE_URL


class ProtectedResourceQuerySet(QuerySet):
    def created_by(self, user):
        return self.filter(user=user)

    def urls_only(self):
        return self.filter(resource_type=TYPE_URL)

    def files_only(self):
        return self.filter(resource_type=TYPE_FILE)

    def count_visited_links_and_files(self):
        datetime_to_date_str = Func(
            F("created"), Value("YYYY-MM-DD"), function="to_char"
        )
        count_links = Count(
            "id",
            filter=Q(Q(resource_type=TYPE_URL) & Q(visits__gt=0)),
        )
        count_files = Count(
            "id",
            filter=Q(Q(resource_type=TYPE_FILE) & Q(visits__gt=0)),
        )

        return (
            self.annotate(
                date_created=datetime_to_date_str,
            )
            .values("date_created")
            .annotate(
                links=count_links,
                files=count_files,
            )
        )
