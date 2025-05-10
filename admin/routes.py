from flask import Blueprint, render_template, redirect, session, request, url_for
from database import  get_db
from passlib.hash import sha256_crypt
from itsdangerous import URLSafeTimedSerializer
import datetime

admin_bp = Blueprint(
    "admin", 
    __name__,
    url_prefix="/admin",
    template_folder="templates/admin"
    )

# 生成 Token 工具
def generate_reset_token(email, secret_key):
    s = URLSafeTimedSerializer(secret_key)
    return s.dumps(email, salt="password-reset")

# 解码 Token 工具
def verify_reset_token(token, secret_key, max_age=3600):
    s = URLSafeTimedSerializer(secret_key)
    try:
        email = s.loads(token, salt="password-reset", max_age=max_age)
        return email
    except Exception:
        return None
        
@admin_bp.route("/edit-page/<slug>")
def edit_page(slug):
    db = get_db()
    blocks = db.execute("SELECT * FROM page_content_block WHERE tab_slug = ?", (slug,)).fetchall()
    db.close()
    return render_template("edit_page.html", blocks=blocks)


@admin_bp.route("/dashboard")
def dashboard():
    if "admin" not in session:
        return redirect(url_for("admin.login"))
    return render_template("dashboard.html")


@admin_bp.route("/users")
def list_users():
    if "admin" not in session:
        return redirect(url_for("admin.login"))
    db = get_db()
    users = db.execute("SELECT * FROM admin_user").fetchall()
    db.close()
    return render_template("users.html", users=users)


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        user = db.execute("SELECT * FROM admin_user WHERE username = ?", (username,)).fetchone()
        db.close()

        if user and sha256_crypt.verify(password, user["password"]):
            session["admin"] = user["id"]
            return redirect(url_for("admin.dashboard"))
        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


@admin_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("admin.login"))


@admin_bp.route("/forget_password", methods=["GET", "POST"])
def forget_password():
    if request.method == "POST":
        email = request.form["email"]

        db = get_db()
        user = db.execute("SELECT * FROM admin_user WHERE username = ?", (email,)).fetchone()

        if user:
            token = generate_reset_token(email, secret_key="your-secret-key")
            reset_url = f"http://localhost:5000/admin/reset-password?token={token}"

            # 模拟发送邮件，打印链接
            print(f"Password reset link for {email}: {reset_url}")

            # 存 token（可选）
            db.execute("UPDATE admin_user SET reset_token = ?, reset_token_expiry = ? WHERE username = ?",
                       (token, datetime.datetime.now() + datetime.timedelta(hours=1), email))
            db.commit()

        db.close()
        return render_template("forget_password.html", success="If this email exists, a reset link was sent.")

    return render_template("forget_password.html")


@admin_bp.route("/register", methods=["GET", "POST"], endpoint="register")
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = sha256_crypt.hash(request.form["password"])
        email = request.form["email"]

        db = get_db()
        db.execute("INSERT INTO admin_user (username, password, email) VALUES (?, ?, ?)", (username, password, email))
        db.commit()
        db.close()

        return redirect(url_for("admin.login"))  # 注册成功后跳转到登录页

    return render_template("register.html")

@admin_bp.route("/edit_password", methods=["GET", "POST"])
def edit_password():
    if "admin" not in session:
        return redirect(url_for("admin.login"))

    if request.method == "POST":
        current_password = request.form["current_password"]
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        if new_password != confirm_password:
            return render_template("edit_password.html", error="Passwords do not match")

        db = get_db()
        user = db.execute("SELECT * FROM admin_user WHERE id = ?", (session["admin"],)).fetchone()

        if not sha256_crypt.verify(current_password, user["password"]):
            db.close()
            return render_template("edit_password.html", error="Current password incorrect")

        hashed_password = sha256_crypt.hash(new_password)
        db.execute("UPDATE admin_user SET password = ? WHERE id = ?", (hashed_password, session["admin"]))
        db.commit()
        db.close()

        return render_template("edit_password.html", success="Password updated successfully")

    return render_template("edit_password.html")

@admin_bp.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    token = request.args.get("token")
    email = verify_reset_token(token, secret_key="your-secret-key")

    if not email:
        return "Invalid or expired token", 400

    if request.method == "POST":
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        if new_password != confirm_password:
            return render_template("admin/reset_password.html", error="Passwords do not match")

        hashed_password = sha256_crypt.hash(new_password)
        db = get_db()
        db.execute("UPDATE admin_user SET password = ?, reset_token = NULL, reset_token_expiry = NULL WHERE username = ?",
                   (hashed_password, email))
        db.commit()
        db.close()

        return redirect(url_for("admin.login"))

    return 	render_template("admin/reset_password.html")

@admin_bp.route("/edit-user/<int:user_id>", methods=["GET", "POST"])
def edit_admin_user(user_id):
    if "admin" not in session:
        return redirect(url_for("admin.login"))

    db = get_db()

    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        db.execute("UPDATE admin_user SET username = ?, email = ? WHERE id = ?", (username, email, user_id))
        db.commit()
        db.close()
        return redirect(url_for("admin.list_users"))

    user = db.execute("SELECT * FROM admin_user WHERE id = ?", (user_id,)).fetchone()
    db.close()
    if not user:
        return "User not found", 404

    return render_template("edit_admin_user.html", user=user)

@admin_bp.route("/delete-user/<int:user_id>")
def delete_admin_user(user_id):
    if "admin" not in session:
        return redirect(url_for("admin.login"))

    db = get_db()
    db.execute("DELETE FROM admin_user WHERE id = ?", (user_id,))
    db.commit()
    db.close()
    return redirect(url_for("admin.list_users"))


