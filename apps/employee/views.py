from django.db.models import F
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Employee, Position


class EmployeeListView(ListView):
    model = Employee
    # Руководство идёт первым по порядковому номеру, остальные — по фамилии
    queryset = model.active.select_related('position').order_by(F('number').asc(nulls_last=True), 'last_name')
    context_object_name = 'employees'
    template_name = 'employee/index.html'


class EmployeeDetailView(DetailView):
    model = Employee
    queryset = model.active.select_related('position')
    slug_field = 'slug'
    context_object_name = 'employee'
    template_name = 'employee/employee_detail.html'
