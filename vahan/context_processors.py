from .secrets import CLIENT_ID, CLIENT_SECRET

def secret_keys_processor(request):
    return {
        'clientId': CLIENT_ID,
        'clientSecret': CLIENT_SECRET,
    }
