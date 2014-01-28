import sys
import getopt
import datetime
'''
'' Quick script to parse a CSV from a iPhone SQLite3 db with a table
'' for messages using: 
''    : sqlite3 <db_name>
''    : SELECT date, address, text, flags, sender FROM message WHERE address='<RECEIVER_PHONE>' OR sender='<RECEIVER_PHONE>';
'' EX: 
'' SELECT date, address, text, flags, sender FROM message WHERE address='+111111111' OR sender='+1111111111';
'' OR 
'' For messages using:
'' SELECT date, address, text, flags, sender FROM message WHERE address='+111111111' OR sender='+1111111111';
''
'''

# SQLite3 Delimiter
VALUE_DELIMITER = '-|-'

# Date converter
DATE_CONVERTER = datetime.datetime(1,1,1,1,1,1,1)

# If true prints the messages in increasing chronological order 
INCREASING_CHRONO_ORDER = True

# PARAMS for MSGS from the Database
# ID_INDEX = 0
# DATE_INDEX = 1
# ADDRESS_INDEX = 2
# TEXT_INDEX = 3
# FLAGS_INDEX = 4
# HTML_INDEX = 5
# SENDER_INDEX = 6
DATE_INDEX = 0
ADDRESS_INDEX = 1
TEXT_INDEX = 2
FLAGS_INDEX = 3
SENDER_INDEX = 4


# Delineates flags 
SENT_FLAG = '3'       # What I sent
RECEIVER_FLAG = '2'   # What She sent

# Name of person associated with each flag
SENT_FLAG_NAME = "XXXXXXX XXXXXXX"    # My Name 
RECEIVER_FLAG_NAME = "XXXXXXX XXXXXXX" # Friend's Name

# Phone Number of person associated with each flag
SENT_FLAG_PHONE = "111111111"  # My Number
RECEIVER_FLAG_PHONE = "+111111111" # Friend's Number

def main(argv=sys.argv):
  # first arg is always the program name
  if argv is None:
    return
  # First arg is the name of this file
  # Get messages file name
  fileName = argv[1]

  # Get Out file name
  outFileName = argv[2] if len(argv) > 2 else 'output/out-' + fileName

  # Open the messages file
  msgFile = open(fileName, 'r')

  # Read all of the messages 
  msgs = msgFile.read();

  # Split the messages content by comma
  msgContent = msgs.split(VALUE_DELIMITER)

  # output file
  formattedFile = open(outFileName, 'w')

  # Output messages
  formattedMsgs = ''

  # Now get messages
  i = 0
  while i < len(msgContent):
    if i + SENDER_INDEX >= (len(msgContent)):
      break

    # Break up message attributes
    # Each msg has attrs: id , date , address , text , flags, html, sender
    d = float(msgContent[i + DATE_INDEX])
    addr = msgContent[i + ADDRESS_INDEX]
    text = msgContent[i + TEXT_INDEX]
    flags = msgContent[i + FLAGS_INDEX]
    sender = msgContent[i + SENDER_INDEX]
    senderName = RECEIVER_FLAG_NAME

    # Set appropriate sender name based on the flag
    if flags == SENT_FLAG:
      senderName = SENT_FLAG_NAME
      sender = SENT_FLAG_PHONE

    # Format the date by converting from a timestamp to human time
    formattedDate = DATE_CONVERTER.fromtimestamp(d)

    # Create string of form: FNAME LNAME <111111111> : Hello, my lady!
    output = '\n' + str(formattedDate) + '------------------------------------------------ \n'
    output += senderName + " <" + sender + "> " + ": " + text + "\n"
    
    if INCREASING_CHRONO_ORDER:
      formattedMsgs = output + formattedMsgs
    else: 
      formattedMsgs += output
    # Print to formatted file 
    #formattedFile.write(output)

    # Increment Counter
    i+= 5

  # Print all the messages to the file
  formattedFile.write(formattedMsgs)
  
  # Close files when finished
  msgFile.close()  
  formattedFile.close()  


# Run our functio
if __name__ == "__main__":
    sys.exit(main())