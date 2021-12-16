# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 20:35:02 2021

@author: Kabir
"""
### to let the program sleep ###
import time
import schedule
from datetime import datetime

### for extracting emails ###
import imaplib
import email
from email.header import decode_header
import webbrowser
import os

### for sending to sheets ###
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint #stands for pretty print

## machine learning
import torch
import torch.nn as nn
import torch.optim as optim


class MultipleRegression(nn.Module):
    def __init__(self, num_features):
        super(MultipleRegression, self).__init__()
        
        self.layer_1 = nn.Linear(num_features, 16)
        self.layer_2 = nn.Linear(16, 32)
        self.layer_3 = nn.Linear(32, 16)
        self.layer_out = nn.Linear(16, 1)
        
        self.relu = nn.ReLU()
    def forward(self, inputs):
            x = self.relu(self.layer_1(inputs))
            x = self.relu(self.layer_2(x))
            x = self.relu(self.layer_3(x))
            x = self.layer_out(x)
            return (x)
    def predict(self, test_inputs):
            x = self.relu(self.layer_1(test_inputs))
            x = self.relu(self.layer_2(x))
            x = self.relu(self.layer_3(x))
            x = self.layer_out(x)
            return (x)

#Import model for the ML
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = torch.load('/Users/Kabir/Desktop/IOT/COURSEWORK/Machine Learning Model/model.pth')
Email_importance = 0 # declare the variable that the ML will calculate

# account credentials
username = "kk6118@ic.ac.uk"
password = "Sandhya1!!!"

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Emails (real time)").sheet1  # Open the spreadhseet
data = sheet.get_all_records()  # Get a list of all records


### get sentiment of text ###
import nltk 
from nltk.sentiment.vader import SentimentIntensityAnalyzer
#nltk.download('vader_lexicon')   
sentiment_analyzer = SentimentIntensityAnalyzer()

def get_sentiment(text):
    return sentiment_analyzer.polarity_scores(text)['compound']

### word/phrase checking functions ###
def checkForPhrase(string):
    matches = ["respond", "you should", "could you", "provide me with", "asap", "as soon as possible", "DE4"]
    if any(x in string for x in matches):
        body_key_phrase = 1
    else:
        body_key_phrase = 0
    return body_key_phrase

def checkifTutor(string):
    matches = ["<t.nanayakkara@imperial.ac.uk>", "Nanayakkara:", "p.demirel@imperial.ac.uk", "<e.makarova17@imperial.ac.uk>", "h.haddadi@imperial.ac.uk", "e.kirchberger@imperial.ac.uk", "<elena.dieckmann13@imperial.ac.uk>", "<m.rahim@imperial.ac.uk>", "<t.lalitharatne@imperial.ac.uk>"]
    if any(x in string for x in matches):
        from_tutor = 1
    else:
        from_tutor = 0
    return from_tutor

### If the ML model predicted that the e-mail has importance lower than 2, and urgent is in the title, it won't be overridden because it is probably still spam
def checkUrgence(string, datapoint):
    global Email_importance
    matches = ["Urgent:", "Urgent", "urgent", "URGENT"]
    if any(x in string for x in matches):
        Email_importance = predictImportance(datapoint)
        if Email_importance > 2:
            Email_importance = 10
    return Email_importance

#Deploy my ML model
def predictImportance(datapoint):
    global Email_importance
    datapoint = datapoint.to(device)
    #print(datapoint)
    with torch.no_grad():
        model.eval()
        Email_importance = model(datapoint)
        Email_importance = Email_importance.item()
        Email_importance = round(Email_importance, 1) #round to 1 d.p.
    return Email_importance

### ML variables ###
document_attachment = 0
HTML_attachment = 0
body_key_phrase = 0
from_tutor = 0
importance = 0 #this is the label


'''
#only run the following code once to poulate the spreadsheet with titles
#The first two rows are needed for data analysis, the last three are for human interpretation 
titles = ["Unix Time", "Predicted Importance", "Date & Time", "Sender", "Subject"]
sheet.insert_row(titles, 1)
'''



# create an IMAP4 class with SSL, use your email provider's IMAP server
imap = imaplib.IMAP4_SSL("imap-mail.outlook.com")

# authenticate
imap.login(username, password)

# select a mailbox (in this case, the inbox mailbox)
# use imap.list() to get the list of mailboxes
#status, messages = imap.select("INBOX")

    
'''
basically I will have to make N equal to new(messages) - messages
if N = 0, then I'll have to insert an empty row
find N1
wait 5 minutes
find N2
find N1-N2
use this to do the e-mail thing
'''



def updateInbox():
    global status, messages
    status, messages = imap.select("INBOX")
    return messages

    
#gets the number of e-mails at t1
def findN1(all_messages):
    global messages_t1
    messages_t1 = int(all_messages[0])
    return messages_t1


#gets the number of e-mails at t2
def findDiffN1N2(all_messages):
    global messages_t2
    messages_t2 = int(all_messages[0])
    return messages_t2 - messages_t1


# total number of emails
messages_for_loop = int(updateInbox()[0])


def checkMail(messages_for_loop, N):
    global document_attachment
    for i in range(messages_for_loop, messages_for_loop-N, -1):
        #print(messages_for_loop-N)
        # fetch the email message by ID
        res, msg = imap.fetch(str(i), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                # parse a bytes email into a message object
                msg = email.message_from_bytes(response[1])
                # decode the email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    try:
                        # if it's a bytes, decode to str
                        subject = subject.decode(encoding)
                    except:
                        subject = "None"
                # decode email sender
                From, encoding = decode_header(msg.get("From"))[0]
                if isinstance(From, bytes):
                    From = From.decode(encoding)
                try:
                    To, encoding = decode_header(msg["To"])[0]
                    if isinstance(To, bytes):
                        To = To.decode(encoding)
                except:
                        To = "None"
                # if the email message is multipart
                if msg.is_multipart():
                    # iterate over email parts
                    for part in msg.walk():
                        # extract content type of email
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        try:
                            # get the email body
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass
                      
                        if "attachment" in content_disposition:
                            document_attachment = 1
                        else:
                            document_attachment = 0
                else:
                    # extract content type of email
                    content_type = msg.get_content_type()
                    # get the email body
                    try:
                        body = msg.get_payload(decode=True).decode()
                    except:
                        body = "None"
                    
        if content_type == "text/html":
            HTML_attachment = 1
        else:
            HTML_attachment = 0
        
        #Chunk for me to identify e-mail in the console
        '''
        print("Subject:", subject)   
        print("From:", From)
        print("To:", To) 
        '''
        #This chunk predicts the importance of the e-mail and overrides it straight to 10 if the e-mail has 'urgent' written in the subject and is not from a common spammer
        datapoint = torch.tensor([[get_sentiment(subject),checkifTutor(From),get_sentiment(body),checkForPhrase(body),document_attachment,HTML_attachment]])
        predictImportance(datapoint)
        checkUrgence(subject, datapoint) #check for urgency in subject
        print("The e-mail's predicted importance is " + str(Email_importance)) #print the predicted importance from the model
        
        
        now = datetime.now() # dd/mm/YY H:M:S
        TimeAndDate = now.strftime("%d/%m/%Y %H:%M:%S")
        unixTime = int(time.time())    
        
        Latest_Email = [unixTime, Email_importance, TimeAndDate, From, subject]
        sheet.insert_row(Latest_Email, 2)  # Insert the list as a row at index 2 in google sheets



while True:
    findN1(messages)
    print()
    time.sleep(120)
    print("at time 1 there are " + str(messages_t1) + " messages")    
    updateInbox()
    checkMail(int(updateInbox()[0]),findDiffN1N2(messages))
    print("at time 2 there are " + str(messages_t2) + " messages")    
    print("There have been " + str(messages_t2 - messages_t1) + " new e-mails since the last sample was taken.")
    print()




# close the connection and logout
imap.close()
imap.logout()

