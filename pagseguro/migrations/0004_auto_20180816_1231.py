# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pagseguro', '0003_auto_20180127_1345'),
    ]

    operations = [
        migrations.CreateModel(
            name='PreApproval',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(db_index=True, help_text='O c\xf3digo da transa\xe7\xe3o.', max_length=100, unique=True, verbose_name='c\xf3digo')),
                ('tracker', models.CharField(db_index=True, help_text='C\xf3digo identificador p\xfablico.', max_length=100, unique=True, verbose_name='identificador p\xfablico')),
                ('reference', models.CharField(blank=True, db_index=True, help_text='A refer\xeancia passada na transa\xe7\xe3o.', max_length=200, verbose_name='refer\xeancia')),
                ('status', models.CharField(choices=[('PENDING', 'Aguardando processamento do pagamento'), ('ACTIVE', 'Ativa'), ('CANCELLED', 'Cancelada'), ('CANCELLED_BY_RECEIVER', 'Cancelada pelo Vendedor'), ('CANCELLED_BY_SENDER', 'Cancelada pelo Comprador'), ('EXPIRED', 'Expirada')], db_index=True, help_text='Status atual da transa\xe7\xe3o.', max_length=20, verbose_name='Status')),
                ('date', models.DateTimeField(help_text='Data em que a transa\xe7\xe3o foi criada.', verbose_name='Data')),
                ('last_event_date', models.DateTimeField(help_text='Data da \xfaltima altera\xe7\xe3o na transa\xe7\xe3o.', verbose_name='\xdaltima altera\xe7\xe3o')),
                ('content', models.TextField(help_text='Transa\xe7\xe3o no formato json.', verbose_name='Transa\xe7\xe3o')),
            ],
            options={
                'ordering': ['-date'],
                'verbose_name': 'Assinatura: Transa\xe7\xe3o',
                'verbose_name_plural': 'Assinaturas: Transa\xe7\xf5es',
            },
        ),
        migrations.CreateModel(
            name='PreApprovalHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PENDING', 'Aguardando processamento do pagamento'), ('ACTIVE', 'Ativa'), ('CANCELLED', 'Cancelada'), ('CANCELLED_BY_RECEIVER', 'Cancelada pelo Vendedor'), ('CANCELLED_BY_SENDER', 'Cancelada pelo Comprador'), ('EXPIRED', 'Expirada')], help_text='Status da transa\xe7\xe3o.', max_length=20, verbose_name='Status')),
                ('date', models.DateTimeField(verbose_name='Data')),
                ('pre_approval', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pagseguro.PreApproval', verbose_name='Transa\xe7\xe3o')),
            ],
            options={
                'ordering': ['date'],
                'verbose_name': 'Assinatura: Hist\xf3rico da transa\xe7\xe3o',
                'verbose_name_plural': 'Assinaturas: Hist\xf3ricos de transa\xe7\xf5es',
            },
        ),
        migrations.CreateModel(
            name='PreApprovalPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('charge', models.CharField(choices=[('auto', 'Autom\xe1tica'), ('manual', 'Manual')], db_index=True, help_text='Indica se a assinatura ser\xe1 gerenciada pelo PagSeguro (autom\xe1tica) ou pelo Vendedor (manual)', max_length=20, verbose_name='Cobran\xe7a')),
                ('name', models.CharField(db_index=True, help_text='Nome/Identificador da assinatura', max_length=100, unique=True, verbose_name='Nome')),
                ('details', models.TextField(blank=True, help_text='Detalhes/Descri\xe7\xe3o da assinatura', max_length=255, verbose_name='Detalhes')),
                ('amount_per_payment', models.DecimalField(blank=True, decimal_places=2, help_text='Valor exato de cada cobran\xe7a', max_digits=9, null=True, verbose_name='Valor da cobran\xe7a')),
                ('max_amount_per_payment', models.DecimalField(blank=True, decimal_places=2, help_text='Valor m\xe1ximo de cada cobran\xe7a', max_digits=9, null=True, verbose_name='Valor m\xe1ximo de cada cobran\xe7a')),
                ('period', models.CharField(choices=[('WEEKLY', 'Semanal'), ('MONTHLY', 'Mensal'), ('BIMONTHLY', '2 vezes ao m\xeas'), ('TRIMONTHLY', '3 vezes por m\xeas'), ('SEMIANNUALLY', 'A cada 6 meses'), ('YEARLY', 'Anualmente')], db_index=True, help_text='Periodicidade da cobran\xe7a', max_length=20, verbose_name='Periodicidade')),
                ('final_date', models.DateTimeField(blank=True, db_index=True, help_text='Fim da vig\xeancia da assinatura', null=True, verbose_name='Data Final')),
                ('max_total_amount', models.DecimalField(blank=True, decimal_places=2, help_text='Valor m\xe1ximo de cada cobran\xe7a', max_digits=9, null=True, verbose_name='Valor m\xe1ximo de cada cobran\xe7a')),
                ('reference', models.CharField(blank=True, db_index=True, help_text='A refer\xeancia passada na transa\xe7\xe3o.', max_length=200, null=True, verbose_name='Refer\xeancia')),
                ('redirect_code', models.CharField(blank=True, help_text='C\xf3digo gerado para redirecionamento.', max_length=100, null=True, verbose_name='c\xf3digo')),
            ],
            options={
                'verbose_name': 'Assinatura: Plano',
                'verbose_name_plural': 'Assinaturas: Planos',
            },
        ),
        migrations.AddField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('1', 'Pagamento'), ('11', 'Recorr\xeancia')], db_index=True, default='1', help_text='Representa o tipo da transa\xe7\xe3o recebida.', max_length=2, verbose_name='tipo'),
        ),
    ]
