from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Project(models.Model):
    """
    Model represents a construction project
    """
    full_title = models.CharField(max_length=120, help_text='The full official project title')
    short_title = models.CharField(max_length=60, null=True, blank=True)
    contractor = models.CharField(max_length=120)
    consultant = models.CharField(max_length=120)
    client = models.CharField(max_length=120)
    city = models.CharField(max_length=60)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateField(auto_now=True)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['full_title']

    def get_absolute_url(self):
        """
        Returns a particular Project model instance
        """
        return reverse('breakdowns:project_detail', kwargs={'pk': str(self.pk)})

    def __str__(self):
        """
        Returns string representation of the project model
        """
        return self.full_title

class UnitCatagory(models.Model):
    """
    Model representing catagory of measurement units
    Example: length, mass, area, volume
    """
    full_title = models.CharField(max_length=60)
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['full_title']

    def __str__(self):
        """
        Returns string representation of unit catagory model
        """
        return self.full_title

class Unit(models.Model):
    """
    Model representing material measurement units
    Example: Kg, m, litre, m2, m3, ml, quital etc
    """
    catagory = models.ForeignKey(UnitCatagory, on_delete=models.CASCADE, help_text='Type of measurement units')
    full_title = models.CharField(max_length=60)
    short_title = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        ordering = ['full_title']

    def __str__(self):
        """
        Returns string representation of the Unit model
        """
        return self.full_title

class MaterialCatagory(models.Model):
    """
    Model Representing a material type catagory
    Example: Finishing Material, Structural Materials, RHS etc...
    """
    full_title = models.CharField(max_length=120, help_text='Material type catagory')
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['full_title']
        verbose_name_plural = 'Material Catagories'

    def __str__(self):
        """
        Return a string repsentation of the MaterialCatagory model
        """
        return self.full_title

class Material(models.Model):
    """
    Model representing a construction material
    """
    material_catagory = models.ForeignKey(MaterialCatagory, null=True, on_delete=models.SET_NULL)
    full_title = models.CharField(max_length=120)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, default=0, help_text='Current market unit rate of material')
    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateField(auto_now=True)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['full_title', '-rate', '-updated_at']

    def get_absolute_url(self):
        """
        Returns a particular material instance
        """
        return reverse('breakdown:material_detail', kwargs={'pk': str(self.pk)})

    def __str__(self):
        """
        Returns string representation of the Material model
        """
        return self.full_title

class MaterialSupplier(models.Model):
    """
    Model representing a material supplier company
    """
    full_title = models.CharField(max_length=120, help_text='Material Supplier Company name')
    short_title = models.CharField(max_length=30, null=True, blank=True, help_text='Material Supplier short(unofficial) name')
    description = models.TextField(null=True, blank=True,help_text='Short summary about the supplier')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['full_title']

    def __str__(self):
        """
        Returns string representation of the Material supplier model
        """
        return self.full_title

class MaterialPrice(models.Model):
    """
    Model represents material rate per a particular supplier
    """
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    supplier = models.ForeignKey(MaterialSupplier, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, help_text="Supplier's current material price(Before TAX)")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateField(auto_now=True)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['material', '-price']

    def __str__(self):
        """
        Returns string representation of the Material price model
        """
        return 'Material: {}, Supplier: {}, Price: {}'.format(self.material.full_title, self.supplier.full_title, self.price)

class LabourCatagory(models.Model):
    """
    Model Representing a labour type catagory
    Example: 
    """
    full_title = models.CharField(max_length=120, help_text='Labour type catagory')
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['full_title']
        verbose_name_plural = 'Labour Catagories'

    def __str__(self):
        """
        Return a string repsentation of the LabourCatagory model
        """
        return self.full_title

class Labour(models.Model):
    """
    Model representing a labour trade
    """
    labour_catagory = models.ForeignKey(LabourCatagory, null=True, on_delete=models.SET_NULL)
    full_title = models.CharField(max_length=120)
    short_title = models.CharField(max_length=30, null=True, blank=True)
    hourly_rate = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, default=0, help_text='Current hourly rate')
    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateField(auto_now=True)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['full_title', '-hourly_rate', '-updated_at']

    def get_absolute_url(self):
        """
        Returns a particular labour instance
        """
        return reverse('breakdown:labour_detail', kwargs={'pk': str(self.pk)})

    def __str__(self):
        """
        Returns string representation of the Labour model
        """
        return self.full_title

class EquipmentCatagory(models.Model):
    """
    Model Representing a equipment type catagory
    Example: 
    """
    full_title = models.CharField(max_length=120, help_text='Equipment type catagory')
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['full_title']
        verbose_name_plural = 'Equipment Catagories'

    def __str__(self):
        """
        Return a string repsentation of the EquipmentCatagory model
        """
        return self.full_title


class Equipment(models.Model):
    """
    Model representing a construction Equipment
    """
    equipment_catagory = models.ForeignKey(EquipmentCatagory, null=True, on_delete=models.SET_NULL)
    full_title = models.CharField(max_length=120)
    short_title = models.CharField(max_length=30, null=True, blank=True)
    rental_rate = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, default=0, help_text='Current rental rate')
    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateField(auto_now=True)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['full_title', '-rental_rate', '-updated_at']

    def get_absolute_url(self):
        """
        Returns a particular equipment instance
        """
        return reverse('breakdown:equipment_detail', kwargs={'pk': str(self.pk)})

    def __str__(self):
        """
        Returns string representation of the Equipment model
        """
        return self.full_title

