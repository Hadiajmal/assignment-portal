from flask import Flask, request, redirect, url_for, render_template_string
from urllib.parse import urlparse

app = Flask(__name__)
submissions = []

PAGE = """
<h2>Assignment Submission Portal</h2>
<form method="post">
  Name: <input name="name"><br><br>
  Reg No: <input name="reg_no"><br><br>
  Assignment Title: <input name="title"><br><br>
  Submission URL: <input name="url"><br><br>
  <button>Submit</button>
</form>
{% if error %}<p style="color:red">{{ error }}</p>{% endif %}
<h3>Submissions</h3>
<ul>
{% for s in submissions %}
  <li>{{ s.name }} ({{ s.reg_no }}) - {{ s.title }} - <a href="{{ s.url }}">{{ s.url }}</a></li>
{% endfor %}
</ul>
"""

def valid_url(u):
    p = urlparse(u or "")
    return p.scheme in ("http", "https") and bool(p.netloc) and "." in p.netloc

def validate(d):
    labels = {"name": "name", "reg_no": "registration number",
              "title": "assignment title", "url": "submission URL"}
    for f in labels:
        if not (d.get(f) or "").strip():
            return "Missing " + labels[f]
    if not valid_url(d["url"]):
        return "Invalid submission URL"
    return None

@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    if request.method == "POST":
        error = validate(request.form)
        if not error:
            submissions.append({k: request.form[k].strip()
                                for k in ("name", "reg_no", "title", "url")})
            return redirect(url_for("index"))
    return render_template_string(PAGE, submissions=submissions, error=error)

if __name__ == "__main__":
    app.run(port=5000)