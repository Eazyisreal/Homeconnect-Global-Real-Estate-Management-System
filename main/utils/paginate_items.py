from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def paginate_items(request, items, items_per_page):
    """
    Paginates a list of items based on the request and number of items per page.

    Args:
    - request: Django HttpRequest object.
    - items: QuerySet or list of items to paginate.
    - items_per_page: Number of items to display per page.

    Returns:
    - Paginated items (Page object).
    """
    paginator = Paginator(items, items_per_page)
    page_number = request.GET.get('page')

    try:
        paginated_items = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_items = paginator.page(1)
    except EmptyPage:
        paginated_items = paginator.page(paginator.num_pages)
    return paginated_items