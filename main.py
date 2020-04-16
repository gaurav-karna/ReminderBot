from sys import exit
import argparse

ALL_ARGS = None


# found a free server to execute blindly, will update with CRON if need be


def sanity():
    if ALL_ARGS.hour > 23 or ALL_ARGS.hour < 0:
        print('Error in hour provided, must be >= 0 and <= 23')
        exit(0)
    if ALL_ARGS.min > 59 or ALL_ARGS.min < 0:
        print('Error in minute provided, must be >= 0 and <= 59')
        exit(0)


def set_cron():
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CRON setup to send reminder texts')
    parser.add_argument('--cron', action='store_true')
    parser.add_argument('--hour', help='hour in EST', type=int)
    parser.add_argument('--min', help='min of hour, default = 0', type=int, default=0)
    parser.add_argument('--msg', help='message to send', type=str, default='None provided')
    ALL_ARGS = parser.parse_args()
    print(ALL_ARGS.cron)
    # sanity()
    # set_cron()
