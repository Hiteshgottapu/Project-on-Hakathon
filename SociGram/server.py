from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample list to store posts
posts = []

@app.route('/posts', methods=['GET', 'POST', 'DELETE'])
def handle_posts():
    if request.method == 'GET':
        return jsonify(posts)
    elif request.method == 'POST':
        data = request.get_json()
        if 'content' in data:
            posts.append(data['content'])
            return 'Post created', 201
    elif request.method == 'DELETE':
        index = request.args.get('index')
        if index and index.isdigit() and 0 <= int(index) < len(posts):
            deleted_post = posts.pop(int(index))
            return f'Deleted post: {deleted_post}', 200
        return 'Invalid index', 400

if __name__ == '__main__':
    app.run(debug=True)
