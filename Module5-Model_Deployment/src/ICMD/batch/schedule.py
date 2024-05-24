import os
import sys
from crontab import CronTab

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import ROOT_DIR


def main():
    cron = CronTab(user=True)
    script_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "batch_inference.py")
    )
    command = f"{os.path.join(ROOT_DIR,'icmd_env/bin/python')} {script_path}"
    job = cron.new(command=command, comment="Runs batch inference script")
    # Runs script every minute
    job.setall("* * * * *")
    cron.write()

    print("Cron job created successfully")


if __name__ == "__main__":
    main()
