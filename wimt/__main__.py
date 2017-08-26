#!/usr/bin/env python3

import argparse

from . import wimt

def main():
    parser = argparse.ArgumentParser(
        description="Find your train's current location")
    parser.add_argument('-b', '--boarding-station',
        help='limit the output to the given boarding station',
        dest='station')
    parser.add_argument('-s', '--send-to',
        help='send the output to the given email ID',
        dest='email')
    parser.add_argument(
        'train', help='the train number to track the status of')
    args = parser.parse_args()

    data = wimt.get_train_data(args.train, args.station)
    if args.email:
        wimt.send_email_report(data, args.email)
    else:
       print(wimt.create_text_timetable(data))
    
if __name__ == '__main__':
    main()
