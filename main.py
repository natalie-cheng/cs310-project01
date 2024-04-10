#
# Main program for photoapp program using AWS S3 and RDS to
# implement a simple photo application for photo storage and
# viewing.
#
# Authors:
#   Natalie Cheng
#   Prof. Joe Hummel (initial template)
#   Northwestern University
#   Fall 2023
#

import datatier  # MySQL database access
import awsutil  # helper functions for AWS
import boto3  # Amazon AWS

import uuid
import pathlib
import logging
import sys
import os

from configparser import ConfigParser

import matplotlib.pyplot as plt
import matplotlib.image as img


###################################################################
#
# prompt
#
def prompt():
  """
  Prompts the user and returns the command number
  
  Parameters
  ----------
  None
  
  Returns
  -------
  Command number entered by user (0, 1, 2, ...)
  """
  print()
  print(">> Enter a command:")
  print("   0 => end")
  print("   1 => stats")
  print("   2 => users")
  print("   3 => assets")
  print("   4 => download")
  print("   5 => download and display")
  print("   6 => upload")
  print("   7 => add user")

  cmd = int(input())
  return cmd


###################################################################
#
# stats
#
def stats(bucketname, bucket, endpoint, dbConn):
  """
  Prints out S3 and RDS info: bucket name, # of assets, RDS 
  endpoint, and # of users and assets in the database
  
  Parameters
  ----------
  bucketname: S3 bucket name,
  bucket: S3 boto bucket object,
  endpoint: RDS machine name,
  dbConn: open connection to MySQL server
  
  Returns
  -------
  nothing
  """
  #
  # bucket info:
  #
  print("S3 bucket name:", bucketname)

  assets = bucket.objects.all()
  print("S3 assets:", len(list(assets)))

  #
  # MySQL info:
  #
  print("RDS MySQL endpoint:", endpoint)

  # sql = """
  # select now();
  # """

  # row = datatier.retrieve_one_row(dbConn, sql)
  # if row is None:
  #   print("Database operation failed...")
  # elif row == ():
  #   print("Unexpected query failure...")
  # else:
  #   print(row[0])

  # Query to retrieve the number of users
  user_count_query = """
  SELECT COUNT(*) FROM users;
  """
  # Get count
  user_count = datatier.retrieve_one_row(dbConn, user_count_query)[0]

  if user_count is None:
      print("Failure to receive user count...")
  else:
      print("# of users:", user_count)

  # Query to retrieve the number of assets
  asset_count_query = """
  SELECT COUNT(*) FROM assets;
  """
  # Get count
  asset_count = datatier.retrieve_one_row(dbConn, asset_count_query)[0]

  if asset_count is None:
      print("Failure to retrieve asset count...")
  else:
      print("# of assets:", asset_count)

###################################################################
#
# users
#
def users(dbConn):
  """
  Prints out users in descending order by user id
  
  Parameters
  ----------
  dbConn: open connection to MySQL server
  
  Returns
  -------
  nothing
  """

  # Query to retrieve users in descending order by user id
  sql_query = """
  SELECT userid, email, lastname, firstname, bucketfolder FROM users ORDER BY userid DESC;
  """
  # Get all the users
  users = datatier.retrieve_all_rows(dbConn, sql_query)

  if users is None:
      print("Failed to retrieve user info...")
  else:
      for user in users:
          userid, email, lastname, firstname, folder = user
          print(f"User id: {userid}")
          print(f" Email: {email}")
          print(f" Name: {lastname} , {firstname}")
          print(f" Folder: {folder}\n")

###################################################################
#
# assets
#
def assets(dbConn):
  """
  Prints out assets in descending order by asset id
  
  Parameters
  ----------
  dbConn: open connection to MySQL server
  
  Returns
  -------
  nothing
  """

  # Query to retrieve assets in descending order by asset id
  sql_query = """
  SELECT assetid, userid, assetname, bucketkey FROM assets ORDER BY assetid DESC;
  """
  # Get all the users
  assets = datatier.retrieve_all_rows(dbConn, sql_query)

  if assets is None:
      print("Failed to retrieve asset info...")
  else:
      for asset in assets:
          assetid, userid, name, keyname = asset
          print(f"Asset id: {assetid}")
          print(f" User id: {userid}")
          print(f" Original name: {name}")
          print(f" Key name: {keyname}\n")

