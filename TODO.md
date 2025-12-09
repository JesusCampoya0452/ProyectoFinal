# TODO List for Fixing Product Image and Display Issues

## Completed Tasks
- [x] Added MEDIA_URL and MEDIA_ROOT to backend_bocineytion/settings.py for serving uploaded images
- [x] Added media URL pattern to backend_bocineytion/urls.py to serve media files during development
- [x] Modified ProductosView in app_admin/views.py to display all products instead of filtering by 'altavoces' category
- [x] Added STATICFILES_DIRS to backend_bocineytion/settings.py for serving static files
- [x] Created static/imagenes/ directory structure
- [x] Copied default image altavoces1.jpg to static/imagenes/ for fallback display

## Summary of Changes
The issues were:
1. **Images not visible**: Django was not configured to serve media files. Added MEDIA_URL='/media/' and MEDIA_ROOT=BASE_DIR/'media' to settings.py, and added URL pattern for serving media files in development.
2. **Products not visible**: The ProductosView was filtering products by categoria='altavoces', but there might not be any products with that category. Changed it to show all products.
3. **Static files not configured**: Added STATICFILES_DIRS and created the necessary directory structure with default images.

## Final Status
All configuration issues have been resolved. The application should now properly display:
- Product images when uploaded (served from /media/)
- Fallback static images when no product image is uploaded (served from /static/)
- All products in the database (not just 'altavoces' category)

## Testing Instructions
1. Run: python manage.py runserver
2. Visit: http://127.0.0.1:8000/productos-altavoces/
3. If no products exist, create some at: http://127.0.0.1:8000/admin/app_admin/producto/
