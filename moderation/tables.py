import django_tables2 as tables
from private.models import PrivateEntry
from public.models import Comment


class ModerateEntriesTable(tables.Table):
    """Table with to_publish entries list"""
    class Meta:
        model = PrivateEntry
        fields = ('song', 'author', 'tuning', 'key', 'capo', 'added', 'added_by')
        attrs = {"class": "table table-striped table-hover "}
        row_attrs = {
            "onClick": lambda record: "document.location.href='/moderate/{0}';".format(record.id)
        }


class ModerateCommentsTable(tables.Table):
    """Table with not moderated comments list"""
    body = tables.TemplateColumn('<data-toggle="tooltip" title="{{record.body}}">{{record.body|truncatechars:100}}', verbose_name='Comment')
    entry = tables.Column(accessor='entry')
    added_date = tables.Column(verbose_name='Added')
    class Meta:
        model = Comment
        fields = ('body', 'entry', 'added_date', 'added_by')
        attrs = {"class": "table table-striped table-hover"}
        row_attrs = {
            "onClick": lambda record: "document.location.href='/moderate/comments/{0}';".format(record.id)
        }
