from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(help_text=b'C\xc3\xb3digo gerado para redirecionamento.', max_length=100, verbose_name=b'c\xc3\xb3digo', blank=True)),
                ('date', models.DateTimeField(help_text=b'Data em que o checkout foi realizado.', verbose_name=b'Data')),
                ('success', models.BooleanField(help_text=b'O checkout foi feito com sucesso?', db_index=True, verbose_name=b'Sucesso')),
                ('message', models.TextField(help_text=b'Mensagem apresentada no caso de erro no checkout.', verbose_name=b'Mensagem de erro', blank=True)),
            ],
            options={
                'ordering': ['-date'],
                'verbose_name': 'Checkout',
                'verbose_name_plural': 'Checkouts',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(help_text=b'O c\xc3\xb3digo da transa\xc3\xa7\xc3\xa3o.', unique=True, max_length=100, verbose_name=b'c\xc3\xb3digo', db_index=True)),
                ('reference', models.CharField(help_text=b'A refer\xc3\xaancia passada na transa\xc3\xa7\xc3\xa3o.', max_length=200, verbose_name=b'refer\xc3\xaancia', db_index=True, blank=True)),
                ('status', models.CharField(help_text=b'Status atual da transa\xc3\xa7\xc3\xa3o.', max_length=20, verbose_name=b'Status', db_index=True, choices=[(b'aguardando', b'Aguardando'), (b'em_analise', b'Em an\xc3\xa1lise'), (b'pago', b'Pago'), (b'disponivel', b'Dispon\xc3\xadvel'), (b'em_disputa', b'Em disputa'), (b'devolvido', b'Devolvido'), (b'cancelado', b'Cancelado')])),
                ('date', models.DateTimeField(help_text=b'Data em que a transa\xc3\xa7\xc3\xa3o foi criada.', verbose_name=b'Data')),
                ('last_event_date', models.DateTimeField(help_text=b'Data da \xc3\xbaltima altera\xc3\xa7\xc3\xa3o na transa\xc3\xa7\xc3\xa3o.', verbose_name=b'\xc3\x9altima altera\xc3\xa7\xc3\xa3o')),
                ('content', models.TextField(help_text=b'Transa\xc3\xa7\xc3\xa3o no formato json.', verbose_name=b'Transa\xc3\xa7\xc3\xa3o')),
            ],
            options={
                'ordering': ['-date'],
                'verbose_name': 'Transa\xe7\xe3o',
                'verbose_name_plural': 'Transa\xe7\xf5es',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TransactionHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(help_text=b'Status da transa\xc3\xa7\xc3\xa3o.', max_length=20, verbose_name=b'Status', choices=[(b'aguardando', b'Aguardando'), (b'em_analise', b'Em an\xc3\xa1lise'), (b'pago', b'Pago'), (b'disponivel', b'Dispon\xc3\xadvel'), (b'em_disputa', b'Em disputa'), (b'devolvido', b'Devolvido'), (b'cancelado', b'Cancelado')])),
                ('date', models.DateTimeField(verbose_name=b'Data')),
                ('transaction', models.ForeignKey(verbose_name=b'Transa\xc3\xa7\xc3\xa3o', to='pagseguro.Transaction', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ['date'],
                'verbose_name': 'Hist\xf3rico da transa\xe7\xe3o',
                'verbose_name_plural': 'Hist\xf3ricos de transa\xe7\xf5es',
            },
            bases=(models.Model,),
        ),
    ]
