from enum import Enum


class OutputSpeechTypeEnum(Enum):
    """Enum that provides the valid options of OutputSpeech Types used in the OutputSpeech object."""
    PlainText = 1
    SSML = 2


class CardTypeEnum(Enum):
    """Enum that provides the valid options of Card Types used in the Card object."""
    Simple = 1
    Standard = 2
    LinkAccount = 3


class RequestTypeEnum(Enum):
    """Enum that provides the valid options of Standard Request types used by the Request object."""
    LaunchRequest = 1
    IntentRequest = 2
    SessionEndedRequest = 3


class SessionEndedRequestErrorTypeEnum(Enum):
    """Enum that provides the valid options of Standard Request types used by the Request object."""
    INVALID_RESPONSE = 1
    DEVICE_COMMUNICATION_ERROR = 2
    INTERNAL_ERROR = 3


class IntentConfirmationStatusEnum(Enum):
    """Enum that provides the valid options of the Intent confirmation status """
    NONE = 1
    CONFIRMED = 2
    DENIED = 3

class SimpleRequest(object):
    def __init__(self, event):
        
        self.IntentName = None
        self.Slots = Slots()

        r = Request(event)
        self.SessionAttributes = r.Session.SessionAttributes
        self.RequestType = r.Request.Type
        if self.RequestType == RequestTypeEnum.IntentRequest:
            self.IntentName = r.Request.Intent.Name
            self.Slots = r.Request.Intent.Slots
            

class Session(object):
    """Model object for the session section in the request."""
    def __init__(self, new_session, session_id, application=None, session_attributes=None, request_user=None):
        self.NewSession = new_session
        self.SessionID = session_id
        self.Application = None
        self.SessionAttributes = SessionAttributes()
        self.User = None

        # Check if the application provided was an instance of the Application object
        if isinstance(application, Application):
            self.Application = application

        # Check if the session attributes provided was an instace of the SessionAttributes object
        if isinstance(session_attributes, SessionAttributes):
            self.SessionAttributes = session_attributes

        # Check if the provided value for user was an instance of User object
        if isinstance(request_user, User):
            self.User = request_user


class User(object):
    """Model object for the user section in the session section."""
    def __init__(self, user_id, access_token=None, permissions=None):
        self.UserID = None
        self.AccessToken = None
        self.Permissions = None

        # check that user_id is not none and isn't just an empty value
        if user_id is not None and str(user_id).strip():
            self.UserID = user_id

        # Check if there is an access token and if not then don't add the attribute
        if access_token is not None and str(access_token).strip():
            self.AccessToken = access_token

        # Check if there is a value for permissions and that it's of the right object type
        if permissions is not None:
            if isinstance(permissions, Permissions):
                self.Permissions = permissions


class Permissions(object):
    """Model object for the permissions section in the user section."""
    def __init__(self, consent_token=None):
        self.ConsentToken = consent_token


class Application(object):
    """Model object for the application section in the session section."""
    def __init__(self, application_id):
        self.ApplicationID = None

        if application_id is not None and not application_id:
            self.ApplicationID = application_id

class Context(object):
    """Model object for the context section in the request."""
    def __init__(self, system, audio_player=None):

        self.System = None
        self.AudioPlayer = None

        if isinstance(system,System):
            self.System = system

        if isinstance(audio_player,AudioPlayer):
            self.AudioPlayer = audio_player


class System(object):
    """Model object for the system section in the context section."""
    def __init__(self, device, application, user, api_endpoint):
        self.Device = None
        self.Application = None
        self.User = None
        self.APIEndpoint = api_endpoint

        # Check that the provided values are the proper instance types
        if isinstance(device, Device):
            self.Device = device

        if isinstance(application, Application):
            self.Application = application

        if isinstance(user, User):
            self.User = user


class Device(object):
    """Model object for the device section in the system section."""
    def __init__(self, device_id, supported_interfaces):
        
        self.DeviceID = device_id
        self.SupportedInterfaces = supported_interfaces


class AudioPlayer(object):
    """Model object for the AudioPlayer section in the context section."""
    def __init__(self, player_activity, token, offset_in_milliseconds):
        self.PlayerActivity = player_activity
        self.Token = token
        self.OffsetInMilliseconds = offset_in_milliseconds


