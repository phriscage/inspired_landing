#!/usr/bin/python
""" 
    Name: user_list_dump.py
    Developer: Chris Page
    Purpose: Dump the current user list and update the google spreadsheet
        with the new user data
"""
import os
import sys
import gdata.spreadsheet.service
import MySQLdb
import logging
import time
import argparse

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../lib')
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../conf')

from inspired_landing_config import DB_USER, DB_PASSWD, DB_HOST

logging.basicConfig(
    level=logging.DEBUG,
    format=('%(asctime)s %(levelname)s %(name)s[%(process)s] : %(funcName)s '
        ' : %(message)s'),
    filename='/var/log/invidio/user_list_dump.log',
    filemode='a')

logger = logging.getLogger(__name__)

def _get_users():
    """ get the logged in users 
    Retruns:
        users (tup): tuple of user dictionaries
    """
    logger.debug("Getting the users...")
    database = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD)
    cursor = database.cursor(MySQLdb.cursors.DictCursor)
    query_sql = """
        SELECT 
            email_address, 
            created_at 
        FROM inspired_landing.users
        ORDER BY user_id
    """
    cursor.execute(query_sql)
    users = (row for row in cursor.fetchall())
    cursor.close()
    return users


def _create_client(email_address, password):
    """ create the client object 
    Returns:
        client (obj): gdata.spreadsheet.service.SpreadsheetsService
            client 
    """
    logger.debug("Creating the client...")
    client = gdata.spreadsheet.service.SpreadsheetsService()
    client.email = email_address
    client.password = password
    client.source = 'DUMP'
    client.ProgrammaticLogin()
    return client
    

def main(email_address, password):
    """ run the main logic 
    Args:
        email_address (str): email address for auth
        password (str): password for auth
    """
    logger.info("Starting...")
    spreadsheet_key = '0Anuh1TrO5NgZdHhheGZ2ZDVpSmRJbVU0anpZX1YwZUE'
    worksheet_id = 'od6'
    now = time.strftime('%m/%d/%Y %H:%M:%S')

    users = _get_users()
    client = _create_client(email_address, password)
    spreadsheet_rows = client.GetListFeed(spreadsheet_key, worksheet_id)
    batchRequest = gdata.spreadsheet.SpreadsheetsCellsFeed()
    logger.debug("Total spreadsheet_rows = '%i' already exist." 
        % len(spreadsheet_rows.entry))
    for user_index, user_data in enumerate(users):
        new_data = {
            'email-address': user_data['email_address'],
            'created-at': str(user_data['created_at']),
            #'inserted-at': '=now()'
            'inserted-at': str(now)
        }
        if user_index < len(spreadsheet_rows.entry):
            entry = spreadsheet_rows.entry[user_index]
            row_data = dict(zip(entry.custom.keys(),
                [value.text for value in entry.custom.values()]))
            if new_data['email-address'] != row_data['email-address']:
                logger.debug("UpdateRow for user: '%s'" % new_data)
                client.UpdateRow(entry, new_data)
        else:
            logger.debug("InsertRow for user: '%s'" % new_data)
            client.InsertRow(new_data, spreadsheet_key, worksheet_id)
        #print dict(zip(entry.custom.spreadsheet_keys(),
            #[value.text for value in entry.custom.values()]))
        #print entry.custom.values()
    logger.info("Finished.")
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--email_address",
        help="Email Address for authentication",
        dest="email_address", type=str, required=True)
    parser.add_argument("-p", "--password",
        help="Password for authentication",
        dest="password", type=str, required=True)
    kwargs = parser.parse_args()
    main(**kwargs.__dict__)

