from flask import Flask, render_template, redirect, request
from models import db, Flavor, Inventory, Suggestion

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///choco_house.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/flavors/add/', methods=['GET', 'POST'])
def add_flavor():
    if request.method == 'POST':
        name = request.form['name']
        seasonal = request.form['seasonal']
        new_flavor = Flavor(name=name, seasonal=seasonal)
        db.session.add(new_flavor)
        db.session.commit()
        return redirect('/flavors/')
    return render_template('add_flavor.html')

@app.route('/flavors/')
def view_flavors():
    flavors = Flavor.query.all()
    return render_template('view_flavors.html', flavors=flavors)

@app.route('/inventory/add/', methods=['GET', 'POST'])
def add_inventory():
    if request.method == 'POST':
        ingredient = request.form['ingredient']
        quantity = request.form['quantity']
        new_inventory_item = Inventory(ingredient=ingredient, quantity=quantity)
        db.session.add(new_inventory_item)
        db.session.commit()
        return redirect('/inventory/')
    return render_template('add_inventory.html')

@app.route('/inventory/')
def view_inventory():
    inventory = Inventory.query.all()
    return render_template('view_inventory.html', inventory=inventory)

@app.route('/suggestions/add/', methods=['GET', 'POST'])
def add_suggestion():
    flavors = Flavor.query.all()
    if request.method == 'POST':
        flavor_id = request.form.get('flavor')
        allergies = request.form['allergies']
        if flavor_id == 'new_flavor':
            flavor_name = request.form.get('new_flavor_name')
            if flavor_name:
                new_flavor = Flavor(name=flavor_name, seasonal='No season')
                db.session.add(new_flavor)
                db.session.commit()
                suggestion = Suggestion(flavor=new_flavor, allergies=allergies)
                db.session.add(suggestion)
                db.session.commit()
            else:
                return render_template('add_suggestion.html', flavors=flavors, error='New flavor name is required.')
        elif flavor_id:
            flavor = Flavor.query.get(flavor_id)
            suggestion = Suggestion(flavor=flavor, allergies=allergies)
            db.session.add(suggestion)
            db.session.commit()
        else:
            return render_template('add_suggestion.html', flavors=flavors, error='Flavor is required.')
        return redirect('/suggestions/')
    return render_template('add_suggestion.html', flavors=flavors)

@app.route('/suggestions/')
def view_suggestions():
    suggestions = Suggestion.query.all()
    return render_template('view_suggestions.html', suggestions=suggestions)

if __name__ == '__main__':
    app.run(debug=True)
