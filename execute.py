from jinja2 import Environment, PackageLoader, select_autoescape
from metalink.metalink import Video
import os
import yaml
# Envirorment for Jinja templates
env = Environment(
    loader=PackageLoader("metalink"),
    autoescape=select_autoescape()
)
index_template = env.get_template("index.html")
image_template = env.get_template("image.html")


def render_index_html(video_obj):
    rendered_html = index_template.render(og_title=video_obj.title, og_description=video_obj.description, channel_domain=video_obj.domain, video_id=video_obj.id, og_image=video_obj.thumbnail_URL, keywords=video_obj.keywords)
    video_obj.index_html= rendered_html
    return rendered_html

def render_image_html(video_obj):
    rendered_html = image_template.render(image_URL=video_obj.thumbnail_URL)
    video_obj.image_html = rendered_html
    return rendered_html


with open("video_list.yaml", 'r') as stream:
    try:
        video_list = yaml.safe_load(stream)["videos"]
    except yaml.YAMLError as exc:
        print(exc)

def output(video_id, rendered_html, image=False):
    if image == True:
        outF = open(video_id + "/image/index.html", "w")
        outF.writelines(rendered_html)
        outF.close()
    else:
        outF = open(video_id + "/index.html", "w")
        outF.writelines(rendered_html)
        outF.close()


def yaml_processor(video_obj):
    video_yaml = dict()
    video_yaml.update({"id": video_obj.id})
    video_yaml.update({"title": video_obj.title})
    video_yaml.update({"description": video_obj.description})
    video_yaml.update({"keywords": video_obj.keywords})
    video_yaml.update({"thumbnail": video_obj.thumbnail_URL})
    os.system("touch " + "/"+video_obj.id+"/video.yaml")
    with open(video_obj.id + "/video.yaml", 'w') as file:
        yaml.safe_dump(video_yaml, file)
    file.close()


    return video_yaml

if __name__ == '__main__':
    os.system("git stash")
    for x in video_list:
        object=Video(x)
        render_index_html(object)
        render_image_html(object)
        os.system("git checkout release")
        os.system("rm -Rf " + object.id)
        os.mkdir(object.id)
        os.mkdir(object.id+"/image")
        yaml_processor(object)
        output(object.id,object.index_html)
        output(object.id,object.image_html, image=True)
        commit_message = ' '.join((object.id, object.title,"\n",object.description))
        os.system('git add *')
        os.system("git commit -a -m 'updated redirects'")
        os.system("git checkout main")
        os.system("rm -Rf " + object.id)
    os.system("git stash pop")


