import json
import PyForAlexa
import random

# Model object for Json data
class SpeechSample(object):
    def __init__(self, speech_id, name, speech_type, description, notes, speech_text):
        self.ID = speech_id
        self.Name = name
        self.SpeechType = speech_type
        self.Description = description
        self.Notes = notes
        self.SpeechText = speech_text


# Parse json file with the speech samples and add them to a list as SpeechSample objects
def get_speech_samples():
    
    # Create an empty list 
    speech_samples = []

    # Open the json file and load the json into memory
    with open("AlexaSpeech.json") as json_data:
        sayings = json.load(json_data)

    # Parse out each record in the json file and create an object from it, when complete add it to the list
    for item in sayings["Sayings"]:
        speech_samples.append(SpeechSample(item["ID"], item["Name"], item["Type"], item["Description"], item["Notes"], item["SpeechText"]))
    
    # Return the list of SpeechSample objects
    return speech_samples


# Main function that is invoked at the start of the lambda
def lambda_handler(event, context):

    # Variable to store the output (response object) we want to return to Alexa
    output = None

    # Create an instance of the Request/SimpleRequest object from the provided event
    request = PyForAlexa.SimpleRequest(event)
    
    # Get the list of object parsed out from the json file
    speech_samples = get_speech_samples()

    # Create a response and pass in the SessionAttributes from the request in order to ensure that they persist from session to session
    response = PyForAlexa.Response(request.SessionAttributes)

    # Check if the request type is a LaunchRequest
    if request.RequestType == PyForAlexa.RequestTypeEnum.LaunchRequest:

        # Add to the session attributes the number of times the user has requested another record

        # Prompt the user to provide the name of a speech record they wish to hear
        output = response.ask_simple("Please tell me the name of the speech sample you wish to hear.","I'm sorry I didn't get your answer, could you please repeat it?")

    # Check if the request type is an IntentRequest
    elif request.RequestType == PyForAlexa.RequestTypeEnum.IntentRequest:
        
        # Check what Intent is being called - In this case this is the custom intent we created
        if request.IntentName.lower() == "SampleSpeech".lower():

            # Get the user value
            user_value = str(request.Slots.get_by_name("speechName").Value)

            selected_item = None
            # Look for the item the user requested in the list of available records
            for item in speech_samples:
                if item.Name.lower() == user_value.lower():
                    selected_item = item
                    break
            
            # Format the data to print out to the card
            if selected_item is not None:
                card_output = "ID: " + str(selected_item.ID) + "\n"
                card_output += "Name: " + str(selected_item.Name) + "\n"
                card_output += "Type: " + str(selected_item.SpeechType) + "\n"
                card_output += "Description: " + str(selected_item.Description) + "\n"
                card_output += "Notes: " + str(selected_item.Notes) + "\n"
                card_output += "SpeechText: " + str(selected_item.SpeechText) + "\n"


                output_text_options = []
                output_text_options.append("This is great, give me more.")
                output_text_options.append("I like this game. Another!")
                output_text_options.append("This is so much more fun than I had expected, please give me more.")
                output_text_options.append("<say-as interpret-as=\"interjection\">yippee</say-as> <break time=\"500ms\"/> AGAIN AGAIN AGAIN")
                output_text_options.append("That was fun, give me another one")
                output_text_options.append("Another one please")

                output_value = random.randint(0, len(output_text_options)-1)

                output = response.ask_with_card_advanced(selected_item.SpeechText + " <break time=\"1s\"/> " + output_text_options[output_value],"Give me something else to say","Selected Speech Record : " + str(selected_item.Name),card_output)
            else:
                output = response.ask_simple("I didn't find a record for that. Please try again or give me another record to say.","I'm sorry but I didn't get that, what was your selection again?")

        # Check if the user invoked the stop or cancel intents (These are required intents from Amazon)
        elif request.IntentName.lower() == "AMAZON.CancelIntent".lower() or request.IntentName.lower() == "AMAZON.StopIntent".lower() :
            output = response.tell_simple("Ok")

        # Check if the user invoked the help intent and provide a help message (This is a required intent from Amazon)
        elif request.IntentName.lower() == "AMAZON.HelpIntent".lower() :
            output = response.ask_simple("You give me the name of a record in the coresponding JSON file and I will say the SpeechText. What would you like to hear?","I'm sorry but I didn't hear you. What was your selection again?")

    # Return to Alexa the response you generated
    return output
