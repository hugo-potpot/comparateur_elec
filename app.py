from flask import Flask, render_template
from Formulaire.RefForm import RefForm, InfoForm
from Comparator import Comparator
from database import Database

app = Flask(__name__)
app.secret_key = 'secret'

def getData(comparator):
    comparator.all_comparator(comparator)
    data = comparator.tmp
    return data

@app.route('/', methods=['GET', 'POST'])
def index():
    form = RefForm()
    form_search = InfoForm()
    if form.validate_on_submit():
        ref = form.ref.data
        comparator = Comparator(ref)
        return render_template('index.html', form=form, data=getData(comparator), best_price=comparator.getBestPrice(ref))
    if form_search.validate_on_submit():
        info = form_search.info.data
        return render_template('index.html', form_search=form_search, form=form, search_produit=Database().get_info_by_search(info))
    return render_template('index.html', form=form, form_search=form_search, data=[])

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