class Slot(object):
    """Model object for slot info (user provided inputs) found in the request."""
    def __init__(self, name, value, confirmation_status):
        self.Name = name
        self.Value = value
        self.ConfirmationStatus = confirmation_status


class StandardRequest(object):
    """Base class for the Alexa request types"""
    def __init__(self, request_type, request_id, timestamp, locale):
        self.Type = request_type
        self.RequestID = request_id
        self.Timestamp = timestamp
        self.Locale = locale


class LaunchRequestObject(StandardRequest):
    """Model used to create a LaunchRequest object from the request that is provided to the user from Alexa"""
    def __init__(self, request_type, request_id, timestamp, locale):
        super().__init__(request_type, request_id, timestamp, locale)


class IntentRequest(StandardRequest):
    """Model used to create a IntentRequest object from the request that is provided to the user from Alexa"""
    def __init__(self, request_type, request_id, timestamp, locale, dialog_state, intent):

        # Implement the constructor of the base class to include those properties into the current object
        super().__init__(request_type, request_id, timestamp, locale)

        # Add the properties for the IntentRequest
        self.DialogState = dialog_state
        self.Intent = intent


class SessionEndedRequest(StandardRequest):
    def __init__(self, request_type, request_id, timestamp, locale, session_error=None):
        """Model used to create a SessionEndedRequest object from the request that is provided to the user from Alexa"""

        self.SessionError = None

        # Implement the constructor of the base class to include those properties into the current object
        super().__init__(request_type, request_id, timestamp, locale)

        # Check if the session_error attributes is none and/ or of the right instance type and if it passes validation, add it to the object
        if session_error is not None:
            if isinstance(session_error, SessionEndedRequestError):
                self.SessionError = session_error
            else:
                raise TypeError("The Error in the SessionEndedRequest must be of type SessionEndedRequestError")


class SessionEndedRequestError(object):
    """Model used to create a SessionEndedRequestError object which is a sub object of the SessionEndedRequest object"""

    def __init__(self, error_type, message):
        # Add the SessionEndedRequestError properties
        self.ErrorType = error_type
        self.Message = message


class Intent(object):
    """Model used to create an Intent object which is a sub object of the IntentRequest object and values are provided by the request from Alexa"""

    def __init__(self, name, confirmation_status, slots=None):
        # Create the properties for the Intent object
        self.Name = name
        self.ConfirmationStatus = confirmation_status

        # Check that the value provide by the the slots input is the proper instance type and if it's not then provide an empty instance of it
        if isinstance(slots, Slots):
            self.Slots = slots
        else:
            self.Slots = Slots()

class Card(object):
    """Object used to create a card that can be sent with the response"""

    def __init__(self, card_type, title, text, card_image=None):

        # Type : Check that the user provided value is the proper type and if not throw a TypeError
        if isinstance(card_type, CardTypeEnum):
            self.Type = card_type
        else:
            raise TypeError("card_type is required and must be of the type CardTypeEnum Enum")

        # Title : Check that it has a value and if not then throw ValueError
        if title is not None and title != "":
            self.Title = title
        else:
            raise ValueError("title cannot be none or empty")

        # Text : Check that it has a value and if not then throw ValueError
        if text is not None and text != "":
            self.Text = text
        else:
            raise ValueError("Text cannot be none or empty")

        # Check that the Card Image provided is not none and is of the proper instance type and adds it as a Card Image instance otherwise it raises an exception.
        if card_image is not None:
            if isinstance(card_image, CardImage):
                self.CardImage = card_image
            else:
                raise TypeError("card_image must be of type CardImage")
        else:
            self.CardImage = None


class CardImage(object):
    """Object used to create a card image that can be added onto the card object"""

    def __init__(self, small_image_url, large_image_url):

        # Check if the small image url is empty or none and raises and exception if it is
        if small_image_url is None or small_image_url == "":
            raise ValueError("small_image_url cannot be none or empty")
        else:
            self.SmallImageURL = small_image_url

        # Check if the large image url is empty or none and raises and exception if it is
        if large_image_url is None or large_image_url == "":
            raise ValueError("small_image_url cannot be none or empty")
        else:
            self.LargeImageURL = large_image_url


