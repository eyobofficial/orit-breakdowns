from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import Http404
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignupForm
from .models import Project, Unit, MaterialCatagory, Material, LabourCatagory, Labour, EquipmentCatagory, Equipment, CostBreakdownCatagory, CostBreakdown, MaterialBreakdown, LabourBreakdown, EquipmentBreakdown

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
        context['page_name'] = 'Materials'
        return context

# Labour List View
@login_required
def labour_list(request):
    """
    Returns labour list 
    """
    try:
        labour_catagory = int(request.GET.get('labour_catagory'))
    except:
        labour_catagory = None
    labour_search = request.GET.get('labour_search')

    # Admin User
    admin = User.objects.get(pk=1)
    
    # Return all labour objects
    try:
        labour_list = Labour.objects.filter(created_by=admin.id)
    except Labour.DoesNotExist:
        raise Http404('page not found')


    if labour_catagory is not None:
        labour_catagory = int(labour_catagory)
        labour_list = Labour.objects.filter(labour_catagory=labour_catagory)

    if labour_search is not None:
        labour_list = labour_list.filter(full_title__icontains=labour_search)      

    labour_catagory_list = get_list_or_404(LabourCatagory)
    page_name = 'Labours'
    template_name = 'breakdowns/labour_list.html'

    return render(request, template_name, context={
            'labour_list': labour_list,
            'labour_catagory_list': labour_catagory_list,
            'page_name': page_name,
            'labour_search': labour_search,
            'labour_catagory': labour_catagory,
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
class ProjectDetail(LoginRequiredMixin, generic.DetailView):
    model = Project

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
class ProjectUpdate(LoginRequiredMixin, UpdateView):
    model = Project
    fields = ['full_title', 'short_title', 'city', 'client', 'consultant', 'contractor',]

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
    Returns cost breakdown list 
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
    page_name = 'CostBreakdowns'
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
@login_required
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
        cost_breakdown_list = CostBreakdown.objects.filter(created_by=request.user.id)
    except CostBreakdown.DoesNotExist:
        raise Http404('page not found')


    if project is not None:
        project = int(project)
        cost_breakdown_list = CostBreakdown.objects.filter(created_by=request.user.id).filter(project=project)

    if cost_breakdown_search is not None:
        cost_breakdown_list = cost_breakdown_list.filter(created_by=request.user.id).filter(full_title__icontains=cost_breakdown_search)      

    project_list = get_list_or_404(Project)
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
class MyBreakdownDetail(LoginRequiredMixin, generic.DetailView):
    model = CostBreakdown
    template_name = 'breakdowns/my_breakdown_detail.html'
    context_object_name = 'cost_breakdown'

    def get_context_data(self, *args, **kwargs):
        context = super(MyBreakdownDetail, self).get_context_data(*args, **kwargs)
        
        # Inititalize direct material cost subtotal for this cost breakdown
        material_direct_cost = 0
        material_list = MaterialBreakdown.objects.filter(costbreakdown_id=self.kwargs['pk']).order_by('rate')
        
        # Calculate material cost subtotal
        for material in material_list:
            material_direct_cost += material.subtotal()

        # Initialize direct labour costs
        labour_direct_cost = 0
        labour_list = LabourBreakdown.objects.filter(costbreakdown_id=self.kwargs['pk']).order_by('-hourly_rate')

        # Calculate labour cost subtotal
        for labour in labour_list:
            labour_direct_cost += labour.subtotal()

        # Initialize direct equipment cost subtotal
        equipment_direct_cost = 0

        # Calculate equipment cost subtotal
        equipment_list = EquipmentBreakdown.objects.filter(costbreakdown_id=self.kwargs['pk']).order_by('-rental_rate')
        for equipment in equipment_list:
            equipment_direct_cost += equipment.subtotal()

        # Calculate total direct cost
        direct_cost = material_direct_cost + labour_direct_cost + equipment_direct_cost

        # Calculate indirect cost
        indirect_cost = round(direct_cost * (context['cost_breakdown'].profit + context['cost_breakdown'].overhead) / 100, 2)

        # Calculate total cost ( after profit and overhead)
        total_cost = direct_cost + indirect_cost 

        context['material_list'] = material_list
        context['material_direct_cost'] = material_direct_cost
        context['labour_list'] = labour_list
        context['labour_direct_cost'] = labour_direct_cost
        context['equipment_list'] = equipment_list
        context['equipment_direct_cost'] = equipment_direct_cost
        context['direct_cost'] = direct_cost
        context['total_cost'] = total_cost
        context['page_name'] = 'CostBreakdowns'
        context['subpage_name'] = 'library'
        return context

# CostBreakdown Detail View
class CostBreakdownDetail(LoginRequiredMixin, generic.DetailView):
    model = CostBreakdown
    context_object_name = 'cost_breakdown'

    def get_context_data(self, *args, **kwargs):
        context = super(CostBreakdownDetail, self).get_context_data(*args, **kwargs)
        
        # Inititalize direct material cost subtotal for this cost breakdown
        material_direct_cost = 0
        material_list = MaterialBreakdown.objects.filter(costbreakdown_id=self.kwargs['pk']).order_by('rate')
        
        # Calculate material cost subtotal
        for material in material_list:
            material_direct_cost += material.subtotal()

        # Initialize direct labour costs
        labour_direct_cost = 0
        labour_list = LabourBreakdown.objects.filter(costbreakdown_id=self.kwargs['pk']).order_by('-hourly_rate')

        # Calculate labour cost subtotal
        for labour in labour_list:
            labour_direct_cost += labour.subtotal()

        # Initialize direct equipment cost subtotal
        equipment_direct_cost = 0

        # Calculate equipment cost subtotal
        equipment_list = EquipmentBreakdown.objects.filter(costbreakdown_id=self.kwargs['pk']).order_by('-rental_rate')
        for equipment in equipment_list:
            equipment_direct_cost += equipment.subtotal()

        # Calculate total direct cost
        direct_cost = material_direct_cost + labour_direct_cost + equipment_direct_cost

        # Calculate indirect cost
        indirect_cost = round(direct_cost * (context['cost_breakdown'].profit + context['cost_breakdown'].overhead) / 100, 2)

        # Calculate total cost ( after profit and overhead)
        total_cost = direct_cost + indirect_cost 

        context['material_list'] = material_list
        context['material_direct_cost'] = material_direct_cost
        context['labour_list'] = labour_list
        context['labour_direct_cost'] = labour_direct_cost
        context['equipment_list'] = equipment_list
        context['equipment_direct_cost'] = equipment_direct_cost
        context['direct_cost'] = direct_cost
        context['total_cost'] = total_cost
        context['page_name'] = 'CostBreakdowns'
        context['subpage_name'] = 'library'
        return context

# Create a new cost breakdown view
class BreakdownCreate(LoginRequiredMixin, CreateView):
    """
    Create a new cost breakdown with the current user as it's
    owner
    """
    model = CostBreakdown
    template_name = 'breakdowns/my_breakdown_form.html'
    success_url = '/breakdowns/mybreakdown/{id}'
    fields = ['cost_breakdown_catagory', 'project', 'full_title', 'description', 'unit', 'output', 'overhead', 'profit',]

    def form_valid(self, form, *args, **kwargs):
        form.instance.created_by = self.request.user
        return super(BreakdownCreate, self).form_valid(form, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(BreakdownCreate, self).get_context_data(*args, **kwargs)
        context['project_list'] = Project.objects.filter(created_by=self.request.user.id)
        context['catagory_list'] = CostBreakdownCatagory.objects.all()
        context['unit_list'] = Unit.objects.all()
        context['page_name'] = 'CostBreakdowns'
        context['subpage_name'] = 'Add'
        return context

# Create A Material Breakdown View
class MaterialBreakdownCreate(LoginRequiredMixin, CreateView):
    model = MaterialBreakdown
    fields = ['material', 'unit', 'quantity', 'rate', ]
    template_name = 'breakdowns/material_breakdown_form.html'

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
class MaterialBreakdownUpdate(LoginRequiredMixin, UpdateView):
    model = MaterialBreakdown
    fields = ['material', 'unit', 'quantity', 'rate', ]
    template_name = 'breakdowns/material_breakdown_form.html'
    context_object_name = 'material'

    def get_success_url(self):
        return reverse('breakdowns:my_breakdown_detail', kwargs={'pk': self.kwargs['breakdown_pk']})

    def get_context_data(self, *args, **kwargs):
        context = super(MaterialBreakdownUpdate, self).get_context_data(*args, **kwargs)
        context['cost_breakdown'] = CostBreakdown.objects.get(pk=self.kwargs['breakdown_pk'])
        context['material_list'] = Material.objects.all()
        context['unit_list'] = Unit.objects.all()
        context['page_name'] = 'CostBreakdowns'
        context['subpage_name'] = 'mybreakdowns'
        return context