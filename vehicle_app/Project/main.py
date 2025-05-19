from flask import Blueprint, render_template, request,redirect,url_for,abort,flash
from . import db
from .models import User,Category, Products
from flask_login import login_required,current_user

main = Blueprint('main',__name__)

@main.route('/admin/manage_cat',methods=['GET','POST'])
@login_required
def manage_cat():
    if request.method == 'POST':
        if 'create_category' in request.form:
            category_name = request.form.get('create_category')
            existing_category = Category.query.filter_by(name=category_name).first()

            if existing_category:
                flash('Category already exists',category='error')

            else:
                new_category = Category(name=category_name)
                db.session.add(new_category)
                db.session.commit()

                flash('Category created successfully')
        elif 'remove_category' in request.form:
            category_id = request.form.get('category_id')
            category = Category.query.get(category_id)
            if category:
                    db.session.delete(category)
                    db.session.commit()
            else:
                flash('Category already exists',category='error')
        elif 'edit_category' in request.form:
            category_id = request.form.get('category_id')
            new_category_name = request.form.get('new_category_name')

            category = Category.query.get(category_id)

            if category:
                category.name = new_category_name
                db.session.commit()

                flash('Category updated successfully')
            else:
                flash('Category not found',category= 'error')
        return redirect(url_for('main.manage_cat'))

    if not current_user.role == 0:
        abort(403)

    
    categories = Category.query.all()

    return render_template('manage_cat.html',categories = categories)




@main.route('/admin/manage_product',methods=['GET','POST'])
@login_required
def manage_product():
    if request.method=='POST':
        if 'add_product' in request.form:
            product_name = request.form.get('product_name')
            category_id = request.form.get('category_id')


            new_product = Products(name=product_name,category_id=category_id)

            db.session.add(new_product)
            db.session.commit()


    categories = Category.query.all()
    products = Products.query.all()

    return render_template('manage_prod.html',categories=categories,products=products)


import matplotlib.pyplot as plt
import matplotlib 
matplotlib.use('Agg')

@main.route('/user-chart')
def user_chart():
    users = User.query.all()

    role_counts={}

    for user in users:
        if user.role == 0:
            role='admin'
        else:
            role='user'
        role_counts[role] = role_counts.get(role,0) + 1

    roles = list(role_counts.keys())
    counts = list(role_counts.values())

    plt.figure(figsize=(10,6))  
    plt.bar(roles,counts,color='blue',alpha=0.7)
    plt.xlabel('Roles')
    plt.ylabel('Number of Users')
    plt.title('Number of users by role')
    plt.tight_layout()

    chart_path = 'Project/static/user_chart.png'
    plt.savefig(chart_path)
    plt.close()
    return render_template('user_chart.html',chart_path=chart_path)