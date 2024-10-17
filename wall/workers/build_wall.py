from queue import Empty

from wall.models import DailyIceUsage

import logging


def worker(task_queue):
    """Worker function that processes each section and calculates ice usage."""
    while True:
        try:
            profile_id, section, height, day = task_queue.get_nowait()

            max_height = 30
            feet_needed = max_height - height

            if feet_needed > 0:
                feet_added = min(feet_needed, 1)
                ice_amount = feet_added * 195

                logging.info(
                    f'Day {day}: Profile {profile_id}, Section {section} added {feet_added} feet and used {ice_amount} cubic yards')

                DailyIceUsage.objects.create(
                    profile_id=profile_id,
                    day=day,
                    ice_used=ice_amount,
                    cost=ice_amount * 1900
                )

                # Requeue the task with updated height and incremented day
                task_queue.put((profile_id, section, height + feet_added, day + 1))

            else:
                logging.info(
                    f'Day {day}: Profile {profile_id}, Section {section} is completed. Moving to the next section.')

        except Empty:
            break

