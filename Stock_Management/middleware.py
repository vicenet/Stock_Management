from django.shortcuts import redirect
from django.urls import reverse

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the URL paths for the login page and password reset views
        login_page_url = reverse('shop:loginPage')
        password_reset_url = reverse('shop:password_reset')
        password_reset_done_url = reverse('shop:password_reset_done')
        password_reset_confirm_url = reverse('shop:password_reset_confirm', args=[1, 'token'])
        # password_reset_complete_url = reverse('shop:password_reset_complete')

        # Check if the user is authenticated
        if not request.user.is_authenticated:
            # Allow access to the login page, password reset views, and password_reset_done view
            if request.path not in [login_page_url, password_reset_url, password_reset_done_url, password_reset_confirm_url,]:
                return redirect(login_page_url)

        # Redirect to the home page after successful login
        elif request.user.is_authenticated and request.path == login_page_url:
            return redirect('shop:home')  # Replace 'home' with the desired URL for the home/dashboard page

        return self.get_response(request)
