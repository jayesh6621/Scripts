
## An absolute file path describes how to access a given file or directory, starting from the root of the file system. A file path is also called a pathname. Relative file paths are notated by a lack of a leading forward slash.

## Parser for command-line options, arguments and sub-commands. ... The argparse module also automatically generates help and usage messages and issues errors when users give the program invalid arguments

## A MIME attachment with the content type "application/octet-stream" is a binary file. Typically, it will be an application or a document that must be opened in an application, such as a spreadsheet or word processor. If the attachment has a filename extension associated with it, you may be able to tell what kind of file it is. A .exe extension, for example, indicates it is a Windows or DOS program (executable), while a file ending in .doc is probably meant to be opened in Microsoft Word.

##The open() function opens a file in text format by default. To open a file in binary format, add 'b' to the mode parameter. Hence the "rb" mode opens the file in binary format for reading, while the "wb" mode opens the file in binary format for writing. Unlike text mode files, binary files are not human readable.

import argparse
import os
import smtplib

from email import Encoders
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.Utils import formatdate

DIR = os.path.abspath(os.path.dirname(__file__))

LOGS = [
        os.path.join(DIR, 'logs', 'error.log'),
        os.path.join(DIR, 'logs', 'access.log')
]

## os.path.join(DIR, 'logs', 'error.log') = DIR/logs/error.log

def send_logs(host, user, password, send_to, send_from, client):
        """
        Sends the log file to send_to
        """
		## Create the container (outer) email message
        msg = MIMEMultipart()
        msg['From'] = send_from
        msg['To'] = send_to
        msg['Subject'] = '{} Logs'.format(client)
        msg['Date'] = formatdate(localtime=True)

        for log in LOGS:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(open(log, 'rb').read())
                Encoders.encode_base64(part)
                part.add_header(
                        'Content-Disposition',
                        'attachment; filename={}'.format(os.path.basename(log))
                )
                msg.attach(part)

        try:
                server = smtplib.SMTP(host)
                server.starttls()
                server.login(user, password)
        except Exception, e:
                err = 'Something terrible happened: {}'.format(str(e))
                print err
                return False

        try:
                worked = server.sendmail(send_from, send_to, msg.as_string())
        except Exception, e:
                err = 'Unable to send email: {}'.format(str(e))
                print err
                return False
        finally:
                server.close()
        return True

def clean_logs():
        """
        Clear out the log files
        """
        for log in LOGS:
                with open(log, 'w') as l:
                        pass

def main():
        """
        The main deal.  Sets up an argument parser and calls send_logs and
        clean_logs
        """
        parser = argparse.ArgumentParser(description='Email server logs')
        parser.add_argument('-s', '--server', dest='server',
                           default='smtp.gmail.com', help='The mail server')
        parser.add_argument('-u', '--user', dest='user', help='Email username')
        parser.add_argument('-p', '--password', dest='pw', help='Email password')
        parser.add_argument('-t', '--to', dest='to', help='Where to send')
        parser.add_argument('-f', '--from', dest='frm', help='Email from?')
        parser.add_argument('-c', '--client', dest='client', help='Client name')

        args = parser.parse_args()

        send_from = args.frm if args.frm is not None else args.user

        email_sent = send_logs(args.server, args.user, args.pw, args.to,
                                                     send_from, args.client)
        if email_sent:
                clean_logs()

if __name__ == '__main__':
        main()
		
