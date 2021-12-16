# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 20:35:02 2021

@author: Kabir
"""
### to let the program sleep ###
import time

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

# account credentials
username = "kk6118@ic.ac.uk"
password = "Sandhya1!!!"

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Outlook dataset").sheet1  # Open the spreadhseet
data = sheet.get_all_records()  # Get a list of all records


#populate google sheet with feature titles
titles = ["Sender", "Subject", "Importance(1-10)", "Subject (sentiment)", "From Tutor? (Y/N) ","Body(sentiment)", "Key phrases in body ?(Y/N)", "Document attached?(Y/N)", "HTML attachments?(Y/N)"] #add body too
sheet.insert_row(titles, 1)


### get sentiment of text ###
import nltk 
from nltk.sentiment.vader import SentimentIntensityAnalyzer
#nltk.download('vader_lexicon')   
sentiment_analyzer = SentimentIntensityAnalyzer()

def get_sentiment(text):
    return sentiment_analyzer.polarity_scores(text)['compound']

### word checking functions ###

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


def checkUrgence(string):
    matches = ["Urgent:", "urgent:", "URGENT"]
    global importance
    if any(x in string for x in matches):
        importance = 10
    else:
        importance = "enter importance here"
    return importance


def checkAnnoyingSpammer(string):
    matches = ["<news@email.gordonramsayrestaurants.com>:", "<hello@announcement.deliveroo.co.uk>", "<josh@opportunities.brightnetwork.co.uk>", "<nia.davies19@imperial.ac.uk>", "<enquiries@u2tuition.com>", "<jobs@email.targetjobs.co.uk>" , "Lowercase Events", "<debating-soc@imperial.ac.uk>", "<ebay@reply2.ebay.co.uk>", "<careers@imperial.ac.uk>", "Gradcracker", "<uber@uber.com>", "<lorenzo.verani17@imperial.ac.uk>", "<rmp@ratemyplacement-email.co.uk>", "<team@fatsoma.com>", "<no-reply@mail.instagram.com>", "<vpeducation@imperial.ac.uk>", "<dylan@opportunities.brightnetwork.co.uk>", "<social@dramsoc.org>", "<superdrug@email.superdrug.com>", "<no-reply@mailings.annsummers.com>", "<no-reply@mailers.countryattire.com>", "<leonardo@imperial.ac.uk>", "<wushu-bounces@imperial.ac.uk>", "<news@email.gordonramsayrestaurants.com>", "IC Kung Fu", "Imperial Indian Society", "<Intl.PR@Keyloop.com>", "<dodgeball@imperial.ac.uk>", "Imperial Indian Society", "<pnepal@imperial.ac.uk>", "<marisa.hadjichristofis19@imperial.ac.uk>", "<debating-soc@imperial.ac.uk>", "materialise", ]
    global importance
    if any(x in string for x in matches):
        importance = 1
    return importance



### ML variables ###
document_attachment = 0
HTML_attachment = 0
body_key_phrase = 0
from_tutor = 0

importance = 0 #this is the label

# number of top emails to fetch
N = 500

# create an IMAP4 class with SSL, use your email provider's IMAP server
imap = imaplib.IMAP4_SSL("imap-mail.outlook.com")

# authenticate
imap.login(username, password)

# select a mailbox (in this case, the inbox mailbox)
# use imap.list() to get the list of mailboxes
status, messages = imap.select("INBOX")

# total number of emails
messages = int(messages[0])

for i in range(messages, messages-N, -1):
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
     
    checkUrgence(subject) #check for urgency in subject
    checkAnnoyingSpammer(From) #override global variable if spam
 
    #For me to identify e-mail so that I can label it (non-numerical)
    print("Subject:", subject)   
    print("From:", From)
    print("To:", To) 
    print("From tutor :" + str(checkifTutor(From)))    
    print("Subject sentiment score: " + str(get_sentiment(subject)))
    print("Body sentiment score: " + str(get_sentiment(body)))
    print("key words: " + str(checkForPhrase(body)))  
    print("Document attached:" + str(document_attachment))
    print("HTML attachment:" + str(HTML_attachment))
    print("Known importance: " + str(importance))
    print("content type: " + content_type)
    print() #empty line

    #send training data to google sheets
    
    DataPoint = [From, subject, importance, get_sentiment(subject), checkifTutor(From), get_sentiment(body), checkForPhrase(body), document_attachment, HTML_attachment] #add body too
    sheet.insert_row(DataPoint, 2)  # Insert the list as a row at index 2 in google sheets (row 1 has headers)
     
    time.sleep(3) #This stops me from reaching the maximum number of quotas per minute on google sheets

# close the connection and logout
imap.close()
imap.logout()

