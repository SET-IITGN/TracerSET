from enum import Enum

class UserRole(Enum):
    # Members assigned a tuple of values
    ADMIN = ("Administrator", "Full system access")
    EDITOR = ("Content Editor", "Can modify content")
    VIEWER = ("Viewer", "Read-only access")

    def __init__(self, title, description):
        self.title = title
        self.description = description

# Accessing the custom attributes
print(UserRole.ADMIN.title)       # Output: Administrator
print(UserRole.ADMIN.description) # Output: Full system access

