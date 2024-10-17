from django.core.management.base import BaseCommand
from wall.models import WallProfile


class Command(BaseCommand):
    help = ('Loads wall profiles from a configuration file. Each row in the file has random number'
            'of space separated numbers representing sections and their height of a wall profile.')

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the configuration file.')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        try:
            with open(file_path, 'r') as file:
                for line_number, line in enumerate(file, start=1):
                    heights = line.strip().split()

                    # Check if all values are integers
                    try:
                        heights = list(map(int, heights))
                    except ValueError:
                        self.stdout.write(
                            self.style.ERROR(f'Invalid data at line {line_number}. All values must be integers.'))
                        continue

                    # Check if all values are in the valid range [0, 30]
                    if not all(0 <= h <= 30 for h in heights):
                        self.stdout.write(
                            self.style.ERROR(f'Invalid data at line {line_number}. Heights must be between 0 and 30.'))
                        continue

                    # Create WallProfile object
                    WallProfile.objects.create(sections=' '.join(map(str, heights)))
                self.stdout.write(self.style.SUCCESS('Profiles loaded successfully.'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('Configuration file not found.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))
