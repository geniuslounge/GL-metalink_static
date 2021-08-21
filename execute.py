from jinja2 import Environment, PackageLoader, select_autoescape
from metalink.metalink import Video
import yaml
env = Environment(
    loader=PackageLoader("metalink"),
    autoescape=select_autoescape()
)
template = env.get_template("index.html")


def render_html(video_obj):
    return template.render(og_title=video_obj.title, og_description=video_obj.description, channel_domain=video_obj.domain, video_id=video_obj.id, og_image=video_obj.thumbnail_URL, keywords=video_obj.keywords)

if __name__ == '__main__':
    with open("video_list.yaml", 'r') as stream:
        try:
            video_list = yaml.safe_load(stream)["videos"]
        except yaml.YAMLError as exc:
            print(exc)
    video_objects=[]
    for x in video_list:
        video_object = Video(x)
        print(video_object.title)
        print(video_object.description)
        print(video_object.domain)
        print(video_object.id)
        print(video_object.thumbnail_URL)
        print(video_object.keywords)
        print(video_object.URL)
        print(render_html(video_object))