class OutputSpeech(object):
    """Model used to create an OutputSpeech object that is added to the response"""

    def __init__(self, speech_type, text):

        # Type : Check that the user provided value is the proper type and if not throw a TypeError
        if isinstance(speech_type, OutputSpeechTypeEnum):
            self.Type = speech_type
        else:
            raise TypeError("speech_type is required and must of the type OutputSpeechTypeEnum Enum")

        # Text: Validate the provided text and assign its the text property, if validation fails raise an exception
        if text is None or text == "":
            raise ValueError("Text cannot be none or empty")

        elif len(text) > 8000:
            raise ValueError("Text cannot be longer than 8000 characters")

        else:
            self.Text = text


class Reprompt(OutputSpeech):
    """Model Used to create a reprompt object that can be added to the response. Reprompt is just a wrapper for the OutputSpeech object."""
    pass


class SessionAttributes(object):
    """Used to use, store and pass along variables/attributes that a user wishes to carry between different session states."""

    def __init__(self):
        """Create a dictionary that will be private to each instance"""
        self.__temp = {}

    def insert(self, key, value):
        """Checks if the collection already has the key and updates it if it does, otherwise it adds it."""
        if key in self.__temp:
            self.__temp[key] = value
        else:
            self.__temp.update({key: value})

    def get_all(self):
        """Returns a dictionary of all of the session attributes."""
        return self.__temp

    def delete_by_key(self, key):
        """Removes a specified session attribute from the collection."""
        del self.__temp[key]

    def get_by_key(self, key):
        """Gets a specified session attribute by the provided key"""
        if key in self.__temp:
            return self.__temp[key]
        else:
            return None

    def edit_by_key(self, key, value):
        """Edit a specified record in the session attributes"""
        if key in self.__temp:
            self.__temp[key] = value

    def delete_all(self):
        """Clears all session attributes from the collection"""
        self.__temp.clear()


class Slots(object):
    """Storage for the slots(user provided inputs) found in the request"""

    def __init__(self):
        """Create a dictionary that will be private to each instance"""
        self.__slots_dictionary = {}

    def insert(self, slot):
        """Checks if the collection already has the slot and updates it if it does, otherwise it adds it."""
        if slot.Name in self.__slots_dictionary:
            self.__slots_dictionary[slot.Name] = slot
        else:
            self.__slots_dictionary.update({slot.Name: slot})

    def get_by_name(self, slot_name):
        """Retrieves a slot using the provided slot name"""
        if slot_name in self.__slots_dictionary:
            return self.__slots_dictionary[slot_name]
        else:
            return None

    def __delete_by_name(self, slot_name):
        """Removes a specified slot from the colletion using the provided slot name"""
        del self.__temp[slot_name]

    def get_all(self):
        """Returns a dictionary of all the slots"""
        return self.__slots_dictionary

    def __delete_all(self):
        """Clears the collection of all slots"""
        self.__slots_dictionary.clear()


