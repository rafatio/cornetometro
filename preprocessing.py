import os
import re

count = 0

def preprocess_tweet(tweet, teams, players):
  global count
  count += 1

  processed_tweet = tweet.lower() # To lowercase
  processed_tweet = re.sub('\n', ' ', processed_tweet) # Removing newlines
  processed_tweet = re.sub(r'#[^#!\n ]+', '', processed_tweet) # Removing hashtags
  processed_tweet = re.sub(r'http(.)+', '', processed_tweet) # Removing links

  processed_tweet = re.sub(r'[0-9]-[0-9]', '#score', processed_tweet) # Changing scores to custom token
  processed_tweet = re.sub(r'(\w)\1{2,}', r'\1', processed_tweet) # Removing unnecessary repeating of letters

  # Replaces team names for custom token
  for team in teams:
    if team.lower() in processed_tweet:
      processed_tweet = processed_tweet.replace(team.lower(), "#team")

  # Replaces player names for custom token
  for player in players:
    if player.lower() in processed_tweet:
      processed_tweet = processed_tweet.replace(player.lower(), "#player")

  # Merge two consecutive occurences of team and player tokens
  processed_tweet = processed_tweet.replace("#team #team", "#team")
  processed_tweet = processed_tweet.replace("#player #player", "#player")

  return processed_tweet

def preprocess_file(input_file, output_file):
  tweet = ''

  teams = input_file.readline()[:-1].lower().split() # Reads teams from fist line. Removes newline and splits the string.
  players = input_file.readline()[:-1].lower().split() # Reads players from fist line.

  line_number = 0
  for line in input_file:
    if line[:4] == '####':
      if tweet[:4] == '###!':
        processed_tweet = preprocess_tweet(tweet, teams, players)
        output_file.write(processed_tweet)
        output_file.write('\n#####\n')
      tweet = ''
    else:
      tweet += line

def main():
    path_of_file = os.path.dirname(os.path.realpath(__file__))
    path_datasets = path_of_file + "/data_classified"

    output_folder = path_of_file + "/preprocessed"
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

if __name__ == "__main__":
    main()
