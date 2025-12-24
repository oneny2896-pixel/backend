import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("app.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# 게시글 전체 조회
def get_posts():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, title, content, create_date FROM posts ORDER BY id ASC")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

# 게시글 작성
def create_post(title: str, content: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO posts (title, content, create_date) VALUES (?, ?, date('now'))",
        (title, content)
    )
    conn.commit()
    post_id = cur.lastrowid
    conn.close()
    return post_id

# 게시글 단건 조회
def get_post_by_id(post_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, title, content, create_date FROM posts WHERE id = ?", (post_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

# 댓글 목록 조회 (명세에서 post 키로 "post": post_id 넣어야 함)
def get_comments_by_post_id(post_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, content, create_date
        FROM comments
        WHERE post_id = ?
        ORDER BY id ASC
        """,
        (post_id,)
    )
    rows = cur.fetchall()
    conn.close()

    comments = []
    for r in rows:
        d = dict(r)
        d["post"] = post_id
        comments.append(d)
    return comments

# 댓글 작성
def create_comment(post_id: int, content: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO comments (content, create_date, post_id) VALUES (?, date('now'), ?)",
        (content, post_id)
    )
    conn.commit()
    comment_id = cur.lastrowid
    conn.close()
    return comment_id
