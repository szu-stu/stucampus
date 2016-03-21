from .models import Article




def nav_column(request):
	nav_display_columns = Article.objects.filter(publish=True, deleted=False).order_by('-pk')[:4]
	return	{'nav_display_columns': nav_display_columns}