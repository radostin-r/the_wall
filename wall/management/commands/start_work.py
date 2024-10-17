import django
from django.core.management.base import BaseCommand
from wall.models import WallProfile, DailyIceUsage
import pandas as pd
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor
from wall.workers.build_wall import worker

import logging


class Command(BaseCommand):
    help = ('Start the work on the wall and calculate daily ice usage per profile.')

    def add_arguments(self, parser):
        parser.add_argument('--num_teams', type=str, help='The number of teams for multiprocessing version.', default=None)

    def handle(self, *args, **kwargs):
        num_teams = int(kwargs['num_teams']) if kwargs['num_teams'] else None
        if num_teams:
            self.multiprocess_work(num_teams)
        else:
            self.calculate_daily_ice_usage()

    def calculate_daily_ice_usage(self):
        profiles = WallProfile.objects.all()
        total_ice = 0
        total_cost = 0

        for profile in profiles:

            # skip a profile if we already calculated the costs and usage
            if DailyIceUsage.objects.filter(profile=profile).exists():
                continue

            sections = profile.get_sections()
            max_height = 30
            ice_per_foot = 195
            cost_per_cubic_yard = 1900
            df = pd.DataFrame(sections)

            # Calculate the number of days each section needs to reach the target height
            total_days_required = df.apply(lambda x: max_height - x, axis=0).clip(lower=0)
            day = 1

            while total_days_required.sum().sum() > 0:
                active_sections = total_days_required > 0
                ice_for_today = active_sections.sum().sum() * ice_per_foot
                total_ice += ice_for_today
                cost_for_today = ice_for_today * cost_per_cubic_yard
                total_cost += cost_for_today
                total_days_required = total_days_required.apply(lambda x: x - 1)
                total_days_required = total_days_required.clip(lower=0)

                DailyIceUsage.objects.create(
                    profile=profile,
                    day=day,
                    ice_used=ice_for_today,
                    cost=cost_for_today,
                )

                self.stdout.write(self.style.SUCCESS(
                    f'Successfully recorded {ice_for_today} cubic yards for profile {profile.id} on day {day}'))
                day += 1

        return total_ice, total_cost

    def multiprocess_work(self, num_teams):
        """Calculate the total ice used on a given day using multiprocessing.Queue for multiple profiles."""
        df = self.preprocess_profiles()
        mp.set_start_method('spawn')
        task_queue = self.create_task_queue(df)
        self.handle_tasks(num_teams, task_queue)
        self.stdout.write(self.style.SUCCESS('Successfully recorded daily ice usage for all profiles.'))

    @staticmethod
    def preprocess_profiles():
        """Load wall profiles into a DataFrame and preprocess section data."""
        profiles = WallProfile.objects.all()
        profile_data = []

        for profile in profiles:
            for section_idx, section_height in enumerate(profile.get_sections()):
                profile_data.append({
                    'profile_id': profile.id,
                    'height': section_height,
                    'section': section_idx
                })

        # Create a DataFrame from the wall profile data
        df = pd.DataFrame(profile_data)
        df['max_height'] = 30
        df['feet_needed'] = df['max_height'] - df['height']
        df['completed'] = df['feet_needed'] <= 0
        return df

    @staticmethod
    def create_task_queue(df):
        """Create a task queue for sections that need work."""
        task_queue = mp.Manager().Queue()
        day = 1
        # Add tasks for sections that are not completed
        for index, row in df.iterrows():
            if not row['completed']:
                task_queue.put((row['profile_id'], row['section'], row['height'], day))

        return task_queue

    @staticmethod
    def handle_tasks(num_teams, task_queue):
        """Handle task distribution using multiprocessing."""
        # Initialize the pool of workers
        print('CREATE POOL, ', mp.get_start_method())
        with ProcessPoolExecutor(max_workers=num_teams, initializer=Command.subprocess_setup) as pool:
            results = []
            for _ in range(num_teams):
                pool.map(worker, (task_queue,))
                # results.append(result)

            # Collect results from workers
            # for result in results:
            #     result.get()

    @staticmethod
    def subprocess_setup():
        django.setup()
        from django.db import connections
        for conn in connections.all():
            conn.close()


if __name__ == '__main__':
    # protect entry point
    print('WORKER START')
    logging.info('Worker starting.')
