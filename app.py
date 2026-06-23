from flask import Flask, render_template, request, redirect, url_for
import json
app = Flask(__name__)


def fetch_post_by_id(post_id):
    with open('data.json', 'r', encoding='utf-8') as file:
        blog_posts = json.load(file)

        post = next((post for post in blog_posts if post['id'] == post_id), None)
        return post


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        with open('data.json', 'r', encoding='utf-8') as file:
            blog_posts = json.load(file)

        new_id = blog_posts[-1]['id'] + 1 if blog_posts else 1

        new_post = {
            "id": new_id,
            "author": author,
            "title": title,
            "content": content
        }

        blog_posts.append(new_post)

        with open('data.json', 'w', encoding='utf-8') as file:
            json.dump(blog_posts, file, ensure_ascii=False, indent=4)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    with open('data.json', 'r', encoding='utf-8') as file:
        blog_posts = json.load(file)
        refreshed_blog_posts = [post for post in blog_posts if post['id'] != post_id]

    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(refreshed_blog_posts, file, ensure_ascii=False, indent=4)

    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        updated_post =  {
            "id": post_id,
            "author": author,
            "title": title,
            "content": content
        }

        try:
            with open('data.json', 'r', encoding='utf-8') as file:
                blog_posts = json.load(file)

        except (FileNotFoundError, json.JSONDecodeError):
            blog_posts = []

        blog_posts = [updated_post if post['id'] == post_id else post for post in blog_posts]

        with open('data.json', 'w', encoding='utf-8') as file:
            json.dump(blog_posts, file, ensure_ascii=False, indent=4)

        return redirect(url_for('index'))

    return render_template('update.html', post=post)


@app.route('/')
def index():
    with open('data.json', 'r', encoding='utf-8') as file:
        blog_posts = json.load(file)

    return render_template('index.html', posts=blog_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)


