
# Go to https://github.com/settings/developers

# Add a New OAuth2 App 

# Then copy the client_key and secret to this file

SOCIAL_AUTH_GITHUB_KEY = 'a18f15baa3d347f746f8'
SOCIAL_AUTH_GITHUB_SECRET = '56b532d3f766f92c3a8c52c7552e4c2110ba2073'

# Ask for the user's email (don't edit this line)
SOCIAL_AUTH_GITHUB_SCOPE = ['user:email']

# Note you may not get email for github users that don't make their
# email public - that is OK

# For detail: https://readthedocs.org/projects/python-social-auth/downloads/pdf/latest/

# Using ngrok is hard because the url changes every time you start ngrok

# If you are running on localhost, here are some settings:

# Application name: Your app name
# Homepage Url: http://localhost:8000
# Application Description: Whatever
# Authorization callback URL: http://127.0.0.1:8000/oauth/complete/github/