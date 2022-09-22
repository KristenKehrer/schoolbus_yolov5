import os


def write_credential_file(filepath, inputs, template):
    """Generic function for writing a credentials file"""

    # If the filepath exists, we don't have to do anything
    if os.path.exists(filepath):
        print(f'Credential file {filepath} exists. All set!')
        return

    # Loop through the inputs prompts, and have the user enter the value
    # to save in input_values
    input_values = []
    for i in inputs:
        input_values.append(input(i + ':'))

    # Create the config contents with str.format()
    # "{}:{}".format('kristen', 4) => "kristen:4"
    content = template.format(*input_values)

    # Open a file for writing
    with open(filepath, 'w', encoding='utf-8') as file:
        # Write the contents to the file
        file.write(content)
    print(f'Wrote credentials to {filepath}')


def setup_credentials():

    # Set up API Key and project name for Comet
    write_credential_file(
        '.comet.config',
        [
            'Enter your Comet API key',
            'Enter your Comet project name'
        ],
        '[comet]\napi_key = {}\nproject_name = {}\n')

    # Set up the api key for Roboflow
    write_credential_file(
        '.roboflow_api_key',
        ['Enter your Roboflow API key'],
        '{}')

    # Set up the Access Key Id / Secret for AWS access
    write_credential_file(
        '.aws_credentials',
        [
            'Enter your AWS Access Key ID',
            'Enter your AWS Secret Access Key'
        ],
        '[default]\naws_access_key_id={}\naws_secret_access_key={}\nregion=us-east-1\n')

    # Set up the username:password for the webcam RTSP url
    write_credential_file(
        '.camera_credentials',
        [
            'Enter the webcam username',
            'Enter the webcam password'
        ],
        '{}:{}\n')


# When this script is run, start with setup_credentials()
setup_credentials()
