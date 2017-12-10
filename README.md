# PyForAlexa

PyForAlexa is a native python 3 SDK for Amazon Alexa. It is lightweight and helps to quickly and efficiently develop custom Alexa skills.
Using this SDK will give developers access to the Alexa request objects along with with a SimpleRequest object for quicker access to the most desired pieces of information.
It also simplifies the creation of responses by providing functions that allow a user to generate their entire response in a single call. 
All in all this SDK should cut down the time it takes to get up and running custom skills on Alexa. 

## Getting Started
These instructions will help you to install and develop to this SDK.

### Prerequisites

- Python 3
- Amazon AWS Account (For more information: https://aws.amazon.com/)
- Amazon Developer Account (For more information: https://developer.amazon.com/alexa)

### Installing

Instructions on how to add the SDK to a project.

#### Run
```
pip install PyForAlexa
```

#### Install to a local directory for upload to AWS Lambda
```
pip install --target="LOCAL DIRECTORY PATH HERE" PyForAlexa 
```

#### Clone

1. Clone/Download the repo to the desired location.
2. Copy the PyForAlexa directory and add it to the same directory as the Alexa program source code.
3. Import the SDK into the project

```
import PyForAlexa
```

### Using PyForAlexa

#### Request

PyForAlexa uses the request provided by Alexa in the event parameter of the handler to create an object that the user can more easily implement. There are two Request objects that you can create, __Request__ and __SimpleRequest__.

The Request object contains the information provided by the Alexa event in the structure it's provided. For more information on request elements, please see: https://developer.amazon.com/docs/custom-skills/request-and-response-json-reference.html#request-format .

For simple Alexa apps, there are very few of the elements in the request that are needed. The SimpleRequest object provides the user with the few properties that the will more than likely need for simple voice apps. If more of the properties are needed then use the full Request object instead. The properties provided are as follows.

* **SimpleRequest**
    * SessionAttributes
    * RequestType
    * IntentName
    * Slots

For those who are new to Alexa development, these are the fields that are most liking going to be needed from the request.

- **SessionAttributes** - Session Attributes is a collection of key pair variables that the user wishes to persist from session to session. If an element is not stored in the session attributes it will be lost at the close of the session that it was created. 

- **RequestType** - This is the type of request that was initiated. Currently, only standard requests are supported. These types are _LaunchRequest_, _IntentRequest_, and _SessionEndedRequest_. An enum called RequestTypeEnum, has been created to help work with these request types. The _LaunchRequest_ when the user has told Alexa to invoke a program. Most often the user will be dealing with _IntentRequest_ types. These are the types that are invoked when a user is interacting with an intent they have created. Finally, _SessionEndedRequest_ is triggered if the app is closed for any other reason than the proper closing of a session.

- **IntentName** - This is the name of the intent that the user has created. This will only have a value if the RequestType is _IntentRequest_.

- **Slots** - The slots object is a collection of values that the user speaks to Alexa. These are usually responses to questions or any input from a user that has a corresponding slot for Alexa. Slots are only present if the RequestType is _IntentRequest_.

#### Response
The response object is content that the user intends to send back to Alexa. The user must minimally respond back to Alexa with text for output speech. The Response object has a property to store the Session Attributes that they wish to carry on to further sessions, and functions to easily create the response to return. The functions are as follows.

- **tell_simple** - Creates a response that will have Alexa respond with the provided text and end the session.

- **tell_with_card_simple** - Creates a response that will have Alexa respond with the provided text, create a simple card that will be sent to the users Alexa app and end the session.

- **tell_advanced** - Creates a response that will have Alexa respond with the provided text in the SSML format and end the session.

- **tell_with_card_advanced** - Creates a response that will have Alexa respond with the provided text in the SSML format. It also creates a standard card, which can contain images, that will be returned to the users Alexa App. Finally, the session will be ended.

- **ask_simple** - Creates a response that will have Alexa respond with the provided text and will keep the session alive to waiting for interaction from the user. Reprompts are implemented for when a user does not respond to the original prompt.

- **ask_with_card_simple** - Creates a response that will have Alexa respond with the provided text and will keep the session alive to waiting for interaction from the user. Reprompts are implemented for when a user does not respond to the original prompt. A simple card will also be sent to the users Alexa app with the provided content.

- **ask_advanced** - Creates a response that will have Alexa respond with the provided text in the SSML format, and will keep the session alive to waiting for interaction from the user. Reprompts are implemented in SSML for when a user does not respond to the original prompt.

- **ask_with_card_advanced** - Creates a response that will have Alexa respond with the provided text in the SSML format, and will keep the session alive to waiting for interaction from the user. Reprompts are implemented in SSML, for when a user does not respond to the original prompt. A Standard card will also be sent to the users Alexa app with the provided content. Standard cards also allow users to provide images via HTTPS URL to the images.

- **generate_response** - Dynamically builds the response that will be sent to Alexa using the custom provided object.

### Implementation Recommendations and Notes
---

 * Use the optional parameter of the Response constructor to pass in the SessionAttributes from the Request object. This will allow you to persist your attributes with minimal effort and to add, modify or remove as you see fit.

 * Unless you need advanced functionality, use the SimpleRequest and provided simple response functions to create your app. You are in no way limited to using them however these features are less confusing and easier to work with.

* If you use the Request object, always check the type of request you are are getting because the objects for each of the types are different and do not have all of the same properties.

* If you are intending to include references to any images or sounds files, your files **MUST** be secured with HTTPS or Alexa will not use them.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
