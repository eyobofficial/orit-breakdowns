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
from django.core import serializers
from datetime import date
import openpyxl
from xlrd import open_workbook
from xlwt import Workbook, easyxf, Formula
from xlutils.copy import copy
from .forms import SignupForm, StepOneForm, StepTwoForm, CreateBreakdownForm, ChooseLibraryForm
from .models import Package, UserMembership, City, ProjectCatagory, Project, UnitCatagory, Unit, MaterialCatagory, Material, MaterialPrice, LabourCatagory, Labour, LabourPrice, EquipmentCatagory, Equipment, ActivityCatagory, CostBreakdown, MaterialBreakdown, LabourBreakdown, EquipmentBreakdown, StandardLibrary, LibraryBreakdown

# Create your views here.
@login_required
def index(request):
    # current_membership = list(UserMembership.objects.filter(user=request.user).filter(approved=True).filter(is_expired=False).order_by('-package')[0])
    # request.session['account'] = serializers.serialize('json', current_membership)

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
            email = form.cleaned_data.get('email')
            form.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            # member_group = Group.objects.get(name='member')
            # user.groups.add(member_group,)
            user.save()

            # Register new user to default account package
            # default_package = Package.objects.get(default=True)
            # membership = UserMembership(user=user, package=default_package)
            # membership.save()

            # Login and redirect to user dashboard
            login(request, user)
            return redirect('breakdowns:index')
    else:
        form = form_class()
    return render(request, template_name, context={'form': form})

# Material List View
class MaterialList(LoginRequiredMixin, generic.ListView):
    model = Material

    def get_queryset(self, *args, **kwargs):
        return Material.objects.filter(created_by__is_staff=True)

    def get_context_data(self, *args, **kwargs):
        context = super(MaterialList, self).get_context_data(*args, **kwargs)
        context['catagory_count'] = MaterialCatagory.objects.all().count()
        context['page_name'] = 'materials'
        return context  

# Material Detail View
class MaterialDetail(LoginRequiredMixin, generic.DetailView):
    model = Material

    def get_context_data(self, *args, **kwargs):
        context = super(MaterialDetail, self).get_context_data(*args, **kwargs)
        context['price_list'] = MaterialPrice.objects.filter(material_id=self.kwargs['pk'])
        context['page_name'] = 'materials'
        return context

# Labour List View
class LabourPriceList(LoginRequiredMixin, generic.ListView):
    model = LabourPrice
    template_name = 'breakdowns/labour_list.html'
    context_object_name = 'labour_price_list'

    def get_queryset(self, *args, **kwargs):
        # return LabourPrice.objects.filter(created_by__is_staff=True)
        return LabourPrice.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(LabourPriceList, self).get_context_data(*args, **kwargs)
        context['catagory_count'] = LabourCatagory.objects.all().count()
        context['city_count'] = City.objects.all().count()
        context['page_name'] = 'labour'
        return context  

# Labour Detail View
class LabourDetail(LoginRequiredMixin, generic.DetailView):
    model = Labour

    def get_context_data(self, *args, **kwargs):
        context = super(LabourDetail, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'labour'
        return context

# Equipment List View
class EquipmentList(LoginRequiredMixin, generic.ListView):
    model = Equipment

    def get_queryset(self, *args, **kwargs):
        return Equipment.objects.filter(created_by__is_staff=True)

    def get_context_data(self, *args, **kwargs):
        context = super(EquipmentList, self).get_context_data(*args, **kwargs)
        context['catagory_count'] = EquipmentCatagory.objects.all().count()
        context['page_name'] = 'equipment'
        return context 

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
        context['catagory_count'] = ProjectCatagory.objects.all().count()
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
    fields = ['full_title', 'short_title', 'city', 'client', 'consultant', 'contractor', 'project_catagory',]
    success_url = '/breakdowns/projects/'
    redirect_field_name = None
    
    def form_valid(self, form, *args, **kwargs):
        form.instance.created_by = self.request.user 
        return super(ProjectCreate, self).form_valid(form, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectCreate, self).get_context_data(*args, **kwargs)
        context['catagory_list'] = ProjectCatagory.objects.all();
        context['page_name'] = 'Projects'
        return context

# Project Update View
class ProjectUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    fields = ['full_title', 'short_title', 'city', 'client', 'consultant', 'contractor', 'project_catagory',]
    login_url = 'breakdowns:project_list'
    success_url = '/breakdowns/projects/'
    redirect_field_name = None

    def test_func(self):
        project = Project.objects.get(pk=self.kwargs['pk'])
        return project.created_by.id == self.request.user.id

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectUpdate, self).get_context_data(*args, **kwargs)
        context['catagory_list'] = ProjectCatagory.objects.all();
        context['page_name'] = 'Projects'
        return context

