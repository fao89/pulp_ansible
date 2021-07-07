# Generated by Django 2.2.24 on 2021-07-07 17:46

from django.db import migrations, models, transaction
import django.db.models.deletion


def migrate_data_from_old_model_to_new_model_up(apps, schema_editor):
    """ Move objects from AnsibleCollectionDeprecated to NewAnsibleCollectionDeprecated."""
    AnsibleCollectionDeprecated = apps.get_model('ansible', 'AnsibleCollectionDeprecated')
    NewAnsibleCollectionDeprecated = apps.get_model('ansible', 'NewAnsibleCollectionDeprecated')
    RepositoryContent = apps.get_model('core', 'RepositoryContent')
    for deprecated_collection in AnsibleCollectionDeprecated.objects.all():
        with transaction.atomic():
            deprecation = NewAnsibleCollectionDeprecated(
                namespace=deprecated_collection.collection.namespace,
                name=deprecated_collection.collection.name,
            )
            deprecation.save()
            RepositoryContent(
                repository=deprecated_collection.repository_version.repository,
                content_id=deprecation.pk,
                version_added=deprecated_collection.repository_version,
            ).save()
            deprecated_collection.delete()


def migrate_data_from_old_model_to_new_model_down(apps, schema_editor):
    """ Move objects from NewAnsibleCollectionDeprecated to AnsibleCollectionDeprecated."""
    AnsibleCollectionDeprecated = apps.get_model('ansible', 'AnsibleCollectionDeprecated')
    NewAnsibleCollectionDeprecated = apps.get_model('ansible', 'NewAnsibleCollectionDeprecated')
    RepositoryContent = apps.get_model('core', 'RepositoryContent')
    for repo_content in RepositoryContent.objects.all():
        with transaction.atomic():
            AnsibleCollectionDeprecated(
                collection_id=repo_content.content_id,
                repository_version=repo_content.version_added,
            ).save()
            repo_content.delete()
    NewAnsibleCollectionDeprecated.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0068_add_timestamp_of_interest'),
        ('ansible', '0033_swap_distribution_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewAnsibleCollectionDeprecated',
            fields=[
                ('content_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='ansible_ansiblecollectiondeprecated', serialize=False, to='core.Content')),
                ('namespace', models.CharField(editable=False, max_length=64)),
                ('name', models.CharField(editable=False, max_length=64)),
            ],
            options={
                'default_related_name': '%(app_label)s_%(model_name)s',
                'unique_together': {('namespace', 'name')},
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
