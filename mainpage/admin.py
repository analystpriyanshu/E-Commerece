from django.contrib import admin
admin.site.site_header="The hut printing"
admin.site.site_title="The hut printing"
admin.site.index_title="The hut printing"
from mainpage.models import Category,Product,Product_type,ExtendedUser,order
# Register your models here.
admin.site.register(Category),
admin.site.register(Product),
admin.site.register(Product_type),
admin.site.register(ExtendedUser),
admin.site.register(order),

