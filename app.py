from flask import Flask, render_template
from RefForm import RefForm
from Comparator import Comparator

app = Flask(__name__)
server = app.server
app.secret_key = 'secret'

def getData(comparator):
    comparator.all_comparator(comparator)
    data = comparator.data
    return data

@app.route('/', methods=['GET', 'POST'])
def index():
    form = RefForm()
    if form.validate_on_submit():
        ref = form.ref.data
        comparator = Comparator(ref)
        return render_template('index.html', form=form, data=getData(comparator), best_price=comparator.getBestPrice())
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
