from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse

from .models import Portfolio, PortfolioCategory
from .forms import PortfolioForm
from .cloudinary_utils import delete_image

@login_required
def portfolio_list(request):
    portfolios = Portfolio.objects.all().order_by('-created_at')
    categories = PortfolioCategory.objects.all()
    
    context = {
        'portfolios': portfolios,
        'categories': categories,
        'title': 'Portfolio Management'
    }
    
    return render(request, 'admin/portfolio_list.html', context)

@login_required
def portfolio_create(request):
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES)
        if form.is_valid():
            portfolio = form.save()
            messages.success(request, f'Portfolio "{portfolio.title}" created successfully!')
            return redirect('admin_portfolio_list')
    else:
        form = PortfolioForm()
    
    context = {
        'form': form,
        'title': 'Create Portfolio Item',
        'is_create': True
    }
    
    return render(request, 'admin/portfolio_form.html', context)

@login_required
def portfolio_edit(request, pk):
    portfolio = get_object_or_404(Portfolio, pk=pk)
    
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES, instance=portfolio)
        if form.is_valid():
            portfolio = form.save()
            messages.success(request, f'Portfolio "{portfolio.title}" updated successfully!')
            return redirect('admin_portfolio_list')
    else:
        form = PortfolioForm(instance=portfolio)
    
    context = {
        'form': form,
        'portfolio': portfolio,
        'title': f'Edit Portfolio: {portfolio.title}',
        'is_create': False
    }
    
    return render(request, 'admin/portfolio_form.html', context)

@login_required
def portfolio_delete(request, pk):
    portfolio = get_object_or_404(Portfolio, pk=pk)
    
    if request.method == 'POST':
        # Delete the Cloudinary image if it exists
        if portfolio.cloudinary_image_id:
            try:
                delete_image(portfolio.cloudinary_image_id)
            except Exception as e:
                messages.warning(request, f'Error deleting image from Cloudinary: {str(e)}')
        
        portfolio_title = portfolio.title
        portfolio.delete()
        messages.success(request, f'Portfolio "{portfolio_title}" deleted successfully!')
        return redirect('admin_portfolio_list')
    
    context = {
        'portfolio': portfolio,
        'title': f'Delete Portfolio: {portfolio.title}'
    }
    
    return render(request, 'admin/portfolio_confirm_delete.html', context)

@login_required
def portfolio_category_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        slug = request.POST.get('slug')
        
        if not name:
            return JsonResponse({'success': False, 'error': 'Category name is required'}, status=400)
        
        category = PortfolioCategory.objects.create(name=name, slug=slug)
        
        return JsonResponse({
            'success': True, 
            'category': {
                'id': category.id,
                'name': category.name,
                'slug': category.slug
            }
        })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)