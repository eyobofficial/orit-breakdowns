from django.contrib import admin
from .models import (Company,
                     PackageType,
                     Package,
                     CompanyMembership,
                     UserMembership,
                     UserPayment,
                     CompanyPayment,
                     City,
                     ProjectCatagory, 
                     Project,
                     UnitCatagory, 
                     Unit, 
                     MaterialCatagory, 
                     Material, 
                     MaterialSupplier, 
                     MaterialPrice, 
                     LabourCatagory, 
                     Labour, 
                     LabourPrice, 
                     EquipmentCatagory, 
                     Equipment, 
                     ActivityCatagory, 
                     CostBreakdown, 
                     MaterialBreakdown, 
                     LabourBreakdown, 
                     EquipmentBreakdown,
                     LibraryPackage,
                     StandardLibrary,
                     LibraryBreakdown,
                     LibraryMaterialBreakdown,
                     LibraryLabourBreakdown,
                     LibraryEquipmentBreakdown,
                     NotificationGroup,
                     NotificationType,
                     Notification,
                     UserNotification,
                     )

# Customize admin site header and title
admin.site.site_header = 'Orit-Breakdowns Admin'
admin.site.site_title = 'Orit Breakdowns Admin'

# Register Company
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_title', 'registered_date',)
    list_filter = ('registered_date',)

# Register PackageType
admin.site.register(PackageType)

# Register Package
@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('full_title', 'package_type', 'duration', 'max_members', 'price', 'level', 'default',)
    list_filter = ('package_type', 'duration', 'max_members', 'price',)

# Register CompanyMembership
@admin.register(CompanyMembership)
class CompanyMembershipAdmin(admin.ModelAdmin):
    list_display = ('company', 'registered_at', 'start_date', 'end_date', 'approved',)
    list_filter = ('end_date', 'approved',)

# Register UserMembership
@admin.register(UserMembership)
class UserMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_membership', 'package', 'registered_at', 'start_date', 'end_date', 'approved',)
    list_filter = ('end_date', 'company_membership', 'package', 'approved',)

# Register UserPayment
@admin.register(UserPayment)
class UserPaymentAdmin(admin.ModelAdmin):
    list_display = ('user_membership', 'amount', 'payment_date',)
    list_filter = ('payment_date', 'amount',)

# Register CompanyPayment
@admin.register(CompanyPayment)
class CompanyPaymentAdmin(admin.ModelAdmin):
    list_display = ('company_membership', 'amount', 'payment_date',)
    list_filter = ('payment_date', 'amount',)

# Register City
admin.site.register(City)

# Register ProjectCatagory
admin.site.register(ProjectCatagory)

# Register Project model
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_title', 'client', 'consultant', 'contractor', 'created_by')
    list_filter = ('created_by', 'contractor', 'consultant', 'client')

# Register UnitCatagory Model
admin.site.register(UnitCatagory)

# Register Unit model
@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('full_title', 'short_title')

# Register MaterialCatagory
admin.site.register(MaterialCatagory)

# Register Material model
@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('full_title', 'updated_at', 'created_by')
    list_filter = ('created_by', 'updated_at')

# Register MaterialSupplier
@admin.register(MaterialSupplier)
class MaterialSupplierAdmin(admin.ModelAdmin):
    list_display = ('full_title', 'short_title', 'created_by')
    list_filter = ('created_by',)

# Register MaterialPrice
@admin.register(MaterialPrice)
class MaterialPriceAdmin(admin.ModelAdmin):
    list_display = ('material', 'supplier', 'price')
    list_filter = ('material', 'supplier', 'price')

# Register LabourCatagory
admin.site.register(LabourCatagory)

# Register Labour model
@admin.register(Labour)
class LabourAdmin(admin.ModelAdmin):
    list_display = ('full_title', 'short_title', 'updated_at', 'created_by')
    list_filter = ('created_by', 'updated_at')

# Register LabourPrice model
@admin.register(LabourPrice)
class LabourPriceAdmin(admin.ModelAdmin):
    list_display = ('labour', 'city', 'hourly_rate')
    list_filter = ('labour', 'city')

# Register EquipmentCatagory
admin.site.register(EquipmentCatagory)

# Register Equipment model
@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('full_title', 'short_title', 'updated_at', 'created_by')
    list_filter = ('created_by', 'updated_at')

# Register CostBreakdownCatagory
admin.site.register(ActivityCatagory)

# Register CostBreakdown model
@admin.register(CostBreakdown)
class CostBreakdownAdmin(admin.ModelAdmin):
    list_display = ('full_title', 'project', 'created_by', 'is_library',)
    list_filter = ('project', 'created_by',)

# Register MaterialBreakdown model
@admin.register(MaterialBreakdown)
class MaterialBreakdownAdmin(admin.ModelAdmin):
    list_display = ('costbreakdown', 'material')
    list_filter = ('costbreakdown', 'material')

# Register LabourBreakdown model
@admin.register(LabourBreakdown)
class LabourBreakdownAdmin(admin.ModelAdmin):
    list_display = ('costbreakdown', 'labour', 'hourly_rate')
    list_filter = ('costbreakdown', 'labour', 'hourly_rate')

# Register EquipmentBreakdown model
@admin.register(EquipmentBreakdown)
class EquipmentBreakdownAdmin(admin.ModelAdmin):
    list_display = ('costbreakdown', 'equipment', 'rental_rate')
    list_filter = ('costbreakdown', 'equipment', 'rental_rate')

# Register Price Package for Standard Libraries
admin.site.register(LibraryPackage)

# Register StandardLibrary
@admin.register(StandardLibrary)
class StandardLibraryAdmin(admin.ModelAdmin):
    list_display = ('full_title', 'library_package')
    list_filter  = ('library_package', )

# Register StandardBreakdown
@admin.register(LibraryBreakdown)
class LibraryBreakdownAdmin(admin.ModelAdmin):
    list_display = ('full_title', 'activity_catagory', 'created_by', 'updated_at', 'is_premium',)
    list_filter = ('activity_catagory', 'updated_at', 'is_premium', 'created_by',)

# Register StandardMaterialBreakdown
@admin.register(LibraryMaterialBreakdown)
class LibraryMaterialBreakdownAdmin(admin.ModelAdmin):
    list_display = ('library_breakdown', 'material', 'updated_at',)
    list_filter = ('library_breakdown', 'material', 'updated_at')

# Register StandardLabourBreakdown
@admin.register(LibraryLabourBreakdown)
class LibraryLabourBreakdownAdmin(admin.ModelAdmin):
    list_display = ('library_breakdown', 'labour', 'updated_at',)
    list_filter = ('library_breakdown', 'labour', 'updated_at',)

# Register StandardEquipmentBreakdown
@admin.register(LibraryEquipmentBreakdown)
class LibraryEquipmentBreakdownAdmin(admin.ModelAdmin):
    list_display = ('library_breakdown', 'equipment', 'updated_at',)
    list_filter = ('library_breakdown', 'equipment', 'updated_at',)

# Register NotificationGroup
admin.site.register(NotificationGroup)

# Register NotificationType
admin.site.register(NotificationType)

# Register Notification
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('full_title', 'notification_group', 'notification_type',)
    list_filter = ('notification_group', 'notification_type',)

# Register UserNotification
@admin.register(UserNotification)
class UserNotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification', 'is_seen', 'updated_at',)
    list_filter = ('user', 'notification', 'is_seen', 'updated_at',)