from flask import Flask, request, render_template_string, redirect, url_for
import random
import string

app = Flask(__name__)
short_links = {}

HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Rút Gọn Link</title>
  <style>
    body {
      margin: 0;
      font-family: 'Segoe UI', sans-serif;
      background: radial-gradient(ellipse at center, #0d0d1a 0%, #000010 100%);
      color: white;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 30px;
    }

    h1 {
      font-size: 2.2em;
      margin-bottom: 10px;
    }

    form {
      display: flex;
      flex-direction: column;
      width: 90%;
      max-width: 400px;
    }

    input[type="url"] {
      padding: 12px;
      border: none;
      border-radius: 10px;
      margin-bottom: 15px;
      font-size: 1em;
      outline: none;
    }

    button {
      background: #7a00ff;
      border: none;
      border-radius: 10px;
      color: white;
      padding: 12px;
      font-size: 1em;
      cursor: pointer;
      transition: 0.3s;
    }

    button:hover {
      background: #a84bff;
    }

    .result {
      margin-top: 25px;
      font-size: 1.1em;
      opacity: 1;
    }

    @media (max-width: 500px) {
      h1 { font-size: 1.7em; }
    }
  </style>
</head>
<body>
  <h1>Rút Gọn Link</h1>
  <form method="POST">
    <input type="url" name="url" placeholder="Dán link vào đây..." required />
    <button type="submit">Rút gọn</button>
  </form>

  {% if short %}
  <div class="result" id="linkBox">
    🔗 <a href="{{ short }}" target="_blank" style="color:#00f0ff">{{ short }}</a>
  </div>
  {% endif %}

  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
  <script>
    const linkBox = document.getElementById("linkBox");
    if (linkBox) {
      gsap.from(linkBox, { opacity: 0, y: 20, duration: 1 });
      setTimeout(() => {
        gsap.to(linkBox, { opacity: 0, y: -20, duration: 1, onComplete: () => linkBox.remove() });
      }, 5000);
    }
  </script>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    short_url = ''
    if request.method == 'POST':
        full_url = request.form['url']
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
        short_links[code] = full_url
        short_url = request.host_url + code
    return render_template_string(HTML, short=short_url)

@app.route('/<code>')
def redirect_short(code):
    url = short_links.get(code)
    return redirect(url) if url else 'Liên kết không tồn tại', 404

if __name__ == '__main__':
    app.run(debug=True)