###################################################################
#
# download
#
def download(bucket, dbConn, asset_id, display):
  """
  Renames and downloads the image based on the user given asset id
  Displays if required
  
  Parameters
  ----------
  dbConn: open connection to MySQL server
  asset_id: user given asset id
  display: bool for displaying image
  
  Returns
  -------
  nothing
  """
  # Look up asset in the database and retrieve
  sql_query = """
  SELECT assetname, bucketkey FROM assets WHERE assetid = %s;
  """
  asset = datatier.retrieve_one_row(dbConn, sql_query, [asset_id])

  if asset is None:
      print("No such asset...")
      return
  
  # Get asset name and key
  asset_name, asset_key = asset
  
  # Download asset
  downloaded_asset = awsutil.download_file(bucket, asset_key)
  if downloaded_asset is None:
        print("S3 download error...")
        return
  
  # Rename asset
  os.rename(downloaded_asset, asset_name)

  print(f"Downloaded from S3 and saved as: ' {asset_name} '")

  # Display image if necessary
  if (display):
    import matplotlib.pyplot as plt
    import matplotlib.image as img
    image = img.imread(asset_name)
    plt.imshow(image)
    plt.show()
     

###################################################################
#
# upload
#
def upload(bucket, dbConn, local_filename, user_id):
  """
  Uploads a file into the bucket
  
  Parameters
  ----------
  bucket: S3 boto bucket object,
  dbConn: open connection to MySQL server
  local_filename: local file to upload
  user_id: the user id
  
  Returns
  -------
  nothing
  """

###################################################################
#
# add user
#
def add_user(bucketname, bucket, endpoint, dbConn):
  """
  Prints out S3 and RDS info: bucket name, # of assets, RDS 
  endpoint, and # of users and assets in the database
  
  Parameters
  ----------
  bucketname: S3 bucket name,
  bucket: S3 boto bucket object,
  endpoint: RDS machine name,
  dbConn: open connection to MySQL server
  
  Returns
  -------
  nothing
  """


#########################################################################
# main
#
print('** Welcome to PhotoApp **')
print()

# eliminate traceback so we just get error message:
sys.tracebacklimit = 0

#
# what config file should we use for this session?
#
config_file = 'photoapp-config.ini'

print("What config file to use for this session?")
print("Press ENTER to use default (photoapp-config.ini),")
print("otherwise enter name of config file>")
s = input()

if s == "":  # use default
  pass  # already set
else:
  config_file = s

#
# does config file exist?
#
if not pathlib.Path(config_file).is_file():
  print("**ERROR: config file '", config_file, "' does not exist, exiting")
  sys.exit(0)

#
# gain access to our S3 bucket:
#
s3_profile = 's3readwrite'

os.environ['AWS_SHARED_CREDENTIALS_FILE'] = config_file

boto3.setup_default_session(profile_name=s3_profile)

configur = ConfigParser()
configur.read(config_file)
bucketname = configur.get('s3', 'bucket_name')

s3 = boto3.resource('s3')
bucket = s3.Bucket(bucketname)

#
# now let's connect to our RDS MySQL server:
#
endpoint = configur.get('rds', 'endpoint')
portnum = int(configur.get('rds', 'port_number'))
username = configur.get('rds', 'user_name')
pwd = configur.get('rds', 'user_pwd')
dbname = configur.get('rds', 'db_name')

dbConn = datatier.get_dbConn(endpoint, portnum, username, pwd, dbname)

if dbConn is None:
  print('**ERROR: unable to connect to database, exiting')
  sys.exit(0)

#
# main processing loop:
#
cmd = prompt()

while cmd != 0:
  #
  if cmd == 1:
    stats(bucketname, bucket, endpoint, dbConn)
  elif cmd ==2:
    users(dbConn)
  elif cmd ==3:
    assets(dbConn)
  elif cmd ==4:
    # Prompt for asset id
    print("Enter asset id>")
    asset_id = int(input())
    download(bucket, dbConn, asset_id, False)
  elif cmd ==5:
    # Prompt for asset id
    print("Enter asset id>")
    asset_id = int(input())
    download(bucket, dbConn, asset_id, True)
  elif cmd ==6:
    # Prompt for local filename
    print("Enter local filename>")
    local_filename = input()
    # Prompt for user id
    print("Enter user id>")
    user_id = int(input())
    upload(bucket, dbConn, local_filename, user_id)
  elif cmd ==7:
    add_user(bucketname, bucket, endpoint, dbConn)
  else:
    print("** Unknown command, try again...")
  #
  cmd = prompt()

#
# done
#
print()
print('** done **')