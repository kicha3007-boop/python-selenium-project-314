from tests.pages.resource_page import ResourcePage


class StatusesPage(ResourcePage):
    route = "task_statuses"
    title_text = "Task statuses"
    empty_text = "No Task statuses yet."
    form_fields = ("name", "slug")
