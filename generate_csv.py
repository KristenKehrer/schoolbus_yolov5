import pytz
import boto3
import os

os.environ['AWS_SHARED_CREDENTIALS_FILE'] = '.aws_credentials'

resp = boto3.client('s3').list_objects_v2(
    Bucket='bus-detector',
    Prefix='images/'
)


def get_row_from_s3_img(img):
    local = img['LastModified'].astimezone(pytz.timezone('America/New_York'))
    return {
        'timestamp': local.isoformat(),
        'img_url': f'https://bus-detector.s3.amazonaws.com/{img["Key"]}',
        'class': img['Key'].split('_')[-1].split('.')[0]
    }


images = resp['Contents']
images.sort(reverse=True, key=lambda e: e['LastModified'])
rows = list(map(get_row_from_s3_img, images))

lines = ['timestamp,image_url,class']
for row in rows:
    lines.append(f'{row["timestamp"]},{row["img_url"]},{row["class"]}')

file = open('data.csv', 'w')
file.write('\n'.join(lines) + '\n')
