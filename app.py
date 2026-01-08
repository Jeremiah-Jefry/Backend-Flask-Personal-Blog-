from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Database connection helper (Session 3)
def get_db_connection():
    conn = sqlite3.connect('blog.db')
    conn.row_factory = sqlite3.Row
    return conn

# ========================================
# SESSION 1: Backend Basics & Routes
# ========================================

@app.route('/')
def index():
    """Home page - Session 1"""
    return render_template('index.html')

@app.route('/about')
def about():
    """About page - Session 1"""
    return render_template('about.html')

@app.route('/hello/<name>')
def hello(name):
    """Dynamic route practice - Session 1"""
    return f"Hello, {name}! Welcome to my blog!"

# ========================================
# SESSION 2: Forms & Templates
# ========================================

@app.route('/create-post', methods=('GET', 'POST'))
def create_post():
    """Create new blog post - Session 2"""
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        tags = request.form.get('tags', '')
        
        # Simple validation (Session 2)
        if not title or not content:
            return render_template('create_post.html', 
                                 error='Title and content are required!')
        
        # For now: just show success (Session 2)
        # Session 3: Save to database
        return render_template('create_post.html', 
                             success='Post created successfully!')
    
    return render_template('create_post.html')

# ========================================
# SESSION 3: Database Integration
# ========================================

@app.route('/posts')
def posts():
    """Show all posts - Session 3"""
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('posts.html', posts=posts)

@app.route('/create-post', methods=('GET', 'POST'))
def create_post_db():
    """Create post with DATABASE - Session 3"""
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        tags = request.form.get('tags', '')
        
        if not title or not content:
            return render_template('create_post.html', 
                                 error='Title and content are required!')
        
        # INSERT into database (Session 3)
        conn = get_db_connection()
        conn.execute('INSERT INTO posts (title, content, tags) VALUES (?, ?, ?)',
                    (title, content, tags))
        conn.commit()
        conn.close()
        
        return redirect(url_for('posts'))
    
    return render_template('create_post.html')

# ========================================
# SESSION 4: Full CRUD Mini Project
# ========================================

@app.route('/post/<int:id>')
def post_detail(id):
    """View single post - Session 4"""
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if post is None:
        return "Post not found", 404
    
    return render_template('post_detail.html', post=post)

@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit_post(id):
    """Edit post - Session 4"""
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (id,)).fetchone()
    
    if post is None:
        return "Post not found", 404
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        tags = request.form.get('tags', '')
        
        conn.execute('UPDATE posts SET title = ?, content = ?, tags = ? WHERE id = ?',
                    (title, content, tags, id))
        conn.commit()
        conn.close()
        return redirect(url_for('post_detail', id=id))
    
    conn.close()
    return render_template('edit_post.html', post=post)

@app.route('/delete/<int:id>', methods=('POST',))
def delete_post(id):
    """Delete post - Session 4"""
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('posts'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
