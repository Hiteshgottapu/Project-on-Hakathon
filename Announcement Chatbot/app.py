
import pandas as pd
from nltk.chat.util import Chat, reflections

# Load the dataset (replace with the actual file path)
dataset_path = 'train1.xlsx'
df = pd.read_excel(dataset_path)

# Create a dictionary for quick access to train details
train_data_dict = df.to_dict(orient='records')

# Define patterns for the chatbot
patterns = [
    (r'hi|hello|hey', ['Hello! How can I assist you today?']),
    (r'^train details$', ['Sure, I can help with train details. Please provide the train number.']),
    (r'^arrival time$', ['Sure, I can provide arrival time. Please specify the train number and station name.']),
    (r'^train number for (.*)$', ['Sure, I can find the train number for that. Please provide the train name.']),
    (r'^train details for (.*)$', ['Sure, I can find the details for that. Please provide the train name.']),
    (r'^train names for (.*)$', ['Sure, I can find train names for that. Please provide the station name.']),    
    (r'^destination for (.*)$', ['Sure, I can find train names for that. Please provide the destination station.']),
    (r'^train details$', ['Sure, I can help with train details. Please provide the train name.']),
    (r'^arrival and departure times for (.*) at (.*)$', ['Sure, I can find that information.']),
    (r'^train details$', ['Sure, I can help with train details. Please provide the station name.']),
    (r'^train details$', ['Sure, I can help with train details. Please provide the train name.']),
    (r'^trains between (.*) and (.*)$', ['Sure, I can find available trains between those stations.']),
    (r'exit', ['Goodbye!']),
    (r'(.*)', ["I'm sorry, I didn't understand your request. Please try again."]),
]

# Function to get arrival time
def get_arrival_time(train_number, station_name):
    for train in train_data_dict:
        if train['Train No.'] == train_number and train['Station Name'].strip().lower() == station_name.strip().lower():
            return f"The arrival time for train {train_number} at station {station_name} is {train['Arrival time']}."
    return f"Train {train_number} or station {station_name} not found in the dataset."

# Function to get train details
def get_train_details(train_number):
    for train in train_data_dict:
        if train['Train No.'] == train_number:
            return train
    return 'Train not found in the dataset.'

# Function to get train number from train name
def get_train_number(train_name):
    for train in train_data_dict:
        if train['Train Name'].strip().lower() == train_name.strip().lower():
            return f"The train number for train '{train_name}' is {train['Train No.']}."
    return f"Train '{train_name}' not found in the dataset."

# Function to get train details by train name
def get_trains_between_stations(station_name, destination_name):
    matching_trains = []
    for train in train_data_dict:
        if (
            train['Station Name'].strip().lower() == station_name.strip().lower()
            and train['Destination Station Name'].strip().lower() == destination_name.strip().lower()
        ):
            matching_trains.append(train['train Name'])  # Replace 'Train Name' with the correct column name

    if matching_trains:
        return "\n".join(matching_trains)
    else:
        return "No matching trains found for the specified stations."

def get_train_names(station_name, destination_station):
    matching_trains = []
    for train in train_data_dict:
        if (
            train['Station Name'].strip().lower() == station_name.strip().lower()
            and train['Destination Station Name'].strip().lower() == destination_station.strip().lower()
        ):
            matching_trains.append(train['train Name'])
    
    if matching_trains:
        return "\n".join(matching_trains)
    else:
        return "No matching trains found for the specified criteria."
def get_arrival_and_departure_times(train_name, station_name):
    for train in train_data_dict:
        if (
            train['train Name'].strip().lower() == train_name.strip().lower()
            and train['Station Name'].strip().lower() == station_name.strip().lower()
        ):
            return f"Train: {train_name}\nStation: {station_name}\nArrival Time: {train['Arrival time']}\nDeparture Time: {train['Departure time']}"

    return "Information not found for the specified train and station."
def get_distance(station_name, destination_name):
    for train in train_data_dict:
        if (
            train['Station Name'].strip().lower() == station_name.strip().lower()
            and train['Destination Station Name'].strip().lower() == destination_name.strip().lower()
        ):
            return f"Distance between {station_name} and {destination_name} is {train['Distance']} kilometers."

    return "Distance information not found for the specified stations."
# Create a chatbot
chatbot = Chat(patterns, reflections)


# Main chat loop
print("Train Details Chatbot")
print("Type 'exit' to end the conversation.")
while True:
    user_input = input().strip().lower()

    
    if user_input == 'exit':
        response = "Goodbye!"
    elif 'train details' in user_input:
        print("Chatbot: Please provide the train number.")
        train_number = input("You: ").strip()
        train_info = next((train for train in train_data_dict if train['Train No.'] == train_number), None)
        print("Chatbot:")
        if train_info:
            for key, value in train_info.items():
                print(f"{key}: {value}")
        else:
            print(f"Train {train_number} not found in the dataset.")
    elif 'arrival time' in user_input:
        print("Chatbot: Please specify the train number and station name for which you want to know the arrival time.")
        train_number = input("Train Number: ").strip()
        station_name = input("Station Name: ").strip()
        arrival_time = get_arrival_time(train_number, station_name)
        print("Chatbot:", arrival_time)
        
    elif 'trains between' in user_input:
    # Extract station names from user input
        parts = user_input.split('between')
        if len(parts) == 2:
            station_and_destination = parts[1].split('and')
            if len(station_and_destination) == 2:
                station_name, destination_name = [part.strip() for part in station_and_destination]
                train_list = get_trains_between_stations(station_name, destination_name)
                print("Chatbot:")
                if "No matching trains found" in train_list:
                    print(train_list)
                else:
                    print(f"Trains between {station_name} and {destination_name}:\n{train_list}")
            else:
                print("Chatbot: Please provide both station name and destination name separated by 'and'.")
        else:
            print("Chatbot: Please provide both station name and destination name.")
    elif 'train times' in user_input:
        print("Chatbot: Please provide the train name.")
        train_name = input("You: ").strip()
        station_name = input("Please provide the station name: ").strip()

        train_details_response = get_arrival_and_departure_times(train_name, station_name)
        print("Chatbot:")
        if "Information not found" in train_details_response:
            print(train_details_response)
        else:
            print(train_details_response)
    elif 'station distance' in user_input:
        print("Chatbot: Please provide the station name.")
        station_name = input("You: ").strip()
        destination_name = input("Please provide the destination name: ").strip()

        distance_response = get_distance(station_name, destination_name)
        print("Chatbot:")
        if "Distance information not found" in distance_response:
            print(distance_response)
        else:
            print(distance_response)
    else:
        response = chatbot.respond(user_input)
        print("Chatbot:", response[0])
   
