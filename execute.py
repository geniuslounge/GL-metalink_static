from jinja2 import Environment, PackageLoader, select_autoescape
from metalink.metalink import Video
import os
import yaml
env = Environment(
    loader=PackageLoader("metalink"),
    autoescape=select_autoescape()
)
template = env.get_template("index.html")


def render_html(video_obj):
    rendered_html = template.render(og_title=video_obj.title, og_description=video_obj.description, channel_domain=video_obj.domain, video_id=video_obj.id, og_image=video_obj.thumbnail_URL, keywords=video_obj.keywords)
    video_obj.rendered_html= rendered_html
    return rendered_html
with open("video_list.yaml", 'r') as stream:
    try:
        video_list = yaml.safe_load(stream)["videos"]
    except yaml.YAMLError as exc:
        print(exc)

def output(video_id, rendered_html):
    outF = open(video_id+"/index.html", "w")
    outF.writelines(rendered_html)
    outF.close()

if __name__ == '__main__':
    os.system("git stash")

    for x in video_list:
        object=Video(x)
        render_html(object)
        os.system("git checkout release")
        os.system("rm -Rf " + object.id)
        os.mkdir(object.id)
        os.mkdir(object.id+"/image")
        output(object.id,object.rendered_html)
        commit_message = ' '.join((object.id, object.title,"\n",object.description))
        os.system('git add *')
        os.system("git commit -a -m 'updated redirects'")
    os.system("git checkout main")
