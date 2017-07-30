from django.contrib import admin
from .models import Project, Unit, MaterialCatagory, Material, LabourCatagory, Labour, EquipmentCatagory, Equipment, CostBreakdownCatagory, CostBreakdown, MaterialBreakdown, LabourBreakdown, EquipmentBreakdown

# Register Project model
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_title', 'client', 'consultant', 'contractor', 'created_by')
    list_filter = ('created_by', 'contractor', 'consultant', 'client')

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

# Register LabourCatagory
admin.site.register(LabourCatagory)

# Register Labour model
@admin.register(Labour)
class LabourAdmin(admin.ModelAdmin):
    list_display = ('full_title', 'short_title', 'updated_at', 'created_by')
    list_filter = ('created_by', 'updated_at')

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
    list_display = ('full_title', 'project', 'created_by')
    list_filter = ('project', 'created_by')

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