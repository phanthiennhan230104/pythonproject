from django.shortcuts import render

# Create your views here.
def account_view(request):
    return render(request, 'admin_homepage/admin_manage_account.html')

def permission_view(request):
    return render(request, 'admin_homepage/admin_permission.html')

def list_of_account_view(request):
    return render(request, 'admin_homepage/admin_list_account.html')