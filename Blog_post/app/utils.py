
def convert_title_to_url(title: str):
     '''convert title to url slug'''
     return "".join(ch for ch in title if ch.isalnum() or ch.isspace()).replace(" ",'-')
