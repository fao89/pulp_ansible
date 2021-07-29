# Generated by Django 2.2.24 on 2021-07-07 17:46

from django.db import migrations, models
import django.db.models.deletion


def migrate_data_from_old_model_to_new_model_up(apps, schema_editor):
    """ Move objects from AnsibleCollectionDeprecated to NewAnsibleCollectionDeprecated."""
    AnsibleCollectionDeprecated = apps.get_model('ansible', 'AnsibleCollectionDeprecated')
    NewAnsibleCollectionDeprecated = apps.get_model('ansible', 'NewAnsibleCollectionDeprecated')
    for deprecated_collection in AnsibleCollectionDeprecated.objects.all():
        NewAnsibleCollectionDeprecated(
            namespace=deprecated_collection.collection.namespace,
            name=deprecated_collection.collection.name,
            pulp_type="ansible.collection_deprecation",
            collection_id=deprecated_collection.collection_id,
            repository_id=deprecated_collection.repository_version.repository.pk,
            version_added_id=deprecated_collection.repository_version.pk,
            version_added_number=deprecated_collection.repository_version.number,
        ).save()


def migrate_data_from_old_model_to_new_model_down(apps, schema_editor):
    """ Move objects from NewAnsibleCollectionDeprecated to AnsibleCollectionDeprecated."""
    AnsibleCollectionDeprecated = apps.get_model('ansible', 'AnsibleCollectionDeprecated')
    NewAnsibleCollectionDeprecated = apps.get_model('ansible', 'NewAnsibleCollectionDeprecated')
    RepositoryVersionContentDetails = apps.get_model('core', 'RepositoryVersionContentDetails')
    for deprecation in NewAnsibleCollectionDeprecated.objects.all():
        AnsibleCollectionDeprecated(
            collection_id=deprecation.collection_id,
            repository_version_id=deprecation.version_added_id,
        ).save()
        deprecation.version_memberships.all().delete()
    RepositoryVersionContentDetails.objects.filter(content_type=deprecation.pulp_type).delete()

def delete_deprecation_type(apps, schema_editor):
    """ Delete deprecation content type."""
    Content = apps.get_model('core', 'Content')
    Content.objects.filter(pulp_type="ansible.collection_deprecation").delete()

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0068_add_timestamp_of_interest'),
        ('ansible', '0034_handle_jsonfield_warnings'),
    ]

    operations = [
        migrations.RunPython(
            code=migrations.RunPython.noop,
            reverse_code=delete_deprecation_type,
        ),
        migrations.CreateModel(
            name='NewAnsibleCollectionDeprecated',
            fields=[
                ('content_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='ansible_ansiblecollectiondeprecated', serialize=False, to='core.Content')),
                ('namespace', models.CharField(editable=False, max_length=64)),
                ('name', models.CharField(editable=False, max_length=64)),
                ('collection_id',  models.UUIDField(editable=False, primary_key=False, serialize=False, null=True)),
                ('repository_id',  models.UUIDField(editable=False, primary_key=False, serialize=False, null=True)),
                ('version_added_id',  models.UUIDField(editable=False, primary_key=False, serialize=False, null=True)),
                ('version_added_number',  models.IntegerField(default=0)),
            ],
            options={
                'default_related_name': '%(app_label)s_%(model_name)s',
            },
            bases=('core.content',),
        ),
        migrations.RunPython(
            code=migrate_data_from_old_model_to_new_model_up,
            reverse_code=migrate_data_from_old_model_to_new_model_down,
        ),
        migrations.DeleteModel(
            name='AnsibleCollectionDeprecated',
        ),
        migrations.RenameModel(
            old_name='NewAnsibleCollectionDeprecated',
            new_name='AnsibleCollectionDeprecated',
        ),
    ]
