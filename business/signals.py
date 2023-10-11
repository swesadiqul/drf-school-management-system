# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth import get_user_model
# from business.models import Business
# from guardian.shortcuts import assign_perm

# User = get_user_model()


# @receiver(post_save, sender=Business)
# def create_user_for_business(sender, instance, created, **kwargs):
#     if created:
#         # Create a user associated with the newly created business
#         user = User.objects.create(
#             email=f"{instance.email}",
#             username=f"{instance.name.lower()}{instance.id}".replace(" ", ""),
#             business=instance,
#             is_active=True,
#             is_staff=True,
#             is_business_admin=True,
#             is_superuser=False,
#             is_create_branch= instance.has_branch,
#             branch_limit=instance.branch_num
#         )

#         # Set the user's password using set_password to ensure it's hashed
#         user.set_password("use-!@#-123")
#         user.save()

#         # Assign permissions for the user on the specific business
#         assign_perm("add_business", user, instance)
#         assign_perm("view_business", user, instance)
#         assign_perm("change_business", user, instance)
#         assign_perm("delete_business", user, instance)

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from business.models import Business
from guardian.shortcuts import assign_perm

User = get_user_model()


@receiver(post_save, sender=Business)
def create_user_for_business(sender, instance, created, **kwargs):
    if created:
        # Check if it's a branch
        if instance.parent_business:
            is_business_admin = False
            is_branch_admin = True
            is_create_branch = False
            branch_limit = None
        else:
            is_business_admin = True
            is_branch_admin = False
            is_create_branch = True
            branch_limit = instance.branch_num

        # Create a user associated with the newly created business
        user = User.objects.create(
            email=f"{instance.email}",
            username=f"{instance.name.lower()}{instance.id}".replace(" ", ""),
            business=instance,
            is_active=True,
            is_staff=True,
            is_business_admin=is_business_admin,
            is_branch_admin=is_branch_admin,
            is_create_branch=is_create_branch,
            branch_limit=branch_limit
        )

        # Set the user's password using set_password to ensure it's hashed
        user.set_password("use-!@#-123")
        user.save()
