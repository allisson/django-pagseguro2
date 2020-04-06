from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagseguro', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkout',
            name='code',
            field=models.CharField(help_text='C\xf3digo gerado para redirecionamento.', max_length=100, verbose_name='c\xf3digo', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='checkout',
            name='success',
            field=models.BooleanField(default=False, help_text='O checkout foi feito com sucesso?', db_index=True, verbose_name='Sucesso'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='code',
            field=models.CharField(help_text='O c\xf3digo da transa\xe7\xe3o.', unique=True, max_length=100, verbose_name='c\xf3digo', db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='content',
            field=models.TextField(help_text='Transa\xe7\xe3o no formato json.', verbose_name='Transa\xe7\xe3o'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateTimeField(help_text='Data em que a transa\xe7\xe3o foi criada.', verbose_name='Data'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='last_event_date',
            field=models.DateTimeField(help_text='Data da \xfaltima altera\xe7\xe3o na transa\xe7\xe3o.', verbose_name='\xdaltima altera\xe7\xe3o'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='reference',
            field=models.CharField(help_text='A refer\xeancia passada na transa\xe7\xe3o.', max_length=200, verbose_name='refer\xeancia', db_index=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.CharField(help_text='Status atual da transa\xe7\xe3o.', max_length=20, verbose_name='Status', db_index=True, choices=[('aguardando', 'Aguardando'), ('em_analise', 'Em an\xe1lise'), ('pago', 'Pago'), ('disponivel', 'Dispon\xedvel'), ('em_disputa', 'Em disputa'), ('devolvido', 'Devolvido'), ('cancelado', 'Cancelado')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transactionhistory',
            name='status',
            field=models.CharField(help_text='Status da transa\xe7\xe3o.', max_length=20, verbose_name='Status', choices=[('aguardando', 'Aguardando'), ('em_analise', 'Em an\xe1lise'), ('pago', 'Pago'), ('disponivel', 'Dispon\xedvel'), ('em_disputa', 'Em disputa'), ('devolvido', 'Devolvido'), ('cancelado', 'Cancelado')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transactionhistory',
            name='transaction',
            field=models.ForeignKey(verbose_name='Transa\xe7\xe3o', to='pagseguro.Transaction', on_delete=models.CASCADE),
            preserve_default=True,
        ),
    ]
