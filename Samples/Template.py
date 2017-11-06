import json
import PyForAlexa

# Main function that is invoked at the start of the lambda
def lambda_handler(event, context):

    # Flag to simply turn on or off logging the event and response to our cloudwatch logs
    is_debug_mode = True

    # Variable to store the output (response object) we want to return to Alexa
    output = None

    # Create an instance of the Request/SimpleRequest object from the provided event
    request = PyForAlexa.SimpleRequest(event)
    # request = PyForAlexa.Request(event)

    # Try finally block to enable debug logging to be done regardless of success or failure
    try:
        # Create a response and pass in the SessionAttributes from the request in order to ensure that they persist from session to session
        response = PyForAlexa.Response(request.SessionAttributes)

        # Check if the request type is a LaunchRequest
        if request.RequestType == PyForAlexa.RequestTypeEnum.LaunchRequest:
            
            # Response that Alexa will say/ask prompting the user for a number (This is the beginning of when we start to use custom intents)
            output = response.ask_simple("**INSERT OUTPUT SPEECH HERE**", "**INSERT REPROMPT TEXT HERE**")

        # Check if the request type is an IntentRequest
        elif request.RequestType == PyForAlexa.RequestTypeEnum.IntentRequest:
            
            # Check what Intent is being called - In this case this is the custom intent we created
            if request.IntentName.lower() == "**INSERT CUSTOM INTENT NAME HERE**".lower():
                
                ### CODE TO YOUR INTENT HERE ###
                output = response.tell_simple("**INSERT INTENT LOGIC HERE**")


            # Check if the user invoked the stop or cancel intents (These are required intents from Amazon)
            elif request.IntentName.lower() == "AMAZON.CancelIntent".lower() or request.IntentName.lower() == "AMAZON.StopIntent".lower() :
                output = response.tell_simple("**INSERT EXIT OUTPUT SPEECH HERE**")

            # Check if the user invoked the help intent and provide a help message (This is a required intent from Amazon)
            elif request.IntentName.lower() == "AMAZON.HelpIntent".lower() :
                output = response.ask_simple("**INSERT HELP OUTPUT SPEECH HERE**","**INSERT REPROMPT TEXT HERE**")

        # Return to Alexa the response you generated
        return output

    # Before closing the app and if the user has set the is_debug_mode flag to true, print the Request/Event and Response to your CloudWatch logs
    finally:
        if is_debug_mode:
            print("Request : " + json.dumps(event))
            print("Response : " + json.dumps(output))
