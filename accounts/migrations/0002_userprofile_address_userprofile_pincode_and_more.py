from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_external_url_product_seller_name'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='address',
            field=models.CharField(blank=True, max_length=260),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='pincode',
            field=models.CharField(blank=True, max_length=12),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='wishlist',
            field=models.ManyToManyField(blank=True, related_name='wishlisted_by', to='products.product'),
        ),
    ]
