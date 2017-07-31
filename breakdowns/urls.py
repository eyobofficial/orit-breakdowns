from django.conf.urls import url 
from . import views

app_name = 'breakdowns'

urlpatterns = [
    # Index URL 
    url(r'^$', views.index, name='index'),

    # Cost Breakdown List URL
    url(r'^cost-breakdowns/$', views.cost_breakdown_list, name='cost_breakdown_list'),

    # Cost Breakdown Detail URL
    url(r'^cost-breakdown/(?P<pk>[0-9]+)/$', views.CostBreakdownDetail.as_view(), name='cost_breakdown_detail'),

    # User Cost Breakdown List URL
    url(r'^my-breakdowns/$', views.my_breakdown_list, name='my_breakdown_list'),

    # User Cost Breakdown Detail URL
    url(r'^my-breakdown/(?P<pk>[0-9]+)/$', views.MyBreakdownDetail.as_view(), name='my_breakdown_detail'),

    # User Cost Breakdown Create URL
    url(r'^cost-breakdown/create/$', views.BreakdownCreate.as_view(), name='breakdown_create'),

    # Create a MaterialBreakdown for Breakdown URL
    url(r'^my-breakdown/(?P<pk>[0-9]+)/material/add/$', views.MaterialBreakdownCreate.as_view(), name='material_breakdown_create'),

    # Update a MaterialBreakdown for a Particular Breakdown URL
    url(r'^my-breakdown/(?P<breakdown_pk>[0-9]+)/material/update/(?P<pk>[0-9]+)/$', views.MaterialBreakdownUpdate.as_view(), name='material_breakdown_update'),

    # Delete a MaterialBreakdown for a Particular Breakdown URL
    url(r'^my-breakdown/(?P<breakdown_pk>[0-9]+)/material/delete/(?P<pk>[0-9]+)/$', views.MaterialBreakdownDelete.as_view(), name='material_breakdown_delete'),

    # Create a LabourBreakdown for Breakdown URL
    url(r'^my-breakdown/(?P<pk>[0-9]+)/labour/add/$', views.LabourBreakdownCreate.as_view(), name='labour_breakdown_create'),

    # Update a LabourBreakdown for a Particular Breakdown URL
    url(r'^my-breakdown/(?P<breakdown_pk>[0-9]+)/labour/update/(?P<pk>[0-9]+)/$', views.LabourBreakdownUpdate.as_view(), name='labour_breakdown_update'),

    # Delete a LabourBreakdown for a Particular Breakdown URL
    url(r'^my-breakdown/(?P<breakdown_pk>[0-9]+)/labour/delete/(?P<pk>[0-9]+)/$', views.LabourBreakdownDelete.as_view(), name='labour_breakdown_delete'),

    # Material List URL
    url(r'^materials/$', views.material_list, name='material_list'),

    # Material Detail URL
    url(r'^material/(?P<pk>[0-9]+)/$', views.MaterialDetail.as_view(), name='material_detail'),

    # Labour List URL
    url(r'^labours/$', views.labour_list, name='labour_list'),

    # Labour Detail URL
    url(r'^labour/(?P<pk>[0-9]+)/$', views.LabourDetail.as_view(), name='labour_detail'),

    # Equipment List URL
    url(r'^equipments/$', views.equipment_list, name='equipment_list'),

    # Equipment Detail URL
    url(r'^equipment/(?P<pk>[0-9]+)/$', views.EquipmentDetail.as_view(), name='equipment_detail'),

    # Project List URL
    url(r'^projects/$', views.ProjectList.as_view(), name='project_list'),

    # Project Detail URL
    url(r'^project/(?P<pk>[0-9]+)/$', views.ProjectDetail.as_view(), name='project_detail'),
    
    # Add New Project URL
    url(r'^projects/add/$', views.ProjectCreate.as_view(), name='project_create'),

    # Update Existing Project URL
    url(r'^projects/update/(?P<pk>[0-9]+)/$', views.ProjectUpdate.as_view(), name='project_update'),

    # Delete Existing Project URL
    url(r'^projects/delete/(?P<pk>[0-9]+)/$', views.ProjectDelete.as_view(), name='project_delete'),
]