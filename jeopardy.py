import pandas as pd
pd.set_option('display.max_colwidth', -1)

# Loading the data and investigating it
jeopardy_data = pd.read_csv("jeopardy.csv")
print(jeopardy_data.columns)

# Renaming misformatted columns
jeopardy_data = jeopardy_data.rename(columns = {" Air Date": "Air Date", " Round" : "Round", " Category": "Category", " Value": "Value", " Question":"Question", " Answer": "Answer"})
#print(jeopardy_data.columns)
#print(jeopardy_data["Question"])

# Filtering a dataset by a list of words
def filter_data(data, words):
  # Lowercases all words in the list of words as well as the questions. Returns true if all of the words in the list appear in the question.
  filter = lambda x: all(word.lower() in x.lower() for word in words)
  # Applies the lambda function to the Question column and returns the rows where the function returned True
  return data.loc[data["Question"].apply(filter)]

# Testing the filter function
filtered = filter_data(jeopardy_data, ["King", "England"])
print(filtered["Question"])

# Adding a new column. If the value of the float column is not "None", then we cut off the first character (which is a dollar sign), and replace all commas with nothing, and then cast that value to a float. If the answer was "None", then we just enter a 0.
jeopardy_data["Float Value"] = jeopardy_data["Value"].apply(lambda x: float(x[1:].replace(',','')) if x != "None" else 0)

# Filtering the dataset and finding the average value of those questions
filtered = filter_data(jeopardy_data, ["King"])
print(filtered["Float Value"].mean())

# A function to find the unique answers of a set of data
def get_answer_counts(data):
    return data["Answer"].value_counts()

# Testing the answer count function
print(get_answer_counts(filtered))

#Task 7: Investigate the ways in which questions change over time
# Convert the "Air Date" column to datetime
jeopardy_data["Air Date"] = pd.to_datetime(jeopardy_data["Air Date"])

# Filter questions from the 90s and 2000s
questions_90s = jeopardy_data[(jeopardy_data["Air Date"] >= "1990-01-01") & (jeopardy_data["Air Date"] < "2000-01-01")]
questions_2000s = jeopardy_data[(jeopardy_data["Air Date"] >= "2000-01-01")]

# Count the occurrences of the word "Computer" in each decade
count_90s = filter_data(questions_90s, ["Computer"]).shape[0]
count_2000s = filter_data(questions_2000s, ["Computer"]).shape[0]

print(f"Number of questions from the 90s with the word 'Computer': {count_90s}")
print(f"Number of questions from the 2000s with the word 'Computer': {count_2000s}")

# Task 7: Check the connection between round and category
# Create a pivot table to count occurrences of each category in each round
category_round_counts = jeopardy_data.pivot_table(index="Category", columns="Round", aggfunc="size", fill_value=0)

# Print the counts for "Literature" in Single Jeopardy and Double Jeopardy
# Create a pivot table to count occurrences of each category in each round
category_round_counts = jeopardy_data.pivot_table(index="Category", columns="Round", aggfunc="size", fill_value=0)

# Print the counts for "Literature" in Single Jeopardy and Double Jeopardy
literature_counts = category_round_counts.loc["LITERATURE", ["Jeopardy!", "Double Jeopardy!"]]
print(f"Counts for 'Literature' in Single Jeopardy and Double Jeopardy:\n{literature_counts}")

#Task 7: Build a system to quiz yourself
import random

def quiz_yourself(data):
  random_question = data.sample(1) # Select a random question

  # Display the question and get user input
  user_answer = input(f"\nQuestion: {random_question['Question'].values[0]}\nYour Answer: ")

  # Check if the user's answer is correct
  correct_answer = random_question['Answer'].values[0]
  if user_answer.lower() == correct_answer.lower():
    print("Correct!")
  else:
    print(f"Wrong! The correct answer is: {correct_answer}")

# Test the quiz function
quiz_yourself(jeopardy_data)
