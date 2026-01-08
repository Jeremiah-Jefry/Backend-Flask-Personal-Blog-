from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('blog.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts')
def posts():
    conn = get_db()
    all_posts = conn.execute('SELECT * FROM posts ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('posts.html', posts=all_posts)

@app.route('/create-post', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        if not title or not content:
            return render_template('create_post.html', error='Title and content are required!')
        
        conn = get_db()
        conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
        conn.commit()
        conn.close()
        return redirect(url_for('posts'))
    
    return render_template('create_post.html')

@app.route('/post/<int:id>')
def post_detail(id):
    conn = get_db()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if post is None:
        return "Post not found", 404
    
    return render_template('post_detail.html', post=post)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    conn = get_db()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (id,)).fetchone()
    
    if post is None:
        return "Post not found", 404
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        if not title or not content:
            return render_template('edit_post.html', post=post, error='Title and content are required!')
        
        conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (title, content, id))
        conn.commit()
        conn.close()
        return redirect(url_for('post_detail', id=id))
    
    conn.close()
    return render_template('edit_post.html', post=post)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_post(id):
    conn = get_db()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('posts'))

if __name__ == '__main__':
    app.run(debug=True)
