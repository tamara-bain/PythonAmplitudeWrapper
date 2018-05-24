Little Python Wrapper for Amplitudes API
========================================

This wrapper class allows users to interact with amplitudes http api and amplitude identify api.
It simplifies sending events to amplitude, accessing user properties, and pulling amplitude events.

### Getting Started

You can add this to your project by including the github repo url with pip:
`pip install git+https://github.com/Tamarabyte/PythonAmplitudeWrapper`

You will need to specify your amplitude api keys as environmental variables:

    export AMPLITUDE_API_KEY="ASASA99AABLAH"
    export AMPLITUDE_API_SECRET_KEY="ASASECRETBLAH"

### Example Uses

You can identify users as follows:

    from amplitude_wrapper import AmplitudeWrapper
    wrapper = AmplitudeWrapper()

    # sets the user property to the specified value for the amplitude user 'test@test.com'
    wrapper.set_user_properties('test@test.com', {'COUNTRY' : 'Canada'})

You can send events as follows:

    from amplitude_wrapper import AmplitudeWrapper
    wrapper = AmplitudeWrapper()

    # sends the 'click-button' event for amplitude user test@test.com
    wrapper.send_event('test@test.com', 'click-button', {'BUTTON-TEXT' : 'ok'})

You can also initialize global properties that will be sent out with all events
for this instance of the wrapper:

    from amplitude_wrapper import AmplitudeWrapper
    wrapper = AmplitudeWrapper({'DAY_OF_THE_WEEK' : 'monday'})

You can retrieve events from amplitude over a series of days:

    from amplitude_wrapper import AmplitudeWrapper
    wrapper = AmplitudeWrapper()

    # gets the events per day for the last 5 days
    # if the optional 'end' parameter is not specified defaults to
    # end = datetime.now()
    # returns an array of events per day up to and including the end day eg ([0, 0, 1, 0, 5])
    wrapper.get_unique_event_count_per_day('click-button', 5)