# Project Delete View
class ProjectDelete(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'breakdowns/project_form.html'
    success_url = reverse_lazy('breakdowns:project_list')

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectDelete, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'Projects'
        return context

# Standard Library Detail 
class StandardLibraryDetail(LoginRequiredMixin, generic.DetailView):
    model = StandardLibrary
    context_object_name = 'library'
    template_name = 'breakdowns/library_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(StandardLibraryDetail, self).get_context_data(*args, **kwargs)
        context['breakdown_list'] = LibraryBreakdown.objects.filter(standard_library=self.kwargs['pk'])
        context['page_name'] = 'library'
        context['subpage_name'] = self.object.full_title 
        return context

# Standard Library Breakdown Detail
class LibraryBreakdownDetail(LoginRequiredMixin, generic.DetailView):
    model = LibraryBreakdown
    context_object_name = 'library_breakdown'
    template_name = 'breakdowns/library_breakdown_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(LibraryBreakdownDetail, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'library'
        context['subpage_name'] = self.object.standard_library.full_title
        return context

# All My Cost breakdowns list
class MyBreakdownList(LoginRequiredMixin, generic.ListView):
    model = CostBreakdown
    template_name = 'breakdowns/my_breakdown_list.html'
    context_object_name = 'cost_breakdown_list'
    login_url = 'breakdowns:my_breakdown_list'
    redirect_field_name = None

    def test_func(self, *args, **kwargs):
        cost_breakdown = CostBreakdown.objects.get(pk=self.kwargs['pk'])
        return cost_breakdown.created_by.id == self.request.user.id

    def get_queryset(self, *args, **kwargs):
        return CostBreakdown.objects.filter(created_by__pk=self.request.user.id)

    def get_context_data(self, *args, **kwargs):
        context = super(MyBreakdownList, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'my cost breakdowns'
        return context

# My Cost Breakdowns Detail
class MyBreakdownDetail(UserPassesTestMixin, generic.DetailView):
    model = CostBreakdown
    template_name = 'breakdowns/my_breakdown_detail.html'
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
                excel_template_path = settings.MEDIA_ROOT + 'blank_template_sm_2.xls'
            elif row_count > 14 and row_count <= 18:
                pass
            else:
                pass
            
            rb = open_workbook(excel_template_path, formatting_info=True)
            wb = copy(rb)
            ws = wb.get_sheet(0)
            
            style_default = easyxf('font: name Courier New, height 180;')
            style_default_center_bold = easyxf('font: name Courier New, height 180, bold on; align: horiz center')
            style_left = easyxf('font: name Courier New, height 180; borders: left thin, right thin, top thin, bottom thin; align: horiz left;')
            style_center = easyxf('font: name Courier New, height 180; borders: left thin, right thin, top thin, bottom thin; align: horiz center;')
            style_right = easyxf('font: name Courier New, height 180; borders: left thin, right thin, top thin, bottom thin; align: horiz right;')
            style_left_bold = easyxf('font: name Courier New, height 180; borders: left thin, right thin, top thin, bottom thin; align: horiz left; font: bold on;')
            style_center_bold = easyxf('font: name Courier New, height 180, bold on; borders: left thin, right thin, top thin, bottom thin; align: horiz center;')
            style_right_bold = easyxf('font: name Courier New, height 180, bold on; borders: left thin, right thin, top thin, bottom thin; align: horiz right;')
            style_center_shade = easyxf('font: name Courier New, height 180; borders: left thin, right thin, top thin, bottom thin; align: horiz center; pattern: pattern solid, fore_colour yellow;')
            style_percent = easyxf(num_format_str='0.00%')

            # Add General breakdown data to excel
            ws.write(0, 3, self.object.project.full_title, style_default)
            ws.write(1, 3, self.object.project.client, style_default)
            ws.write(2, 3, self.object.project.consultant, style_default)
            ws.write(3, 3, self.object.project.contractor, style_default)
            ws.write(5, 3, self.object.full_title, style_default)
            ws.write(0, 15, self.object.project.city, style_center_shade)
            # ws.write(1, 15, self.object.created_at, style_center_shade)
            ws.write(39, 2, self.request.user.get_full_name(), style_default)
            ws.write(35, 16, self.object.overhead/100, style_percent)
            ws.write(36, 16, self.object.profit/100, style_percent)
            ws.write(37, 16, self.object.unit.short_title, style_default_center_bold)

            # Add Material Breakdown data to excel
            if len(material_list) > 0:
                mb_row_count = 12 # Material Excel Row Starts at 7 row

                for i, mb in enumerate(material_list, start=1):
                    ws.write(mb_row_count, 0, i, style_center)
                    ws.write(mb_row_count, 1, mb.material.full_title, style_left)
                    ws.write(mb_row_count, 2, mb.unit.short_title, style_center)
                    ws.write(mb_row_count, 3, mb.quantity, style_right)
                    ws.write(mb_row_count, 4, mb.rate, style_right)
                    ws.write(mb_row_count, 5, Formula("D{}*E{}".format(mb_row_count + 1, mb_row_count + 1)), style_right)
                    mb_row_count += 1

                # Material Subtotal
                ws.write(28, 5, Formula("SUM(F13:F26)"), style_right)
                ws.write(32, 5, Formula("F29"), style_right)

            # Add Labour Breakdown data to excel
            if len(labour_list) > 0:
                lb_row_count = 12 # Labour Excel Row Starts at 7 row
                ws.write(31, 11, self.object.output, style_right)

                for i, lb in enumerate(labour_list, start=1):
                    ws.write(lb_row_count, 7, lb.labour.full_title, style_left)
                    ws.write(lb_row_count, 8, lb.number, style_center)
                    ws.write(lb_row_count, 9, lb.uf, style_center)
                    ws.write(lb_row_count, 10, lb.hourly_rate, style_right)
                    ws.write(lb_row_count, 11, Formula("I{}*J{}*K{}".format(lb_row_count + 1, lb_row_count + 1, lb_row_count + 1)), style_right)
                    lb_row_count += 1

                # Labour Subtotal
                ws.write(28, 11, Formula("ROUND(SUM(L13:L26),2)"), style_right)
                ws.write(32, 11, Formula("L29/L32"), style_right)
            else:
                # Labour Subtotal
                ws.write(32, 11, 0.0, style_right)

            # Add Equipement Breakdown data to excel
            if len(equipment_list) > 0:
                eb_row_count = 12 # Equipement Excel Row Starts at 7 row
                ws.write(31, 17, self.object.output, style_right)

                for i, eb in enumerate(equipment_list, start=1):
                    ws.write(eb_row_count, 13, eb.equipment.full_title, style_left)
                    ws.write(eb_row_count, 14, eb.number, style_center)
                    ws.write(eb_row_count, 15, eb.uf, style_center)
                    ws.write(eb_row_count, 16, eb.rental_rate, style_right)
                    ws.write(eb_row_count, 17, Formula("O{}*P{}*Q{}".format(eb_row_count + 1, eb_row_count + 1, eb_row_count + 1)), style_right)
                    eb_row_count += 1

                # Equipment Subtotal
                ws.write(28, 17, Formula("ROUND(SUM(R13:R26),2)"), style_right)
                ws.write(32, 17, Formula("R29/R32"), style_right)
            else:
                # Equipment Subtotal
                ws.write(32, 17, 0.0, style_right)

            # Direct Cost
            ws.write(34, 17, Formula("SUM(F33+L33+R33)"), style_right)

            # Overhead Cost
            ws.write(35, 17, Formula("ROUND(R35*Q36, 2)"), style_right)

            # Profit Cost
            ws.write(36, 17, Formula("ROUND(R35*Q37,2)"), style_right)

            # Total Cost
            ws.write(37, 17, Formula("SUM(R35+R36+R37)"), style_right_bold)

            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=cost_breakdown_{}.xls'.format(self.object.id)

            wb.save(response)
            return response
        return super(MyBreakdownDetail, self).get(*args, **kwargs)
    def get_context_data(self, *args, **kwargs):
        context = super(MyBreakdownDetail, self).get_context_data(*args, **kwargs)         
        context['page_name'] = 'my cost breakdowns'
        return context

# Create a cost breakdown from library
def breakdown_create(request):
    if request.method == 'POST':
        pass
    else:
        if request.GET.get('m') == 'library':
            step = int(request.GET.get('step', 1))
            template_name = 'breakdowns/breakdown_create.html'
            context = {}

            if step == 1:
                context['library_list'] = StandardLibrary.objects.all()
                context['form_html'] = 'breakdowns/partials/breakdown_create_step1.html'
            elif step == 2:
                library = int(request.GET.get('library'))
                context['library_breakdown_list'] = LibraryBreakdown.objects.filter(standard_library=library)
                context['form_html'] = 'breakdowns/partials/breakdown_create_step2.html'
            else:
                pass
        else: # Blank
            pass
    return render(request, template_name, context)


# OLD CODE - Create a new cost breakdown - Step 1
@login_required
def step_one(request):
    form_class = StepOneForm
    step_1_template = 'breakdowns/breakdown_form_step_1.html'
    step_2_template = 'breakdowns/breakdown_form_step_2.html'

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            option = int(form.cleaned_data['options'])
            if option == 0:
                request.session['library_breakdown'] = CostBreakdown.objects.get(pk=form.cleaned_data['breakdown'].id).id
            else:
                request.session['library_breakdown'] = None
            return redirect('breakdowns:breakdown_create_step_2')
    else:
        request.session['library_breakdown'] = None
        form = form_class()

    return render(request, step_1_template, {
            'form': form,
        })

# Create a new cost breakdown - Step 2
@login_required
def step_two(request):
    form_class = StepTwoForm
    template_name = 'breakdowns/breakdown_form_step_2.html'
    catagory_list = CostBreakdownCatagory.objects.all()
    #unit_list = Unit.objects.all()
    unit_catagory_list = UnitCatagory.objects.all()
    project_list = Project.objects.filter(created_by = request.user.id)

    if request.session.get('library_breakdown') is not None:
        library_breakdown = CostBreakdown.objects.get(pk=request.session.get('library_breakdown'))
    elif request.GET.get('library_breakdown') is not None:
        library_breakdown = CostBreakdown.objects.get(pk=int(request.GET.get('library_breakdown')))
    else:
        library_breakdown = None

    if request.method == 'POST': 
        form = form_class(request.POST)
        if form.is_valid():
            cb = form.save(commit=False)
            cb.created_by = request.user
            cb.save()
            
            # If cost_breakdown is duplicated from the library
            if library_breakdown is not None:
                mb_list = MaterialBreakdown.objects.filter(costbreakdown = library_breakdown.id)
                lb_list = LabourBreakdown.objects.filter(costbreakdown = library_breakdown.id)
                eb_list = EquipmentBreakdown.objects.filter(costbreakdown = library_breakdown.id)

                for mb in mb_list:
                    mb.costbreakdown = cb
                    mb.pk = None
                    mb.save()

                for lb in lb_list:
                    lb.costbreakdown = cb
                    lb.pk = None
                    lb.save()

                for eb in eb_list:
                    eb.costbreakdown = cb
                    eb.pk = None
                    eb.save()
            # Destroy session data        
            request.session.library_breakdown = None

            # Redirect to newly created cost breakdown
            return redirect(reverse('breakdowns:my_breakdown_detail', kwargs={'pk': cb.id}))           
    else:
        form = form_class()
    return render(request, template_name, {
            'form': form,
            'catagory_list': catagory_list,
            'unit_catagory_list': unit_catagory_list,
            'library_breakdown': library_breakdown,
            'project_list': project_list,
        })

# Update an Existing Breakdown
class BreakdownUpdate(LoginRequiredMixin, UpdateView):
    """
    Update existing cost breakdown
    """
    model = CostBreakdown
    fields = ['activity_catagory', 'project', 'full_title', 'description', 'unit', 'output', 'overhead', 'profit',]
    template_name = 'breakdowns/breakdown_form_update.html'

    def get_success_url(self, *args, **kwargs):
        return reverse('breakdowns:my_breakdown_detail', kwargs={'pk': self.object.id})

    def get_context_data(self, *args, **kwargs):
        context = super(BreakdownUpdate, self).get_context_data(*args, **kwargs)
        context['project_list'] = Project.objects.filter(created_by=self.request.user.id)
        context['catagory_list'] = CostBreakdownCatagory.objects.all()
        context['unit_catagory_list'] = UnitCatagory.objects.all()
        context['page_name'] = 'mybreakdowns'
        return context

# Delete an Existing Breakdown
class BreakdownDelete(LoginRequiredMixin, DeleteView):
    """
    Delete an existing cost breakdown
    """
    model = CostBreakdown
    template_name = 'breakdowns/breakdown_confirm_delete.html'

    def get_success_url(self, *args, **kwargs):
        if self.object.is_library:
            return reverse('breakdowns:cost_breakdown_list')
        return reverse('breakdowns:my_breakdown_list')

# Create a new cost breakdown view
class BreakdownCreate(LoginRequiredMixin, CreateView):
    """
    Create a new cost breakdown with the current user as it's owner
    """
    model = CostBreakdown
    template_name = 'breakdowns/breakdown_form.html'
    fields = ['activity_catagory', 'project', 'full_title', 'description', 'unit', 'output', 'overhead', 'profit',]

    def form_valid(self, form, *args, **kwargs):
        form.instance.created_by = self.request.user
        return super(BreakdownCreate, self).form_valid(form, *args, **kwargs)

    def get_success_url(self, *args, **kwargs):
        return reverse('breakdowns:my_breakdown_detail', kwargs={'pk': self.object.id})

    def get_context_data(self, *args, **kwargs):
        context = super(BreakdownCreate, self).get_context_data(*args, **kwargs)
        context['project_list'] = Project.objects.filter(created_by=self.request.user.id)
        context['catagory_list'] = CostBreakdownCatagory.objects.all()
        context['unit_list'] = Unit.objects.all()
        context['subpage_name'] = 'My Breakdowns'
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
        context['page_name'] = 'my cost breakdowns'
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
    template_name = 'breakdowns/my_breakdown_detail.html'
    login_url = 'breakdowns:my_breakdown_list'
    redirect_field_name = None

    def test_func(self, *args, **kwargs):
        cost_breakdown = CostBreakdown.objects.get(pk=self.kwargs['breakdown_pk'])
        material_breakdown = MaterialBreakdown.objects.get(pk=self.kwargs['pk'])
        return material_breakdown.costbreakdown.id == cost_breakdown.id

    def get_success_url(self, *args, **kwargs):
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
        return context

# Delete A Material Breakdown 
class LabourBreakdownDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = LabourBreakdown
    template_name = 'breakdowns/my_breakdown_detail.html'
    login_url = 'breakdowns:my_breakdown_list'
    redirect_field_name = None

    def test_func(self, *args, **kwargs):
        cost_breakdown = CostBreakdown.objects.get(pk=self.kwargs['breakdown_pk'])
        labour_breakdown = LabourBreakdown.objects.get(pk=self.kwargs['pk'])
        return labour_breakdown.costbreakdown.id == cost_breakdown.id

    def get_success_url(self, *args, **kwargs):
        return reverse('breakdowns:my_breakdown_detail', kwargs={'pk': self.kwargs['breakdown_pk']})

    def get_context_data(self, *args, **kwargs):
        context = super(LabourBreakdownDelete, self).get_context_data(*args, **kwargs)
        context['cost_breakdown'] = CostBreakdown.objects.get(pk=self.kwargs['breakdown_pk'])
        context['labour_breakdown'] = LabourBreakdown.objects.get(pk=self.kwargs['pk'])
        context['page_name'] = 'CostBreakdowns'
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
        return context

class EquipmentBreakdownDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = EquipmentBreakdown
    template_name = 'breakdowns/my_breakdown_detail.html'
    login_url = 'breakdowns:my_breakdown_list'
    redirect_field_name = None

    def test_func(self, *args, **kwargs):
        cost_breakdown = CostBreakdown.objects.get(pk=self.kwargs['breakdown_pk'])
        equipment_breakdown = EquipmentBreakdown.objects.get(pk=self.kwargs['pk'])
        return equipment_breakdown.costbreakdown.id == cost_breakdown.id

    def get_success_url(self, *args, **kwargs):
        return reverse('breakdowns:my_breakdown_detail', kwargs={'pk': self.kwargs['breakdown_pk']})

    def get_context_data(self, *args, **kwargs):
        context = super(EquipmentBreakdownDelete, self).get_context_data(*args, **kwargs)
        context['cost_breakdown'] = CostBreakdown.objects.get(pk=self.kwargs['breakdown_pk'])
        context['equipment_breakdown'] = EquipmentBreakdown.objects.get(pk=self.kwargs['pk'])
        context['page_name'] = 'CostBreakdowns'
        return context