class CostBreakdownCatagory(models.Model):
    """
    Model Representing a cost breakdown work type catagory
    Example: 
    """
    full_title = models.CharField(max_length=120, help_text='Work type catagory for breakdown')
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['full_title']
        verbose_name_plural = 'Cost Breakdown Catagories'

    def __str__(self):
        """
        Return a string repsentation of the BreakdownCatagory model
        """
        return self.full_title


class CostBreakdown(models.Model):
    """
    Model representing the a cost breakdown
    """
    cost_breakdown_catagory = models.ForeignKey(CostBreakdownCatagory, null=True, on_delete=models.SET_NULL)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    full_title = models.CharField(max_length=120, help_text='Work Item Title')
    description = models.TextField(null=True, blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, help_text='Measurement unit for the cost breakdown')
    overhead = models.DecimalField(null=True, blank=True, max_digits=6, decimal_places=2, help_text='Overhead percentage in decimal number. Example: 0.15 for 15%')
    profit = models.DecimalField(null=True, blank=True, max_digits=6, decimal_places=2, help_text='Profit percentage in decimal number. Example: 0.2 for 20%')
    output = models.DecimalField(max_digits=3, decimal_places=2, help_text='Labour and equipment output')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateField(auto_now=True)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'cost breakdown'
        verbose_name_plural = 'cost breakdowns'
        ordering = ['project', 'full_title']
        permissions = (
                ('download_cost_breakdown', 'Can download cost breakdown in excel and pdf'),
                ('manage_cost_breakdown', 'Can manage own cost breakdown'),
                ('manage_library', 'Can manage standard cost breakdown library'),
            )

    @property 
    def is_library(self):
        """
        Return True if cost breakdown is created by a staff user. 
        Return False if not
        """
        if self.created_by.is_staff:
            return True
        return False

    def get_absolute_url(self):
        """
        Returns a particular instance of costbreakdown
        """
        return reverse('breakdowns:my_breakdown_detail', kwargs={'pk': str(self.pk)})

    def __str__(self):
        """
        Returns string repsentation of the CostBreakdown model
        """
        return self.full_title

class MaterialBreakdown(models.Model):
    """
    Model representing a material breakdown
    """
    costbreakdown = models.ForeignKey(CostBreakdown, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=12, decimal_places=2, default=1)
    rate = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    updated_at = models.DateField(auto_now=True)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
       verbose_name = 'material breakdown'
       verbose_name_plural = 'material breakdowns'
       ordering = ['costbreakdown', 'material', '-rate'] 

    def subtotal(self):
        """
        Returns subtotal of a single material direct cost
        """
        if self.rate is None:
            return round(self.quantity * self.material.rate, 2)
        return round(self.quantity * self.rate, 2)

    def get_absolute_url(self):
        """
        Returns a particular instance of materialbreakdown
        """
        return reverse('breakdowns:materialbreakdown_detail', kwargs={'pk': str(self.pk)})

    def __str__(self):
        """
        Returns string repsentation of the MaterialBreakdown model
        """
        return '{} Material Breakdown'.format(self.material.full_title)

class LabourBreakdown(models.Model):
    """
    Model representing a labour breakdown
    """
    costbreakdown = models.ForeignKey(CostBreakdown, on_delete=models.CASCADE)
    labour = models.ForeignKey(Labour, on_delete=models.CASCADE)
    number = models.IntegerField(default=1)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2)
    uf = models.DecimalField(max_digits=3, decimal_places=2, default=1)
    updated_at = models.DateField(auto_now=True)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
       verbose_name = 'labour breakdown'
       verbose_name_plural = 'labour breakdowns'
       ordering = ['costbreakdown', 'labour', '-hourly_rate'] 

    def subtotal(self):
        """ 
        Return labour direct cost total (after output)
        """
        output = self.costbreakdown.output

        if self.hourly_rate is None:
            return round(self.number, self.labour.hourly_rate * self.uf / output, 2)
        return round(self.number * self.hourly_rate * self.uf / output, 2)

    def get_absolute_url(self):
        """
        Returns a particular instance of labourbreakdown
        """
        return reverse('breakdowns:labourbreakdown_detail', kwargs={'pk': str(self.pk)})

    def __str__(self):
        """
        Returns string repsentation of the LabourBreakdown model
        """
        return '{} Labour Breakdown'.format(self.labour.full_title)

class EquipmentBreakdown(models.Model):
    """
    Model representing a equipment breakdown
    """
    costbreakdown = models.ForeignKey(CostBreakdown, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    number = models.IntegerField(default=1)
    rental_rate = models.DecimalField(max_digits=8, decimal_places=2, help_text='Equipment hourly rental rate')
    uf = models.DecimalField(max_digits=3, decimal_places=2, default=1)
    updated_at = models.DateField(auto_now=True)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
       verbose_name = 'equipment breakdown'
       verbose_name_plural = 'equipment breakdowns'
       ordering = ['costbreakdown', 'equipment', '-rental_rate']

    def subtotal(self):
        """ 
        Return equipment direct cost total (after output)
        """
        output = self.costbreakdown.output

        if self.rental_rate is None:
            return round(self.number * self.equipmentr.ental_rate * self.uf / output, 2)
        return round(self.number * self.rental_rate * self.uf / output, 2)

    def get_absolute_url(self):
        """
        Returns a particular instance of equipmentbreakdown
        """
        return reverse('breakdowns:equipmentbreakdown_detail', kwargs={'pk': str(self.pk)})

    def __str__(self):
        """
        Returns string repsentation of the EquipmentBreakdown model
        """
        return '{} Equipment Breakdown'.format(self.equipment.full_title)

