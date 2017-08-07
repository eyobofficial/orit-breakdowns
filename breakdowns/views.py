from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import Http404, HttpResponse
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.conf import settings
from datetime import date
import openpyxl
from .forms import SignupForm
from .models import City, Project, Unit, MaterialCatagory, Material, MaterialPrice, LabourCatagory, Labour, LabourPrice, EquipmentCatagory, Equipment, CostBreakdownCatagory, CostBreakdown, MaterialBreakdown, LabourBreakdown, EquipmentBreakdown

# Create your views here.
@login_required
def index(request):
    return render(request, 'breakdowns/index.html', context={
            'page_name': 'Index',
        })

# Signup view
def signup(request):
    """
    Register a new user, login the new user and redirect to breakdowns:index page
    """

    # Check if user already logged
    if request.user.is_authenticated:
        return redirect('breakdowns:index')
        
    form_class = SignupForm
    template_name = 'registration/signup.html'

    if request.method == 'POST':
        form = form_class(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            form.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            user.first_name = first_name
            user.last_name = last_name
            member_group = Group.objects.get(name='member')
            user.groups.add(member_group,)
            user.save()
            login(request, user)
            return redirect('breakdowns:index')
    else:
        form = form_class()
    return render(request, template_name, context={'form': form})

# Material List View
@login_required
def material_list(request):
    """
    Returns material list 
    """
    try:
        material_catagory = int(request.GET.get('material_catagory'))
    except:
        material_catagory = None
    material_search = request.GET.get('material_search')

    # Admin User
    admin = User.objects.get(pk=1)
    
    # Return all material objects
    try:
        material_list = Material.objects.filter(created_by=admin.id)
    except Material.DoesNotExist:
        raise Http404('page not found')


    if material_catagory is not None:
        material_catagory = int(material_catagory)
        material_list = Material.objects.filter(material_catagory=material_catagory)

    if material_search is not None:
        material_list = material_list.filter(full_title__icontains=material_search)      

    material_catagory_list = get_list_or_404(MaterialCatagory)
    page_name = 'Materials'
    template_name = 'breakdowns/material_list.html'

    return render(request, template_name, context={
            'material_list': material_list,
            'material_catagory_list': material_catagory_list,
            'page_name': page_name,
            'material_search': material_search,
            'material_catagory': material_catagory,
        })

# Material Detail View
class MaterialDetail(LoginRequiredMixin, generic.DetailView):
    model = Material

    def get_context_data(self, *args, **kwargs):
        context = super(MaterialDetail, self).get_context_data(*args, **kwargs)
        context['price_list'] = MaterialPrice.objects.filter(material_id=self.kwargs['pk'])
        context['page_name'] = 'Materials'
        return context

# Labour List View
@login_required
def labour_list(request):
    """
    Returns labour list 
    """
    labour_search = request.GET.get('labour_search')

    try:
        labour_city = int(request.GET['city'])
    except:
        default_city = City.objects.get(full_title='Addis Ababa')
        labour_city = default_city.id

    labour_price_list = LabourPrice.objects.filter(city=labour_city)

    if labour_search is not None:
        labour_list = []
        for labour_price in labour_price_list:
            if str(labour_search) in str(labour_price.labour.full_title):
                labour_list.append(labour_price)
    else:
        labour_list = list(labour_price_list)


    city_list = get_list_or_404(City)
    page_name = 'Labours'
    template_name = 'breakdowns/labour_list.html'

    return render(request, template_name, context={
            'labour_price_list': labour_list,
            'city_list': city_list,
            'page_name': page_name,
            'labour_search': labour_search,
            'labour_city': labour_city,
        })

# Labour Detail View
class LabourDetail(LoginRequiredMixin, generic.DetailView):
    model = Labour

    def get_context_data(self, *args, **kwargs):
        context = super(LabourDetail, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'Labours'
        return context

# Equipment List View
@login_required
def equipment_list(request):
    """
    Returns equipment list 
    """
    try:
        equipment_catagory = int(request.GET.get('equipment_catagory'))
    except:
        equipment_catagory = None
    equipment_search = request.GET.get('equipment_search')

    # Admin User
    admin = User.objects.get(pk=1)
    
    # Return all equipment objects
    try:
        equipment_list = Equipment.objects.filter(created_by=admin.id)
    except Equipment.DoesNotExist:
        raise Http404('page not found')


    if equipment_catagory is not None:
        equipment_catagory = int(equipment_catagory)
        equipment_list = Equipment.objects.filter(equipment_catagory=equipment_catagory)

    if equipment_search is not None:
        equipment_list = equipment_list.filter(full_title__icontains=equipment_search)      

    equipment_catagory_list = get_list_or_404(EquipmentCatagory)
    page_name = 'Equipments'
    template_name = 'breakdowns/equipment_list.html'

    return render(request, template_name, context={
            'equipment_list': equipment_list,
            'equipment_catagory_list': equipment_catagory_list,
            'page_name': page_name,
            'equipment_search': equipment_search,
            'equipment_catagory': equipment_catagory,
        })

# Equipment Detail View
class EquipmentDetail(LoginRequiredMixin, generic.DetailView):
    model = Equipment

    def get_context_data(self, *args, **kwargs):
        context = super(EquipmentDetail, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'Equipments'
        return context

# Project List View
class ProjectList(LoginRequiredMixin, generic.ListView):
    model = Project

    def get_queryset(self, *args, **kwargs):
        return Project.objects.filter(created_by=self.request.user.id)

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectList, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'Projects'
        return context

# Project Detail View
class ProjectDetail(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Project
    login_url = 'breakdowns:project_list'
    redirect_field_name = None

    def test_func(self):
        project = Project.objects.get(pk=self.kwargs['pk'])
        return project.created_by.id == self.request.user.id

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectDetail, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'Projects'
        return context

# Project Create View
class ProjectCreate(LoginRequiredMixin, CreateView):
    model = Project
    fields = ['full_title', 'short_title', 'city', 'client', 'consultant', 'contractor',]

    def form_valid(self, form, *args, **kwargs):
        form.instance.created_by = self.request.user 
        return super(ProjectCreate, self).form_valid(form, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectCreate, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'Projects'
        context['subpage_name'] = 'Add'
        return context

# Project Update View
class ProjectUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    fields = ['full_title', 'short_title', 'city', 'client', 'consultant', 'contractor',]
    login_url = 'breakdowns:project_list'
    redirect_field_name = None

    def test_func(self):
        project = Project.objects.get(pk=self.kwargs['pk'])
        return project.created_by.id == self.request.user.id

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectUpdate, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'Projects'
        return context

# Project Delete View
class ProjectDelete(LoginRequiredMixin, DeleteView):
    model = Project 
    success_url = reverse_lazy('breakdowns:project_list')

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectDelete, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'Projects'
        return context

# Cost Breakdown List View
@login_required
def cost_breakdown_list(request):
    """
    Returns cost breakdown list from the main library
    """
    try:
        cost_breakdown_catagory = int(request.GET.get('cost_breakdown_catagory'))
    except:
        cost_breakdown_catagory = None
    cost_breakdown_search = request.GET.get('cost_breakdown_search')

    # Admin User
    admin = User.objects.get(pk=1)
    
    # Return all cost breakdown objects
    try:
        cost_breakdown_list = CostBreakdown.objects.filter(created_by=admin.id)
    except CostBreakdown.DoesNotExist:
        raise Http404('page not found')


    if cost_breakdown_catagory is not None:
        cost_breakdown_catagory = int(cost_breakdown_catagory)
        cost_breakdown_list = CostBreakdown.objects.filter(created_by=admin.id).filter(cost_breakdown_catagory=cost_breakdown_catagory)

    if cost_breakdown_search is not None:
        cost_breakdown_list = cost_breakdown_list.filter(created_by=admin.id).filter(full_title__icontains=cost_breakdown_search)      

    cost_breakdown_catagory_list = get_list_or_404(CostBreakdownCatagory)
    page_name = 'library'
    template_name = 'breakdowns/cost_breakdown_list.html'

    return render(request, template_name, context={
            'cost_breakdown_list': cost_breakdown_list,
            'cost_breakdown_catagory_list': cost_breakdown_catagory_list,
            'page_name': page_name,
            'subpage_name': 'library',
            'cost_breakdown_search': cost_breakdown_search,
            'cost_breakdown_catagory': cost_breakdown_catagory,
        })

# My Breakdown List View
@permission_required(('breakdowns.manage_cost_breakdown'))
def my_breakdown_list(request):
    """
    Returns user cost breakdown list 
    """
    try:
        project = int(request.GET.get('project'))
    except:
        project = None
    cost_breakdown_search = request.GET.get('cost_breakdown_search')
    
    # Return all cost breakdown objects
    try:
        cost_breakdown_list = CostBreakdown.objects.filter(created_by=request.user.id).order_by('-updated_at')
    except CostBreakdown.DoesNotExist:
        raise Http404('page not found')


    if project is not None:
        project = int(project)
        cost_breakdown_list = CostBreakdown.objects.filter(created_by=request.user.id).filter(project=project).order_by('-updated_at')

    if cost_breakdown_search is not None:
        cost_breakdown_list = cost_breakdown_list.filter(created_by=request.user.id).filter(full_title__icontains=cost_breakdown_search)      

    try:
        project_list = Project.objects.filter(created_by=request.user.id)
    except:
        project_list = []
        
    page_name = 'CostBreakdowns'
    template_name = 'breakdowns/my_breakdown_list.html'

    return render(request, template_name, context={
            'cost_breakdown_list': cost_breakdown_list,
            'project_list': project_list,
            'page_name': page_name,
            'subpage_name': 'mybreakdowns',
            'cost_breakdown_search': cost_breakdown_search,
            'project': project,
        })

# My Cost Breakdowns Detail
class MyBreakdownDetail(PermissionRequiredMixin, UserPassesTestMixin, generic.DetailView):
    permission_required = ('breakdowns.manage_cost_breakdown',)
    model = CostBreakdown
    template_name = 'breakdowns/breakdown_detail.html'
    context_object_name = 'cost_breakdown'
    login_url = 'breakdowns:my_breakdown_list'
    redirect_field_name = None

    def test_func(self, *args, **kwargs):
        cost_breakdown = CostBreakdown.objects.get(pk=self.kwargs['pk'])
        return cost_breakdown.created_by.id == self.request.user.id

    def get(self, *args, **kwargs):
        if self.request.GET.get('excel'):
            # Get context object
            self.object = self.get_object()

            # Get Material, Labour and Equipment list
            material_list = list(MaterialBreakdown.objects.filter(costbreakdown_id=self.object.id).order_by('-rate'))
            labour_list = list(LabourBreakdown.objects.filter(costbreakdown_id=self.object.id).order_by('-hourly_rate'))
            equipment_list = list(EquipmentBreakdown.objects.filter(costbreakdown_id=self.object.id).order_by('-rental_rate'))

            row_count = max(len(material_list), len(labour_list), len(equipment_list))

            # Import Excel Template
            if row_count <= 14:
                excel_template_path = settings.MEDIA_ROOT + 'Template_sm.xlsx'
            elif row_count > 14 and row_count <= 18:
                pass
            else:
                pass
            
            wb = openpyxl.load_workbook(excel_template_path)
            wb.template = True
            ws = wb.get_sheet_by_name('breakdown')

            # Add General breakdown data to excel
            ws['D1'].value = self.object.project.full_title
            ws['D2'].value = self.object.project.client
            ws['D3'].value = self.object.project.consultant
            ws['D4'].value = self.object.project.contractor
            ws['D6'].value = self.object.full_title
            ws['P1'].value = self.object.project.city
            # ws['P2'].value = self.

            # Add Material Breakdown data to excel
            if len(material_list) > 0:
                mb_row_count = 13 # Material Excel Row Starts at 7 row

                for mb in enumerate(material_list, start=1):
                    ws['A{}'.format(mb_row_count)].value = mb[0]
                    ws['B{}'.format(mb_row_count)].value = mb[1].material.full_title 
                    ws['C{}'.format(mb_row_count)].value = mb[1].unit.short_title
                    ws['D{}'.format(mb_row_count)].value = mb[1].quantity
                    ws['E{}'.format(mb_row_count)].value = mb[1].rate
                    mb_row_count += 1

            # Add Labour Breakdown data to excel
            if len(labour_list) > 0:
                lb_row_count = 13 # Labour Excel Row Starts at 7 row

                ws['L32'].value = self.object.output

                for lb in enumerate(labour_list, start=1):
                    ws['H{}'.format(lb_row_count)].value = lb[1].labour.full_title 
                    ws['I{}'.format(lb_row_count)].value = lb[1].number
                    ws['J{}'.format(lb_row_count)].value = lb[1].uf
                    ws['E{}'.format(lb_row_count)].value = lb[1].hourly_rate
                    lb_row_count += 1

            # Add Equipement Breakdown data to excel
            if len(equipment_list) > 0:
                eb_row_count = 13 # Equipement Excel Row Starts at 7 row

                ws['R32'].value = self.object.output

                for eb in enumerate(equipment_list, start=1):
                    ws['N{}'.format(eb_row_count)].value = eb[1].equipment.full_title 
                    ws['O{}'.format(eb_row_count)].value = eb[1].number
                    ws['P{}'.format(eb_row_count)].value = eb[1].uf
                    ws['Q{}'.format(eb_row_count)].value = eb[1].rental_rate
                    eb_row_count += 1

            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=cost_breakdown_{}.xlsx'.format(self.object.id)

            wb.save(response)
            return response
        return super(MyBreakdownDetail, self).get(*args, **kwargs)


    def get_context_data(self, *args, **kwargs):
        context = super(MyBreakdownDetail, self).get_context_data(*args, **kwargs)
        
        # Material List
        material_list = MaterialBreakdown.objects.filter(costbreakdown_id=self.kwargs['pk']).order_by('rate')

        # Labour List
        labour_list = LabourBreakdown.objects.filter(costbreakdown_id=self.kwargs['pk']).order_by('-hourly_rate')

        # Equipment List
        equipment_list = EquipmentBreakdown.objects.filter(costbreakdown_id=self.kwargs['pk']).order_by('-rental_rate')

        if not context['cost_breakdown'].is_library:
            material_direct_cost = 0
                        
            # Calculate material cost subtotal
            for material in material_list:
                material_direct_cost += material.subtotal()

            context['material_direct_cost'] = material_direct_cost

            # Initialize direct labour costs
            labour_direct_cost = 0
           
            # Calculate labour cost subtotal
            for labour in labour_list:
                labour_direct_cost += labour.subtotal()

            context['labour_direct_cost'] = labour_direct_cost

            # Initialize direct equipment cost subtotal
            equipment_direct_cost = 0

            # Calculate equipment cost subtotal       
            for equipment in equipment_list:
                equipment_direct_cost += equipment.subtotal()

            context['equipment_direct_cost'] = equipment_direct_cost

            # Calculate total direct cost
            direct_cost = material_direct_cost + labour_direct_cost + equipment_direct_cost
            context['direct_cost'] = direct_cost

            # Calculate indirect cost
            indirect_cost = round(direct_cost * (context['cost_breakdown'].profit + context['cost_breakdown'].overhead) / 100, 2)

            # Calculate total cost ( after profit and overhead)
            total_cost = direct_cost + indirect_cost
            context['total_cost'] = total_cost

        context['material_list'] = material_list        
        context['labour_list'] = labour_list
        context['equipment_list'] = equipment_list     
        context['page_name'] = 'CostBreakdowns'
        context['subpage_name'] = 'mybreakdowns'
        return context

# CostBreakdown Detail View
class CostBreakdownDetail(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = CostBreakdown
    context_object_name = 'cost_breakdown'
    template_name = 'breakdowns/library_detail.html'
    login_url = 'breakdowns:cost_breakdown_list'
    redirect_field_name = None

    def test_func(self, *args, **kwargs):
        cost_breakdown = CostBreakdown.objects.get(pk=self.kwargs['pk'])
        return cost_breakdown.created_by.has_perm('breakdowns.admin_cost_breakdown')

    def get_context_data(self, *args, **kwargs):
        context = super(CostBreakdownDetail, self).get_context_data(*args, **kwargs)
        
        # Material List
        material_list = MaterialBreakdown.objects.filter(costbreakdown_id=self.kwargs['pk']).order_by('rate')

        # Labours List
        labour_list = LabourBreakdown.objects.filter(costbreakdown_id=self.kwargs['pk']).order_by('-hourly_rate')

        # Equipement
        equipment_list = EquipmentBreakdown.objects.filter(costbreakdown_id=self.kwargs['pk']).order_by('-rental_rate')

        context['material_list'] = material_list
        context['labour_list'] = labour_list
        context['equipment_list'] = equipment_list
        context['page_name'] = 'library'
        return context

# Create a new cost breakdown view
class BreakdownCreate(LoginRequiredMixin, CreateView):
    """
    Create a new cost breakdown with the current user as it's owner
    """
    model = CostBreakdown
    template_name = 'breakdowns/breakdown_form.html'
    fields = ['cost_breakdown_catagory', 'project', 'full_title', 'description', 'unit', 'output', 'overhead', 'profit',]

    def form_valid(self, form, *args, **kwargs):
        form.instance.created_by = self.request.user
        return super(BreakdownCreate, self).form_valid(form, *args, **kwargs)

    def get_success_url(self, *args, **kwargs):
        if self.object.is_library:
            return reverse('breakdowns:cost_breakdown_detail', kwargs={'pk': self.object.id})
        return reverse('breakdowns:my_breakdown_detail', kwargs={'pk': self.object.id})

    def get_context_data(self, *args, **kwargs):
        context = super(BreakdownCreate, self).get_context_data(*args, **kwargs)
        context['project_list'] = Project.objects.filter(created_by=self.request.user.id)
        context['catagory_list'] = CostBreakdownCatagory.objects.all()
        context['unit_list'] = Unit.objects.all()

        if self.request.user.has_perm('breakdowns.manage_library'):
            context['page_name'] = 'library'
        else:
            context['page_name'] = 'CostBreakdowns'
        context['subpage_name'] = 'add'
        return context

# Create A Material Breakdown View
class MaterialBreakdownCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = MaterialBreakdown
    fields = ['material', 'unit', 'quantity', 'rate', ]
    template_name = 'breakdowns/material_breakdown_form.html'
    login_url = 'breakdowns:my_breakdown_list'
    redirect_field_name = None

    def test_func(self, *args, **kwargs):
        cost_breakdown = CostBreakdown.objects.get(pk=self.kwargs['pk'])
        return cost_breakdown.created_by.id == self.request.user.id

    def get_success_url(self):
        return reverse('breakdowns:my_breakdown_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form, *args, **kwargs):
        form.instance.costbreakdown = CostBreakdown.objects.get(pk=self.kwargs['pk'])
        return super(MaterialBreakdownCreate, self).form_valid(form, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(MaterialBreakdownCreate, self).get_context_data(*args, **kwargs)
        context['cost_breakdown'] = CostBreakdown.objects.get(pk=self.kwargs['pk'])
        context['material_list'] = Material.objects.all()
        context['unit_list'] = Unit.objects.all()
        context['page_name'] = 'CostBreakdowns'
        context['subpage_name'] = 'mybreakdowns'
        return context

# Update A Material Breakdown 
class MaterialBreakdownUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = MaterialBreakdown
    fields = ['material', 'unit', 'quantity', 'rate', ]
    template_name = 'breakdowns/material_breakdown_form.html'
    login_url = 'breakdowns:my_breakdown_list'
    redirect_field_name = None

    def test_func(self, *args, **kwargs):
        cost_breakdown = CostBreakdown.objects.get(pk=self.kwargs['breakdown_pk'])
        material_breakdown = MaterialBreakdown.objects.get(pk=self.kwargs['pk'])
        return material_breakdown.costbreakdown.id == cost_breakdown.id

    def get_success_url(self):
        return reverse('breakdowns:my_breakdown_detail', kwargs={'pk': self.kwargs['breakdown_pk']})

    def get_context_data(self, *args, **kwargs):
        context = super(MaterialBreakdownUpdate, self).get_context_data(*args, **kwargs)
        context['cost_breakdown'] = CostBreakdown.objects.get(pk=self.kwargs['breakdown_pk'])
        context['material_breakdown'] = MaterialBreakdown.objects.get(pk=self.kwargs['pk'])
        context['material_list'] = Material.objects.all()
        context['unit_list'] = Unit.objects.all()
        context['page_name'] = 'CostBreakdowns'
        context['subpage_name'] = 'mybreakdowns'
        return context

# Delete A Material Breakdown 
class MaterialBreakdownDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = MaterialBreakdown
    template_name = 'breakdowns/material_breakdown_confirm_delete.html'
    login_url = 'breakdowns:my_breakdown_list'
    redirect_field_name = None

    def test_func(self, *args, **kwargs):
        cost_breakdown = CostBreakdown.objects.get(pk=self.kwargs['breakdown_pk'])
        material_breakdown = MaterialBreakdown.objects.get(pk=self.kwargs['pk'])
        return material_breakdown.costbreakdown.id == cost_breakdown.id

    def get_success_url(self, *args, **kwargs):
        cost_breakdown = CostBreakdown.objects.get(pk=self.kwargs['breakdown_pk'])
        if cost_breakdown.is_library:
            return reverse('breakdowns:cost_breakdown_detail', kwargs={'pk': self.kwargs['breakdown_pk']})
        return reverse('breakdowns:my_breakdown_detail', kwargs={'pk': self.kwargs['breakdown_pk']})

    def get_context_data(self, *args, **kwargs):
        context = super(MaterialBreakdownDelete, self).get_context_data(*args, **kwargs)
        context['cost_breakdown'] = CostBreakdown.objects.get(pk=self.kwargs['breakdown_pk'])
        context['material_breakdown'] = MaterialBreakdown.objects.get(pk=self.kwargs['pk'])
        context['page_name'] = 'CostBreakdowns'
        context['subpage_name'] = 'mybreakdowns'
        return context

# Create A Labour Breakdown View
class LabourBreakdownCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = LabourBreakdown
    fields = ['labour', 'number', 'uf', 'hourly_rate', ]
    template_name = 'breakdowns/labour_breakdown_form.html'
    login_url = 'breakdowns:my_breakdown_list'
    redirect_field_name = None

    def test_func(self, *args, **kwargs):
        cost_breakdown = CostBreakdown.objects.get(pk=self.kwargs['pk'])
        return cost_breakdown.created_by.id == self.request.user.id

    def get_success_url(self):
        return reverse('breakdowns:my_breakdown_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form, *args, **kwargs):
        form.instance.costbreakdown = CostBreakdown.objects.get(pk=self.kwargs['pk'])
        return super(LabourBreakdownCreate, self).form_valid(form, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(LabourBreakdownCreate, self).get_context_data(*args, **kwargs)
        context['cost_breakdown'] = CostBreakdown.objects.get(pk=self.kwargs['pk'])
        context['labour_list'] = Labour.objects.all()
        context['unit_list'] = Unit.objects.all()
        context['page_name'] = 'CostBreakdowns'
        context['subpage_name'] = 'mybreakdowns'
        return context


# Update A Labour Breakdown 
class LabourBreakdownUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = LabourBreakdown
    fields = ['labour', 'number', 'uf', 'hourly_rate', ]
    template_name = 'breakdowns/labour_breakdown_form.html'
    login_url = 'breakdowns:my_breakdown_list'
    redirect_field_name = None

    def test_func(self, *args, **kwargs):
        cost_breakdown = CostBreakdown.objects.get(pk=self.kwargs['breakdown_pk'])
        labour_breakdown = LabourBreakdown.objects.get(pk=self.kwargs['pk'])
        return labour_breakdown.costbreakdown.id == cost_breakdown.id

    def get_success_url(self):
        return reverse('breakdowns:my_breakdown_detail', kwargs={'pk': self.kwargs['breakdown_pk']})

    def get_context_data(self, *args, **kwargs):
        context = super(LabourBreakdownUpdate, self).get_context_data(*args, **kwargs)
        context['cost_breakdown'] = CostBreakdown.objects.get(pk=self.kwargs['breakdown_pk'])
        context['labour_breakdown'] = LabourBreakdown.objects.get(pk=self.kwargs['pk'])
        context['labour_list'] = Labour.objects.all()
        context['unit_list'] = Unit.objects.all()
        context['page_name'] = 'CostBreakdowns'
        context['subpage_name'] = 'mybreakdowns'
        return context

# Delete A Material Breakdown 
class LabourBreakdownDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = LabourBreakdown
    template_name = 'breakdowns/labour_breakdown_confirm_delete.html'
    login_url = 'breakdowns:my_breakdown_list'
    redirect_field_name = None

    def test_func(self, *args, **kwargs):
        cost_breakdown = CostBreakdown.objects.get(pk=self.kwargs['breakdown_pk'])
        labour_breakdown = LabourBreakdown.objects.get(pk=self.kwargs['pk'])
        return labour_breakdown.costbreakdown.id == cost_breakdown.id

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('breakdowns:my_breakdown_detail', kwargs={'pk': self.kwargs['breakdown_pk']})

    def get_context_data(self, *args, **kwargs):
        context = super(LabourBreakdownDelete, self).get_context_data(*args, **kwargs)
        context['cost_breakdown'] = CostBreakdown.objects.get(pk=self.kwargs['breakdown_pk'])
        context['labour_breakdown'] = LabourBreakdown.objects.get(pk=self.kwargs['pk'])
        context['page_name'] = 'CostBreakdowns'
        context['subpage_name'] = 'mybreakdowns'
        return context

# Create A Equipment Breakdown View
class EquipmentBreakdownCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = EquipmentBreakdown
    fields = ['equipment', 'number', 'uf', 'rental_rate', ]
    template_name = 'breakdowns/equipment_breakdown_form.html'
    login_url = 'breakdowns:my_breakdown_list'
    redirect_field_name = None

    def test_func(self, *args, **kwargs):
        cost_breakdown = CostBreakdown.objects.get(pk=self.kwargs['pk'])
        return cost_breakdown.created_by.id == self.request.user.id

    def get_success_url(self):
        return reverse('breakdowns:my_breakdown_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form, *args, **kwargs):
        form.instance.costbreakdown = CostBreakdown.objects.get(pk=self.kwargs['pk'])
        return super(EquipmentBreakdownCreate, self).form_valid(form, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(EquipmentBreakdownCreate, self).get_context_data(*args, **kwargs)
        context['cost_breakdown'] = CostBreakdown.objects.get(pk=self.kwargs['pk'])
        context['equipment_list'] = Equipment.objects.all()
        context['unit_list'] = Unit.objects.all()
        context['page_name'] = 'CostBreakdowns'
        context['subpage_name'] = 'mybreakdowns'
        return context

# Update A Labour Breakdown 
class EquipmentBreakdownUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = EquipmentBreakdown
    fields = ['equipment', 'number', 'uf', 'rental_rate', ]
    template_name = 'breakdowns/equipment_breakdown_form.html'
    login_url = 'breakdowns:my_breakdown_list'
    redirect_field_name = None

    def test_func(self, *args, **kwargs):
        cost_breakdown = CostBreakdown.objects.get(pk=self.kwargs['breakdown_pk'])
        equipment_breakdown = EquipmentBreakdown.objects.get(pk=self.kwargs['pk'])
        return equipment_breakdown.costbreakdown.id == cost_breakdown.id

    def get_success_url(self):
        return reverse('breakdowns:my_breakdown_detail', kwargs={'pk': self.kwargs['breakdown_pk']})

    def get_context_data(self, *args, **kwargs):
        context = super(EquipmentBreakdownUpdate, self).get_context_data(*args, **kwargs)
        context['cost_breakdown'] = CostBreakdown.objects.get(pk=self.kwargs['breakdown_pk'])
        context['equipment_breakdown'] = EquipmentBreakdown.objects.get(pk=self.kwargs['pk'])
        context['equipment_list'] = Equipment.objects.all()
        context['unit_list'] = Unit.objects.all()
        context['page_name'] = 'CostBreakdowns'
        context['subpage_name'] = 'mybreakdowns'
        return context

class EquipmentBreakdownDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = EquipmentBreakdown
    template_name = 'breakdowns/equipment_breakdown_confirm_delete.html'
    login_url = 'breakdowns:my_breakdown_list'
    redirect_field_name = None

    def test_func(self, *args, **kwargs):
        cost_breakdown = CostBreakdown.objects.get(pk=self.kwargs['breakdown_pk'])
        equipment_breakdown = EquipmentBreakdown.objects.get(pk=self.kwargs['pk'])
        return equipment_breakdown.costbreakdown.id == cost_breakdown.id

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('breakdowns:my_breakdown_detail', kwargs={'pk': self.kwargs['breakdown_pk']})

    def get_context_data(self, *args, **kwargs):
        context = super(EquipmentBreakdownDelete, self).get_context_data(*args, **kwargs)
        context['cost_breakdown'] = CostBreakdown.objects.get(pk=self.kwargs['breakdown_pk'])
        context['equipment_breakdown'] = EquipmentBreakdown.objects.get(pk=self.kwargs['pk'])
        context['page_name'] = 'CostBreakdowns'
        context['subpage_name'] = 'mybreakdowns'
        return context