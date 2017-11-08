import random
import json
import PyForAlexa

# Main function that is invoked at the start of the lambda
def lambda_handler(event, context):

    # Flag we have created to simply turn on or off logging the event and response to our cloudwatch logs
    is_debug_mode = True
    # Variable to store the output (response object) we want to return to Alexa
    output = None
    # Create an instance of the SimpleRequest because we only need basic info from the event in this program
    request = PyForAlexa.SimpleRequest(event)

    # Try finally block to enable debug logging to be done regardless of success or failure
    try:
        # Create a response and pass in the SessionAttributes from the request in order to ensure that they persist from session to session
        response = PyForAlexa.Response(request.SessionAttributes)

        # Check if the request type is a LaunchRequest
        if request.RequestType == PyForAlexa.RequestTypeEnum.LaunchRequest:
            
            # Add entries to the session attributes object that we will need in every session for the following:
            # Number of attempts is the running total of times that the user has guessed a number
            response.SessionAttributes.insert("number_of_attempts", 0)
            # The random number that the user is trying to guess
            response.SessionAttributes.insert("number_to_guess", random.randint(1, 100))
            # A list to track all of the guesses the user has already made
            response.SessionAttributes.insert("previous_guesses", list())

            # Response that Alexa will say/ask prompting the user for a number (This is the beginning of when we start to use custom intents)
            output = response.ask_simple("Let's play the high low game. Please guess a number between 1 and 100", "Excuse me but I need to know your guess")

        # Check if the request type is an IntentRequest
        elif request.RequestType == PyForAlexa.RequestTypeEnum.IntentRequest:
            
            # Get values of session attributes
            number_of_attempts = response.SessionAttributes.get_by_key("number_of_attempts")
            number_to_guess = response.SessionAttributes.get_by_key("number_to_guess")
            previous_guesses = response.SessionAttributes.get_by_key("previous_guesses")

            # Check what Intent is being called - In this case this is the custom intent we created
            if request.IntentName.lower() == "MakeGuessIntent".lower():
                
                # Try/Except block used here to ensure that the value that the user gives is a valid number
                try:

                # Get the value of the slot 'guessedNumber' (This is the guess that the user makes)
                    guessed_number = int(request.Slots.get_by_name("guessedNumber").Value)

                    # Check that the current guess isn't already logged in the previous_guesses list
                    if guessed_number not in previous_guesses:
                        
                        # Add the current guess to the previous guess list
                        previous_guesses.append(guessed_number)

                        # Modify the values of the number_of_attempts and previous_guesses in the SessionAttributes on the Response object
                        number_of_attempts += 1
                        response.SessionAttributes.edit_by_key("number_of_attempts", number_of_attempts)
                        response.SessionAttributes.edit_by_key("previous_guesses", previous_guesses)

                        # Determine if the user is correct, too high or too low and respond accordingly
                        if guessed_number == number_to_guess:
                            output = response.tell_advanced("<say-as interpret-as='interjection'>bada bing bada boom</say-as>. You were correct, it took you " + str(number_of_attempts) + "attempts to figure it out")

                        elif guessed_number > number_to_guess:
                            output = response.ask_simple("You're guess of " + str(guessed_number) + " was too high, please give me another guess","I'm sorry I didn't quite get that, what was your new guess again?")

                        elif guessed_number < number_to_guess:
                            output = response.ask_simple("You're guess of " + str(guessed_number) + " was too low, please give me another guess","I'm sorry I didn't quite get that, what was your new guess again?")

                        else:
                            output = response.ask_simple("You're guess of " + str(guessed_number) + " was incorrect, please give me another guess","I'm sorry I didn't quite get that, what was your new guess again?")
                    else:
                        # If the user has guessed the current number, reply back to the user that they have already guessed it and if it's too high or low
                        number_position = None
                        if guessed_number > number_to_guess:
                            number_position = "too high"
                        else:
                            number_position ="too low"
                             
                        output = response.ask_simple("You have already guessed " + str(guessed_number) + " and it was " + number_position + ". Please give me another guess. ","I'm sorry I didn't quite get that, what was your new guess again?")
                except:
                    # Response to handle if the value given by the user isn't a number
                    output = response.ask_simple("I'm sorry but that's not a number, please give me a number.","I'm sorry but could you please repeat that.")

            # Check if the user invoked the stop or cancel intents (These are required intents from Amazon)
            elif request.IntentName.lower() == "AMAZON.CancelIntent".lower() or request.IntentName.lower() == "AMAZON.StopIntent".lower() or request.IntentName.lower() == "AMAZON.NoIntent".lower() :
                output = response.tell_simple("Ok, maybe later.")

            # Check if the user invoked the help intent and provide a help message (This is a required intent from Amazon)
            elif request.IntentName.lower() == "AMAZON.HelpIntent".lower() :
                text = """In order to play this game you need to guess the number that I have picked. 
                Give me a number between 1 and 100 and I will tell you if you are too high or too low. 
                So with that being said what is your guess?"""
                output = response.ask_simple(text,"I'm sorry but I didn't get your guess. Please give me a number between 1 and 100")
            
            # Since the slot we are expecting is also the invoke value for our custom intent, check here for the value and provide a message, otherwise the app may think you are trying to invoke an intent that doesn't exist
            else:
                output = response.ask_simple("I'm sorry but that's not a number, please give me a number.","I'm sorry but could you please repeat that.")

        # Return to Alexa the response you generated
        return output

    # Before closing the app and if the user has set the is_debug_mode flag to true, print the Request/Event and Response to your CloudWatch logs
    finally:
        if is_debug_mode:
            print("Request : " + json.dumps(event))
            print("Response : " + json.dumps(output))
