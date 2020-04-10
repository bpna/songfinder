from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from forms import SearchForm
from scraper import SongScraper

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'a-023hr0983iuooianf0987g1'

@app.route('/', methods=['GET', 'POST'])
def index():
  form = SearchForm()
  results = None
  scraper = SongScraper()
  if form.validate_on_submit():
      results = scraper.search_lyric(form.lyric.data)
      form.lyric.data = ''
  return render_template('index.html', form=form, results=results)

if __name__ == '__main__':
    app.run(debug=True)
