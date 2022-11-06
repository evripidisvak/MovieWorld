from django.contrib import admin
from .models import *


# class ShopAdminView(admin.ModelAdmin):
#     list_display = ("name", "key_account", "seller_last_name")
#     list_filter = [
#         "key_account",
#         ("seller", admin.RelatedOnlyFieldListFilter),
#         ("seller", admin.EmptyFieldListFilter),
#     ]
#     search_fields = ["name"]

#     def seller_last_name(self, obj):
#         if obj.seller:
#             return obj.seller.last_name
#         else:
#             # return None # or
#             return "Δεν υπάρχει"


@admin.register(Opinion)
class OpinionAdmin(admin.ModelAdmin):
    list_display = ("movie", "user", "like")


admin.site.register(Movie)
# admin.site.register(Opinion)
