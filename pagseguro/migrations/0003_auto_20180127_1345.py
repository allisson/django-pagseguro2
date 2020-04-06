from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagseguro', '0002_auto_20150506_0220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkout',
            name='date',
            field=models.DateTimeField(verbose_name='Data', help_text='Data em que o checkout foi realizado.'),
        ),
        migrations.AlterField(
            model_name='checkout',
            name='message',
            field=models.TextField(verbose_name='Mensagem de erro', blank=True, help_text='Mensagem apresentada no caso de erro no checkout.'),
        ),
        migrations.AlterField(
            model_name='transactionhistory',
            name='date',
            field=models.DateTimeField(verbose_name='Data'),
        ),
    ]
