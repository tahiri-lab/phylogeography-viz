import dash
import dash_core_components as dcc
from dash_core_components.Graph import Graph
import dash_html_components as html
from dash.dependencies import Input, Output,State
import dash_bootstrap_components as dbc
#import dash_bio as dashbio
from dash_html_components.Br import Br
from dash_html_components.Div import Div
from dash_html_components.Hr import Hr
import plotly.express as px
import pandas as pd
import pathlib
from app import app
import dash_table
from dash.exceptions import PreventUpdate
import datetime

global output_df


output_df = pd.read_csv('output.csv')


table_interact = dash_table.DataTable(
                            id='datatable-interactivity1',
                            columns=[
                                {"name": i, "id": i, "deletable": False, "selectable": True, "hideable": False}
                                for i in output_df.columns
                            ],
                            data=output_df.to_dict('records'),  # the contents of the table
                            editable=False,              # allow editing of data inside all cells
                            filter_action="native",     # allow filtering of data by user ('native') or not ('none')
                            sort_action="native",       # enables data to be sorted per-column by user or not ('none')
                            sort_mode="single",         # sort across 'multi' or 'single' columns
                            column_selectable="multi",  # allow users to select 'multi' or 'single' columns
                            row_selectable="multi",     # allow users to select 'multi' or 'single' rows
                            row_deletable=False,         # choose if user can delete a row (True) or not (False)
                            selected_columns=[],        # ids of columns that user selects
                            selected_rows=[],           # indices of rows that user selects
                            page_action="native",       # all data is passed to the table up-front or not ('none')
                            page_current=0,             # page number that user is on
                            page_size=12,                # number of rows visible per page
                            style_cell={                # ensure adequate header width when text is shorter than cell's text
                                'minWidth': 95, 'maxWidth': 95, 'width': 95
                            },
                            style_data={                # overflow cells' content into multiple lines
                                'whiteSpace': 'normal',
                                'height': 'auto'
                            },
                            style_header={
                                'whiteSpace': 'normal',
                                'height': 'auto'
                            }
                        )


def serve_layout():
    #return table_interact
    return html.Div([
        html.H1('The time is: ' + str(datetime.datetime.now())),
                table_interact
    ])
    

app.layout = serve_layout

if __name__ == '__main__':
    app.run_server(debug=True)


# https://dash.plotly.com/live-updates

#https://community.plotly.com/t/updates-on-page-load-and-loading-newest-data/17220/3


'''
import time

start = time.time()
print("hello")
end = time.time()
print(end - start)
'''

'''
import smtplib
from email.message import EmailMessage
#import config


def send_email(subject,msg,reciever):
    EMAIL_ADDRESS = 'testpythonsend08@gmail.com'
    PASSWORD = 'woshixiangzai888'

    msg = EmailMessage()
    msg['Subject'] = 'Subject of the Email' # Subject of Email
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = '806981384wl@gmail.com' # Reciver of the Mail
    msg.set_content('Mail Body') # Email body or Content

    
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
           
        smtp.login(EMAIL_ADDRESS,PASSWORD)
        smtp.send_message(msg)
      
    print("Success: Email sent!")
    

subject = "HI"
msg = "hjkhlk"

reciever = '806981384wl@gmail.com'

send_email(subject,msg,reciever)

'''



'''
# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.message import EmailMessage

textfile = "textfile"
# Open the plain text file whose name is in textfile for reading.
with open(textfile) as fp:
    # Create a text/plain message
    msg = EmailMessage()
    msg.set_content(fp.read())

me = 'testpythonsend08@gmail.com'
you = '806981384wl@gmail.com@gmail.com'
msg['Subject'] = f'The contents of {textfile}'
msg['From'] = me
msg['To'] = you

# Send the message via our own SMTP server.
s = smtplib.SMTP('localhost')
s.send_message(msg)
s.quit()
'''