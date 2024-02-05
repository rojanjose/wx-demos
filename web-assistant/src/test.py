import re
import json

def to_camel_case(text):
    words = text.split('_')
    return words[0].lower() + ''.join(word.capitalize() for word in words[1:])


# file_name = "L3-topic_0TO3n000000RZiaGAG_team_settings.html"

# matched_string = re.search('topic_(.*?)_', file_name )

# if matched_string:
#     extracted_string = matched_string.group(1)
#     print(extracted_string)

# matched_string = re.search(f'{extracted_string}_(.*?).html', file_name )

# if matched_string:
#     extracted_string = matched_string.group(1)
#     print(extracted_string)

# # print(extracted_string.title())

# print(' '.join(word.capitalize() for word in extracted_string.split('_')))

# matched_string = file_name.split(f'{extracted_string}_')[1]
# print(matched_string)

# print(re.search(f'{file_metadata["id"]}_(.*)_', file_name).string())


file_path = '../scrapper/scraped-pages/toc.json'

# Open the JSON file and load its content into a dictionary
with open(file_path, 'r') as file:
    toc = json.load(file)


for line in toc:
    print(line["filename"])

