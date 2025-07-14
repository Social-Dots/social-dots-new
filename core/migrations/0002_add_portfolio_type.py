from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='portfolio_type',
            field=models.CharField(
                choices=[('website', 'Website Portfolio'), ('ai', 'AI Automation'), ('social', 'Social Media Content'), ('other', 'Other')],
                default='other',
                max_length=20
            ),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='portfolio_type',
            field=models.CharField(
                choices=[('website', 'Website Portfolio'), ('ai', 'AI Automation'), ('social', 'Social Media Content'), ('other', 'Other')],
                default='other',
                max_length=20
            ),
        ),
    ]