class Request(object):
    """Request object that contains the functionality to create the request objects from the event property provided by Alexa."""
    def __init__(self, event):
        
        # Check if the event json contains the the following sections and if it does then map those sections
        if "version" in event:
            self.Version = event["version"]
        else:
            raise ValueError("The version is missing from 'event'")

        if "session" in event:
            self.Session = self.__create_session(event["session"])
        else:
            raise ValueError("The session section is missing from 'event'")

        if "context" in event:
            self.Context = self.__create_context(event["context"])
        else:
            raise ValueError("The context section is missing from 'event'")

        if "request" in event:
            self.Request = self.__create_request_section(event["request"])
        else:
            raise ValueError("The request section is missing from 'event'")


    def __create_request_section(self, dict_request):
        """Map the request section provided by Alexa to it's corresponding models"""
        temp = None
        request_id = None
        timestamp = None
        locale = None
        request_type = self.__get_request_type(dict_request)

        # Check that the request section contains the following sections and if it does then get each respective value
        if "requestId" in dict_request:
            request_id = dict_request["requestId"]

        if "timestamp" in dict_request:
            timestamp = dict_request["timestamp"]

        if "locale" in dict_request:
            locale = dict_request["locale"]

        # Create the correct type of alexa request type base on the type found in the event
        if request_type == RequestTypeEnum.LaunchRequest:
            temp = LaunchRequestObject(request_type, request_id, timestamp, locale)

        elif request_type == RequestTypeEnum.SessionEndedRequest:
            temp = SessionEndedRequest(request_type, request_id, timestamp, locale)

        elif request_type == RequestTypeEnum.IntentRequest:

            # check if the request section has the intent section and if so then create an map the intent section
            if "intent" in dict_request:

                dict_intent = dict_request["intent"]

                intent_name = None
                confirmation_status = None
                slots = None

                if "name" in dict_intent:
                    intent_name = dict_intent["name"]

                if "slots" in dict_intent:
                    slots = Slots()
                    slots_from_request = dict_intent["slots"]

                    for item in slots_from_request.values():
                        slot = Slot(item["name"], item["value"], item["confirmationStatus"])
                        slots.insert(slot)

                intent = Intent(intent_name, confirmation_status, slots)

                temp = IntentRequest(request_type, request_id, timestamp, locale, None, intent)

        return temp

    def __create_session(self, dict_session):
        """Map the session section provided by Alexa to it's corresponding models"""
        session_new = None
        session_id = None
        application = None
        session_attributes = None
        user = None

        # Check that the session section contains the needed sections and map the corresponding values if it does
        if "new" in dict_session:
            session_new = dict_session["new"]

        if "sessionId" in dict_session:
            session_id = dict_session["sessionId"]

        if "application" in dict_session:
            application = self.__create_application(dict_session["application"])

        if "attributes" in dict_session:
            session_attributes = self.__create_session_attributes(dict_session["attributes"])

        if "user" in dict_session:
            user = self.__create_user(dict_session["user"])

        return Session(session_new, session_id, application, session_attributes, user)

    def __create_application(self, dict_application):
        """Map the application section provided by Alexa to it's corresponding models"""
        application = None

        # Check that the provided section contains the needed sections and map the corresponding values if it does
        if "applicationId" in dict_application:
            application = Application(dict_application["applicationId"])

        return application

    def __create_session_attributes(self, dict_attributes):
        """Map the session attributes section provided by Alexa to it's corresponding models"""
        
        session_attributes = SessionAttributes()

        for item in dict_attributes:
            session_attributes.insert(item, dict_attributes[item])

        return session_attributes

    def __create_user(self, dict_user):
        """Map the user section provided by Alexa to it's corresponding models"""
        user_id = None
        access_token = None
        permission = Permissions()

        # Check that the provided section contains the needed sections and map the corresponding values if it does
        if "permissions" in dict_user:
            if "consentToken" in dict_user["permissions"]:
                permission = Permissions(dict_user["permissions"]["consentToken"])

        if "userId" in dict_user:
            user_id = dict_user["userId"]

        if "accessToken" in dict_user:
            access_token = dict_user["accessToken"]

        return User(user_id, access_token, permission)


    def __create_context(self, dict_context):
        """Map the context section provided by Alexa to it's corresponding models"""

        if "System" in dict_context:
            system = self.__create_system(dict_context["System"])

        if "AudioPlayer" in dict_context:
            audio_player = self.__create_audio_player(dict_context["AudioPlayer"])

        return Context(system, audio_player)

    def __create_system(self, dict_system):
        """Map the system section provided by Alexa to it's corresponding models"""

        api_endpoint = None

        if "apiEndpoint" in dict_system:
            api_endpoint = dict_system["apiEndpoint"]

        if "device" in dict_system:
            device = self.__create_device(dict_system["device"])

        if "application" in dict_system:
            application = self.__create_application(dict_system["application"])

        user = self.__create_user(dict_system)

        return System(device, application, user, api_endpoint)

    def __create_device(self, dict_device):
        """Map the device section provided by Alexa to it's corresponding models"""

        device_id = None
        supported_interfaces = None

        if "deviceId" in dict_device:
            device_id = dict_device["deviceId"]

        if "supportedInterfaces" in dict_device:
            supported_interfaces = dict_device["supportedInterfaces"]

        return Device(device_id, supported_interfaces)

    def __create_audio_player(self, dict_audio_player):
        """Map the audio player section provided by Alexa to it's corresponding models"""
        player_activity = None
        token = None
        offset = None

        if "playerActivity" in dict_audio_player:
            player_activity = dict_audio_player["playerActivity"]

        if "token" in dict_audio_player:
            token = dict_audio_player["token"]

        if "offsetInMilliseconds" in dict_audio_player:
            offset = dict_audio_player["offsetInMilliseconds"]

        return AudioPlayer(player_activity, token, offset)

    def __get_request_type(self, dict_request):
        """Maps the provided request type to it's RequestTypeEnum enum value and raises and exception if it cannot be mapped."""

        output = None
        request_type = None
        
        if "type" in dict_request:

            request_type = dict_request["type"]

            if request_type.lower() == RequestTypeEnum.LaunchRequest.name.lower():
                output = RequestTypeEnum.LaunchRequest

            elif request_type.lower() == RequestTypeEnum.IntentRequest.name.lower():
                output = RequestTypeEnum.IntentRequest

            elif request_type.lower() == RequestTypeEnum.SessionEndedRequest.name.lower():
                output = RequestTypeEnum.SessionEndedRequest

        else:
            raise TypeError("The request type must be on one of the types in the RequestTypeEnum enum")

        return output


