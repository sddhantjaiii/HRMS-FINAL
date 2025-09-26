from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from excel_data.models import Tenant

User = get_user_model()

class Command(BaseCommand):
    help = 'Setup a default tenant for production deployment'

    def handle(self, *args, **options):
        # Create default tenant
        tenant, created = Tenant.objects.get_or_create(
            subdomain='default',
            defaults={
                'name': 'Default Company',
                'is_active': True
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS('Created default tenant: Default Company'))
        else:
            self.stdout.write(self.style.WARNING('Default tenant already exists'))

        # Create default admin user if it doesn't exist
        admin_email = 'admin@company.com'  # You can change this
        user, user_created = User.objects.get_or_create(
            email=admin_email,
            tenant=tenant,
            defaults={
                'first_name': 'Admin',
                'last_name': 'User',
                'role': 'admin',
                'is_tenant_admin': True,
                'is_hr': True,
                'is_active': True,
                'email_verified': True
            }
        )

        if user_created:
            user.set_password('admin123')  # Change this password
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Created admin user: {admin_email} with password: admin123'))
        else:
            self.stdout.write(self.style.WARNING(f'Admin user already exists: {admin_email}'))

        self.stdout.write(self.style.SUCCESS(f'Default tenant setup complete:'))
        self.stdout.write(f'  Tenant: {tenant.name} (subdomain: {tenant.subdomain})')
        self.stdout.write(f'  Admin: {admin_email} / admin123')