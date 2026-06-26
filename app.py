from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


def fetch_post_by_id(post_id):
    """
    Fetch a specific blog post from the JSON database by its ID.

    Args:
        post_id (int): The unique identifier of the blog post.

    Returns:
        dict, None, or tuple: The post dictionary if found, None if the post
                              does not exist, or an error tuple ("Message", 404)
                              if the data file is missing.
    """
    try:
        with open('data.json', 'r', encoding='utf-8') as file:
            blog_posts = json.load(file)
            post = next((post for post in blog_posts if post['id'] == post_id), None)

    except FileNotFoundError:
        return "Blog post not found", 404

    return post


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Handle the creation of a new blog post.

    Supports both GET and POST methods:
    - GET: Renders the 'add.html' form template.
    - POST: Extracts 'author', 'title', and 'content' from the submitted form,
            generates a new unique ID, appends the post to 'data.json',
            and redirects to the index page.

    Returns:
        str, Response, or tuple: The rendered HTML template (GET), a redirect
                                 to the index route (POST), or an error message
                                 with HTTP 404 if 'data.json' is missing.
    """
    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')
        try:
            with open('data.json', 'r', encoding='utf-8') as file:
                blog_posts = json.load(file)

        except FileNotFoundError:
            return "Data file not found", 404

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
    """
    Delete an existing blog post by its ID.

    Accepts only POST requests for safety. Reads the current posts from 'data.json',
    filters out the post matching the given ID, overwrites the file with the
    updated list, and redirects to the index page.

    Args:
        post_id (int): The unique identifier of the post to be deleted.

    Returns:
        Response or tuple: A redirect to the index route upon success, or an
                           error message with HTTP 404 if 'data.json' is missing.
    """
    try:
        with open('data.json', 'r', encoding='utf-8') as file:
            blog_posts = json.load(file)
            refreshed_blog_posts = [post for post in blog_posts if post['id'] != post_id]

    except FileNotFoundError:
        return "Data file not found", 404

    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(refreshed_blog_posts, file, ensure_ascii=False, indent=4)

    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
    Handle updating the details of an existing blog post.

    Supports both GET and POST methods:
    - GET: Fetches the post data and renders 'update.html' pre-filled with current values.
    - POST: Extracts updated form data, replaces the old post in 'data.json'
            while keeping the same ID, and redirects to the index page.

    Args:
        post_id (int): The unique identifier of the post to be updated.

    Returns:
        str, Response, or tuple: The rendered HTML template (GET), a redirect
                                 to the index route (POST), or an error message
                                 with HTTP 404 if the post or file is not found.
    """
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
            return "Data file not found", 404

        blog_posts = [updated_post if post['id'] == post_id else post for post in blog_posts]

        with open('data.json', 'w', encoding='utf-8') as file:
            json.dump(blog_posts, file, ensure_ascii=False, indent=4)

        return redirect(url_for('index'))

    return render_template('update.html', post=post)


@app.route('/')
def index():
    """
    Display the main blog index page.

    Loads all blog posts from 'data.json' and passes them to the 'index.html'
    template to render the home page list.

    Returns:
        str or tuple: The rendered HTML template for the index page, or an
                      error message with HTTP 404 if 'data.json' is missing.
    """
    try:
        with open('data.json', 'r', encoding='utf-8') as file:
            blog_posts = json.load(file)

    except FileNotFoundError:
        return "Data file not found", 404

    return render_template('index.html', posts=blog_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)