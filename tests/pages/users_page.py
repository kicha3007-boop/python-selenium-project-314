from tests.pages.resource_page import ResourcePage


class UsersPage(ResourcePage):
    route = "users"
    title_text = "Users"
    empty_text = "No Users yet."
    form_fields = ("email", "firstName", "lastName")