class Response(object):
    """ Helps the user to dynamically create the proper response to send to Alexa."""

    def __init__(self, session_attributes=None):
        
        self.SessionAttributes = SessionAttributes()

        if isinstance (session_attributes, SessionAttributes):
            self.SessionAttributes = session_attributes


    def tell_simple(self, speech_text):
        """Creates a response that will have Alexa respond with the provided text and end the session."""

        # Create the needed object using the values provided by the user
        out_speech = OutputSpeech(OutputSpeechTypeEnum.PlainText, speech_text)

        # Build the response and return it to the user
        return self.generate_response(out_speech)


    def tell_with_card_simple(self, speech_text, card_title, card_text):
        """Creates a response that will have Alexa respond with the provided text, create a simple card that will be sent to the users Alexa app and end the session."""

        # Create the needed objects using the values provided by the user
        out_speech = OutputSpeech(OutputSpeechTypeEnum.PlainText, speech_text)
        card = Card(CardTypeEnum.Simple, card_title, card_text)

        # Build the response and return it to the user
        return self.generate_response(out_speech, card)


    def tell_advanced(self, speech_text):
        """Creates a response that will have Alexa respond with the provided text in the SSML format and end the session."""

        # Create the needed object using the values provided by the user
        out_speech = OutputSpeech(OutputSpeechTypeEnum.SSML, speech_text)

        # Build the response and return it to the user
        return self.generate_response(out_speech)


    def tell_with_card_advanced(self, speech_text, card_title, card_text, card_image_small_url=None, card_image_large_url=None):
        """Creates a response that will have Alexa respond with the provided text in the SSML format. It also creates a standard card, which can contain images, that will be returned to the users Alexa App. Finally the session will be ended."""

        # Create the needed objects using the values provided by the user
        out_speech = OutputSpeech(OutputSpeechTypeEnum.SSML, speech_text)
        card = Card(CardTypeEnum.Standard, card_title, card_text)

        # Check that there are values for both small and large image urls
        if card_image_small_url is not None and card_image_large_url is not None:
            card.CardImage = CardImage(card_image_small_url, card_image_large_url)

        # Build the response and return it to the user
        return self.generate_response(out_speech, card)


    def ask_simple(self, speech_text, reprompt_text):
        """Creates a response that will have Alexa respond with the provided text and will keep the session alive to waiting for interaction from the user. Reprompts are implemented for when a user does not respond to the origional prompt ."""

        # Create the needed objects using the values provided by the user
        out_speech = OutputSpeech(OutputSpeechTypeEnum.PlainText, speech_text)
        reprompt = Reprompt(OutputSpeechTypeEnum.PlainText, reprompt_text)

        # Build the response and return it to the user
        return self.generate_response(out_speech, reprompt=reprompt, shouldEndSession=False)


    def ask_with_card_simple(self, speech_text, reprompt_text, card_title, card_text):
        """Creates a response that will have Alexa respond with the provided text and will keep the session alive to waiting for interaction from the user. Reprompts are implemented for when a user does not respond to the origional prompt. A simple card will also be sent to the users Alexa app with the provided content."""

        # Create the needed objects using the values provided by the user
        out_speech = OutputSpeech(OutputSpeechTypeEnum.PlainText, speech_text)
        card = Card(CardTypeEnum.Simple, card_title, card_text)
        reprompt = Reprompt(OutputSpeechTypeEnum.PlainText, reprompt_text)

        # Build the response and return it to the user
        return self.generate_response(out_speech, card, reprompt, shouldEndSession=False)


    def ask_advanced(self, speech_text, reprompt_text):
        """Creates a response that will have Alexa respond with the provided text in the SSML format, and will keep the session alive to waiting for interaction from the user. Reprompts are implemented in SSML for when a user does not respond to the origional prompt ."""

        # Create the needed objects using the values provided by the user
        out_speech = OutputSpeech(OutputSpeechTypeEnum.SSML, speech_text)
        reprompt = Reprompt(OutputSpeechTypeEnum.SSML, reprompt_text)

        # Build the response and return it to the user
        return self.generate_response(out_speech, reprompt=reprompt, shouldEndSession=False)


    def ask_with_card_advanced(self, speech_text, reprompt_text, card_title, card_text, card_image_small_url=None, card_image_large_url=None):
        """Creates a response that will have Alexa respond with the provided text in the SSML format, and will keep the session alive to waiting for interaction from the user. Reprompts are implemented in SSML, for when a user does not respond to the origional prompt. A Standard card will also be sent to the users Alexa app with the provided content. Standard cards alos allow users to provide images via HTTPS Urls to the images """

        # Create the needed objects using the values provided by the user
        out_speech = OutputSpeech(OutputSpeechTypeEnum.SSML, speech_text)
        card = Card(CardTypeEnum.Standard, card_title, card_text)
        reprompt = Reprompt(OutputSpeechTypeEnum.SSML, reprompt_text)

        # check if values have been provided for both small and large URL variables
        if card_image_small_url is not None and card_image_large_url is not None:
            card.CardImage = CardImage(card_image_small_url, card_image_large_url)

        # Build the response and return it to the user
        return self.generate_response(out_speech, card, reprompt, shouldEndSession=False)


    def generate_response(self, output_speech, card=None, reprompt=None, shouldEndSession=True):
        """Dynamically builds the response that will be sent to Alexa using the provided object. This is the function you will use if you want to create a request differnet that the provided ones. """

        session_attributes = self.SessionAttributes

        # output template that the response result is built from
        output = {
            "version": "1.0"
        }

        # Check if there are session attributes that need to be added to the response
        if session_attributes is not None:
            session_attributes_dictionary = self.__create_session_attributes(session_attributes)

            if session_attributes_dictionary is not None:
                output.update(session_attributes_dictionary)

        # Add a subnested dictionary for the response json
        output.update({"response": {}})

        # Variable to store the response section that was just added to the response 
        dict_response = output["response"]

        # Dynamically add sections to the response
        # Add outputSpeech section
        dict_response.update(self.__create_output_speech(output_speech))

        # If card info is provided then add the card section
        if card is not None:
            dict_response.update(self.__create_card(card))

        # If reprompt info is provided then add the reprompt section
        if reprompt is not None:
            dict_response.update(self.__create_reprompt(reprompt))

        dict_response.update({"shouldEndSession": bool(shouldEndSession)})

        # Returns the built response
        return output

    def __create_session_attributes(self, session_attributes):
        """Maps and builds the session attributes section of the response."""

        output = {
            "sessionAttributes": {
            }
        }

        # Check if the provided session attributes are the proper instance and is greater than 0
        if isinstance(session_attributes, SessionAttributes):

            if len(session_attributes.get_all()) > 0:

                # Gets all the session attributes from the collection and builds them into the output
                output["sessionAttributes"].update(session_attributes.get_all())

                # Returns the Session attributes section
                return output

            else:
                return None
        else:
            raise TypeError("The provided session attributes must be of type SessionAttribute")

    def __create_output_speech(self, output_speech):
        """Maps and builds the output speech section of the response."""

        # checks that the provided output_speech is the right type
        if isinstance(output_speech, OutputSpeech):

            output = None

            # Map the provide output speech type to it's corresponding enum value
            if output_speech.Type == OutputSpeechTypeEnum.PlainText:
                output = {
                    "outputSpeech": {
                        "type": "PlainText",
                        "text": output_speech.Text,
                    }
                }

            elif output_speech.Type == OutputSpeechTypeEnum.SSML:
                output = {
                    "outputSpeech": {
                        "type": "SSML",
                        "ssml": "<speak>" + str(output_speech.Text) + "</speak>",
                    }
                }

            else:
                raise ValueError("The provided speech type is invalid")

        # Return the output speech section
        return output

    def __create_reprompt(self, reprompt):
        """Maps and builds the reprompt section of the response."""

        # Checks if the reprompt is the correct instance type
        if isinstance(reprompt, Reprompt):
            output = None

            # Map the reprompt type to it's corresponding OutputSpeechTypeEnum enum, if mapping cannot be found an exception is raised
            if reprompt.Type == OutputSpeechTypeEnum.PlainText:
                output = {
                    "reprompt": {
                        "outputSpeech": {
                            "type": "PlainText",
                            "text": reprompt.Text,
                        }
                    }
                }

            elif reprompt.Type == OutputSpeechTypeEnum.SSML:
                output = {
                    "reprompt": {
                        "outputSpeech": {
                            "type": "SSML",
                            "ssml": "<speak>" + str(reprompt.Text) + "</speak>",
                        }
                    }
                }

            else:
                raise ValueError("The provided reprompt speech type is invalid")

        # Return the reprompt section
        return output

    def __create_card(self, card):
        """Maps and builds the card section of the response"""

        # check that the provided card is the right instance type
        if isinstance(card, Card):

            output = None

            # Create a concatenated string to perform validation checking on the length of all the card text
            validate_card_text_length = card.Title + card.Text

            # Check that the image urs are not greater than 2000 characters, Amazon does not permit either url to be greater than 2000 characters
            if card.CardImage is not None:
                
                if len(card.CardImage.SmallImageURL) < 2000 and len(card.CardImage.LargeImageURL) < 2000:

                    validate_card_text_length += card.CardImage.SmallImageURL + card.CardImage.LargeImageURL
                else:
                    raise ValueError("The total length of an image url exceeded the 2000 character limit")

            # Validate card text length, Amazon only permits the total length of all text properties for a card to be a maximum of 8000 characters
            if len(validate_card_text_length) > 8000:
                raise ValueError("The combined length of the text on the card exceeds the permitted 8000 character limit")

            # Map the card type to it's corresponding CardTypeEnum enum value and if mapping not found then raise an exception
            if card.Type == CardTypeEnum.Simple:
                output = {
                    "card": {
                        "type": "Simple",
                        "title": card.Title,
                        "content": card.Text
                    }
                }

            elif card.Type == CardTypeEnum.Standard:
                output = {
                    "card": {
                        "type": "Standard",
                        "title": card.Title,
                        "text": card.Text
                    }
                }

                # Check if the card image property is not none and if it is not then build the card image section
                if card.CardImage is not None:
                    imgObj = {
                        "image": {
                            "smallImageUrl": card.CardImage.SmallImageURL,
                            "largeImageUrl": card.CardImage.LargeImageURL
                        }
                    }

                    # Add the card image section to the card section
                    output["card"].update(imgObj)

            # Handing of LinkedAccountCards needs to be handled
            elif card.Type == CardTypeEnum.LinkAccount:
                raise Exception("LinkedAccount Card types are currently not supported within this framework, please check back later")
            else:
                raise ValueError("The provided card type is invalid")

        # Return the card section
        return output
