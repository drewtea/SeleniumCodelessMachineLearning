class SearchElement(object):
  # Attributes for search element
  def __init__(self, url, name, placeholder,class_, id, autocomplete, aria_label, 
                autocapitalize, spellcheck, aria_autocomplete, tabindex, 
                role, autofocus, aria_haspopup, accesskey, aria_controls):
        self.url = url
        self.name = name
        self.placeholder = placeholder
        self.class_ = class_
        self.id = id
        self.aria_label = aria_label
        self.tabindex = tabindex
        self.role = role
        self.accesskey = accesskey
        self.aria_control = aria_controls