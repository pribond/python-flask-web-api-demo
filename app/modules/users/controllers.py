#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES ------- 
import datetime
import json
import sendgrid
from flask import request, render_template, flash, current_app, redirect, abort, jsonify, url_for,g
from forms import *
from time import time
from flask_login import login_required, login_user, logout_user, current_user

# ------- IMPORT LOCAL DEPENDENCIES  -------
from app import app, logger
from . import users_page
from models import User

from app.helpers import *
from app.modules.localization.controllers import get_locale, get_timezone

from app.modules.sections.models import Section, UserSection
from app.modules.addresses.models import Address, UserAddress
from app.modules.events.models import Event, UserEvent

# -------  ROUTINGS AND METHODS  ------- 

# All users
@users_page.route('/')
@users_page.route('/<int:page>')
def index(page=1):
    try:
        m_users = User()
        list_users = m_users.all_data(page, app.config['LISTINGS_PER_PAGE'])
        # html or Json response
        if request_wants_json():
            return jsonify([{'id' : d.id, 'email' : d.email, 'username' : d.username} for d in list_users.items])
        else:
            return render_template("users/index.html", list_users=list_users, app = app)

    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        #abort(404)




# Show user
@users_page.route('/<int:id>/show')
def show(id=1):
    try:
        m_users = User()
        m_user = m_users.read_data(id)
        # html or Json response
        if request_wants_json():
            return jsonify({'id' : m_user.id, 
							'email' : m_user.email, 
							'username' : m_user.username})
        else:
            return render_template("users/show.html", user=m_user, app = app)

    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)


# New user
@users_page.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    try :
        form = Form_Record_Add(request.form)
        #  form = request.form

        sections = Section.query.filter(Section.is_active == True).all()

        in_addresses = Address.query.filter(Address.is_active == True).all()
        in_events = Event.query.filter(Event.is_active == True).all()

        if request.method == 'POST':
            if form.validate():
                users = User()

                sanitize_form = {
                    'email' : form.email.data,
                    'username' : form.username.data,

                    'in_addresses' : form.in_addresses.data,
                    'in_events' : form.in_events.data,
                    'sections' : form.sections.data,
                    'is_active' : form.is_active.data
                }

                users.create_data(sanitize_form)
                logger.info("Adding a new record.")
                if request_wants_json():
                    return jsonify(data = { message :"Record added successfully.", form: form }), 200, {'Content-Type': 'application/json'}
                else :
                    flash("Record added successfully.", category="success")
                    return redirect("/users")

        form.action = url_for('users_page.new')


        # html or Json response
        if request_wants_json():
            return jsonify(data = form), 200, {'Content-Type': 'application/json'}
        else:
            return render_template("users/edit.html", form=form, in_addresses = in_addresses, in_events = in_events, sections = sections, title_en_US='New', app = app)
    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)

# Edit user
@users_page.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id=1):
    try : 

        # check_admin()

        sections = Section.query.filter(Section.is_active == True).all()

        in_addresses = Address.query.filter(Address.is_active == True).all()
        in_events = Event.query.filter(Event.is_active == True).all()

        user = User.query.get_or_404(id)
        
        form = Form_Record_Add(request.form)
        #  form = request.form

        if request.method == 'POST':
            if form.validate():

                

                sanitize_form = {
                    'email' : form.email.data,
                    'username' : form.username.data,

                    'in_addresses' : form.in_addresses.data,
                    'in_events' : form.in_events.data,

                    'sections' : form.sections.data,
                    'is_active' : form.is_active.data
                }

                user.update_data(user.id, sanitize_form)
                logger.info("Editing a new record.")
                
                if request_wants_json():
                    return jsonify(data = { message :"Record updated successfully.", form: form }), 200, {'Content-Type': 'application/json'}
                else : 
                    flash("Record updated successfully.", category="success")
                    return redirect("/users")

        
        form.action = url_for('users_page.edit', id = user.id)
        form.email.data = user.email
        form.username.data = user.username

        if  user.sections :
            form.sections.data = user.sections

        if  user.in_addresses :
            form.in_addresses.data = user.in_addresses

        if  user.in_events :
            form.in_events.data = user.in_events

        form.is_active.data = user.is_active


        # html or Json response
        if request_wants_json():
            return jsonify(data = form), 200, {'Content-Type': 'application/json'}
        else:
            return render_template("users/edit.html", form=form,  in_addresses = in_addresses, in_events = in_events, sections = sections, title_en_US='Edit', app = app)
    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)



# Delete user
@users_page.route('/<int:id>/destroy')
@login_required
def destroy(id=1):
    try:
        users = User()
        user = users.query.get_or_404(id)
        users.destroy_data(user.id)
        # html or Json response
        if request_wants_json():
            return jsonify(data = {message:"Record deleted successfully.", user : m_user})
        else:
            flash("Record deleted successfully.", category="success")
            return redirect(url_for('users_page.index'))

    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)





