import os
import shutil
from jinja2 import Environment, PackageLoader

def clean_build_folder():
    if os.path.exists('build'):
        shutil.rmtree('build')
    os.makedirs('build')
    os.makedirs('build/posts')

def build():
    posts = []
    env = Environment(loader=PackageLoader('blog', 'templates'))
    for template in os.listdir('templates/posts'):
        t = env.get_template('posts/{}'.format(template))
        posts.append({'posted': t.module.posted(), 
                      'title': t.module.title(),
                      'filename': os.path.split(t.filename)[1]})
        with open('build/posts/{}'.format(template), "wb") as f:
            f.write(bytes(t.render(), "utf-8"))
    
    posts = sorted(posts, key=lambda k: k['posted'], reverse=True)
    t = env.get_template('index.html')
    with open('build/index.html', "wb") as f:
        f.write(bytes(t.render(posts=posts), "utf-8"))

    shutil.copytree('static', 'build/static')

if __name__ == "__main__":
    clean_build_folder()
    build()
