from flask import Flask, request, jsonify
from init_db import init_db
from db import (
    get_posts,
    create_post,
    get_post_by_id,
    get_comments_by_post_id,
    create_comment
)

app = Flask(__name__)
init_db()

# 공통 404 (POST_NOT_FOUND) 포맷
def post_not_found():
    return jsonify({
        "status_code": 404,
        "error": "POST_NOT_FOUND",
        "message": "존재하지 않는 게시글입니다."
    }), 404

# (옵션) 400 포맷 - 명세에는 없지만 제한조건(30/200) 지키려고 넣음
def bad_request(error_code: str, message: str):
    return jsonify({
        "status_code": 400,
        "error": error_code,
        "message": message
    }), 400


# 1. 게시글 전체 조회
@app.route("/api/posts", methods=["GET"])
def api_get_posts():
    posts = get_posts()
    return jsonify({"posts": posts}), 200


# 2. 게시글 작성
@app.route("/api/posts", methods=["POST"])
def api_create_post():
    data = request.get_json(silent=True) or {}
    title = data.get("title", "")
    content = data.get("content", "")

    # 제목 30자 제한 (요구사항)
    if len(title) == 0:
        return bad_request("TITLE_REQUIRED", "제목은 필수입니다.")
    if len(title) > 30:
        return bad_request("TITLE_TOO_LONG", "제목은 30자 이내여야 합니다.")

    # 내용 제한 없음(요구사항) - 빈 문자열은 허용/비허용 명세 없어서 허용해도 됨.
    create_post(title, content)

    # 명세: 200 + message
    return jsonify({"message": "성공적으로 등록됐습니다."}), 200


# 3. 게시글 개별 조회
@app.route("/api/posts/<int:post_id>", methods=["GET"])
def api_get_post(post_id):
    post = get_post_by_id(post_id)
    if post is None:
        return post_not_found()
    return jsonify(post), 200


# 4. 댓글 조회
@app.route("/api/posts/<int:post_id>/comment", methods=["GET"])
def api_get_comments(post_id):
    post = get_post_by_id(post_id)
    if post is None:
        return post_not_found()

    comments = get_comments_by_post_id(post_id)
    return jsonify({"comments": comments}), 200


# 5. 댓글 작성
@app.route("/api/posts/<int:post_id>/comment", methods=["POST"])
def api_create_comment(post_id):
    post = get_post_by_id(post_id)
    if post is None:
        return post_not_found()

    data = request.get_json(silent=True) or {}
    content = data.get("content", "")

    # 댓글 200자 제한 (요구사항)
    if len(content) == 0:
        return bad_request("COMMENT_REQUIRED", "댓글 내용은 필수입니다.")
    if len(content) > 200:
        return bad_request("COMMENT_TOO_LONG", "댓글은 200자 이내여야 합니다.")

    create_comment(post_id, content)

    # 명세: 200 + message
    return jsonify({"message": "성공적으로 등록됐습니다."}), 200


if __name__ == "__main__":
    app.run(debug=True)
