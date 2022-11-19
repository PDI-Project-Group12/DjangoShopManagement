from django.contrib import admin

# Register your models here.

from DjangoShopApp.models import Company, Product, ProductDetails, Employee, Customer, Bill, EmployeeSalary, BillDetails, CustomerRequest, CompanyAccount, CompanyBank, EmployeeBank

admin.site.register(Company)
admin.site.register(Product)
admin.site.register(ProductDetails)
admin.site.register(Employee)
admin.site.register(Customer)
admin.site.register(Bill)
admin.site.register(EmployeeSalary)
admin.site.register(BillDetails)
admin.site.register(CustomerRequest)
admin.site.register(CompanyAccount)
admin.site.register(CompanyBank)
admin.site.register(EmployeeBank)
