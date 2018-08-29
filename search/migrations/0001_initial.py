# Generated by Django 2.1 on 2018-08-29 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PopulationAttempt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('began', models.DateTimeField(help_text='When the load attempt began.', null=True)),
                ('finished', models.DateTimeField(help_text='When the load attempt finished.', null=True)),
                ('succeeded', models.NullBooleanField(default=None, help_text='Whether the load attempt succeeded.', verbose_name=' ')),
                ('reason', models.CharField(help_text='The reason for a failure.', max_length=250, null=True)),
                ('updatecalaccess_began', models.DateTimeField(help_text='When `updatecalaccess` command began.', null=True)),
                ('updatecalaccess_finished', models.DateTimeField(help_text='When `updatecalaccess` command finished.', null=True)),
                ('updatecalaccess_succeeded', models.NullBooleanField(default=None, help_text='Whether `updatecalaccess` command succeeded.', verbose_name=' ')),
                ('loadactivities_began', models.DateTimeField(help_text='When `loadactivities` command began.', null=True)),
                ('loadactivities_finished', models.DateTimeField(help_text='When `loadactivities` command finished.', null=True)),
                ('loadactivities_succeeded', models.NullBooleanField(default=None, help_text='Whether `loadactivities` command succeeded.', verbose_name=' ')),
                ('loadactivities_count', models.IntegerField(help_text='Count of activities loaded.', null=True, verbose_name='Acts Loaded')),
                ('loadbills_began', models.DateTimeField(help_text='When `loadbills` command began.', null=True)),
                ('loadbills_finished', models.DateTimeField(help_text='When `loadbills` command finished.', null=True)),
                ('loadbills_succeeded', models.NullBooleanField(default=None, help_text='Whether `loadbills` command succeeded.', verbose_name=' ')),
                ('loadbills_count', models.IntegerField(help_text='Count of bills loaded.', null=True, verbose_name='Bills Loaded')),
                ('connectbills_began', models.DateTimeField(help_text='When `connectbills` command began.', null=True)),
                ('connectbills_finished', models.DateTimeField(help_text='When `connectbills` command finished.', null=True)),
                ('connectbills_succeeded', models.NullBooleanField(default=None, help_text='Whether `connectbills` command succeeded.', verbose_name=' ')),
                ('connectedbills_count', models.IntegerField(help_text='Count of bills connected.', null=True, verbose_name='Bills Connected')),
                ('connectedacts_count', models.IntegerField(help_text='Count of acts connected.', null=True, verbose_name='Acts Connected')),
            ],
            options={
                'ordering': ('-began', '-finished'),
                'get_latest_by': 'began',
            },
        ),
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('activities', 'Lobby Activities'), ('registrations', 'Lobby Registrations')], max_length=20)),
                ('company', models.CharField(blank=True, max_length=250, null=True)),
                ('interest', models.CharField(blank=True, max_length=250, null=True)),
                ('bill', models.CharField(blank=True, max_length=250, null=True)),
                ('start', models.CharField(blank=True, max_length=50, null=True)),
                ('end', models.CharField(blank=True, max_length=50, null=True)),
                ('session', models.CharField(blank=True, max_length=10, null=True)),
                ('latest_only', models.BooleanField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Searches',
                'ordering': ('-created',),
                'get_latest_by': 'created',
            },
        ),
    ]
