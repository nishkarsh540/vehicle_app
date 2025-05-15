from flask import Blueprint, render_template, request,redirect,url_for,abort,flash
from . import db
from .models import User,Category
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





def delete_category(category_id):
    category = Category.query.get(category_id)

    if not category.can_be_deleted():
        return "cannot delete category with existing products", 400
    db.session.delete(category)
    db.session.commit()

    return "category deleted successfully", 200