from tests.pages.resource_page import ResourcePage


class LabelsPage(ResourcePage):
    route = "labels"
    title_text = "Labels"
    empty_text = "No Labels yet."
    form_fields = ("name",)
