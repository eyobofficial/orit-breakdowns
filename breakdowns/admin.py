from django.contrib import admin
from .models import (Company,
                     PackageType,
                     Package,
                     AccountType,
                     CompanyMembership,
                     City, 
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
                     CostBreakdownCatagory, 
                     CostBreakdown, 
                     MaterialBreakdown, 
                     LabourBreakdown, 
                     EquipmentBreakdown,
                     LibraryBreakdownCatagory,
                     StandardLibrary,
                     StandardBreakdown,
                     StandardMaterialBreakdown,
                     StandardLabourBreakdown,
                     StandardEquipmentBreakdown,)

# Customize admin site header and title
admin.site.site_header = 'Orit-Breakdowns Admin'
admin.site.site_title = 'Orit Breakdowns Admin'

# Register Company
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_title', 'registered_date',)
    list_filter = ('registered_date',)

# Register AccountType
@admin.register(AccountType)
class AccountTypeAdmin(admin.ModelAdmin):
    list_display = ('full_title',)

# Register CompanyMembership
@admin.register(CompanyMembership)
class CompanyMembershipAdmin(admin.ModelAdmin):
    list_display = ('company', 'start_date', 'end_date',)
    list_filter = ('end_date',)

# Register City
admin.site.register(City)

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
admin.site.register(CostBreakdownCatagory)

# Register CostBreakdown model
@admin.register(CostBreakdown)
class CostBreakdownAdmin(admin.ModelAdmin):
    list_display = ('full_title', 'project', 'created_by', 'is_library',)
    list_filter = ('project', 'created_by', 'is_library',)

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

# Register LibraryBreakdownCatagory
admin.site.register(LibraryBreakdownCatagory)

# Register StandardLibrary
admin.register(StandardLibrary)
class StandardLibraryAdmin(admin.ModelAdmin):
    list_display = ('full_title', 'is_private', 'company',)
    list_filter  = ('is_private', )

# Register StandardBreakdown
admin.register(StandardBreakdown)
class StandardBreakdownAdmin(admin.ModelAdmin):
    list_display = ('full_title', 'library_breakdown_catagory', 'created_by', 'updated_at', 'is_premium',)
    list_filter = ('library_breakdown_catagory', 'updated_at', 'is_premium', 'created_by',)

# Register StandardMaterialBreakdown
admin.register(StandardMaterialBreakdown)
class StandardMaterialBreakdownAdmin(admin.ModelAdmin):
    list_display = ('standard_breakdown', 'material', 'updated_at',)
    list_filter = ('standard_breakdown', 'material', 'updated_at')

# Register StandardLabourBreakdown
admin.register(StandardLabourBreakdown)
class StandardLabourBreakdownAdmin(admin.ModelAdmin):
    list_display = ('standard_breakdown', 'labour', 'updated_at',)
    list_filter = ('standard_breakdown', 'labour', 'updated_at',)

# Register StandardEquipmentBreakdown
admin.register(StandardEquipmentBreakdown)
class StandardEquipmentBreakdownAdmin(admin.ModelAdmin):
    list_display = ('standard_breakdown', 'equipment', 'updated_at',)
    list_filter = ('standard_breakdown', 'equipment', 'updated_at',)