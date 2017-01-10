import os
import re

count = 0

def preprocess_tweet(tweet):
  global count
  count += 1

  processed_tweet = tweet.lower() # To lowercase
  processed_tweet = re.sub(r'#[^#!\n ]+', '', processed_tweet) # Removing hashtags
  processed_tweet = re.sub(r'http(.)+', '', processed_tweet) # Removing links

  processed_tweet = re.sub(r'[0-9]-[0-9]', '#score', processed_tweet) # Changing scores to custom token

  return processed_tweet

def preprocess_file(input_file, output_file):
  tweet = ''
  for line in input_file:
    if line[:4] == '####':
      if tweet[:4] == '###!':
        processed_tweet = preprocess_tweet(tweet)
        output_file.write(processed_tweet)
        output_file.write('#####\n')
      tweet = ''
    else:
      tweet += line

path_of_file = os.path.dirname(os.path.realpath(__file__))
path_datasets = path_of_file + "/data_classified"

output_folder = path_of_file + "/bin"
output_file_path = output_folder + "/dataset.txt"

if not (os.path.isdir(output_folder)):
  os.mkdir(output_folder)

output_file = open(output_file_path, 'w')

for input_file_name in os.listdir(path_datasets):
  input_file = open("{}/{}".format(path_datasets, input_file_name), 'r')
  preprocess_file(input_file, output_file)
  input_file.close()

output_file.close()

print count
