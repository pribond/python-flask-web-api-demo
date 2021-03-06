#!/usr/bin/python
# -*- coding: utf-8 -*-

# import dependencies
from wtforms import Form, StringField, TextAreaField, BooleanField, validators
from wtforms.fields.html5 import DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField

from app.modules.sections.models import Section


class Form_Record_Add(Form):
    email = StringField('email', validators=[validators.DataRequired(),
                                             validators.Length(max=255, message='max 255 characters')])
    username = StringField('username', validators=[validators.DataRequired(),
                                             validators.Length(max=255, message='max 255 characters')])

    # MANY-TO-MANY
    sections = QuerySelectMultipleField('Select Sections',
                             query_factory=lambda : Section.query.filter(Section.is_active == True).all(),
                             get_label=lambda s: s.title_en_US,
                             allow_blank=True)
    # MANY-TO-MANY
    in_addresses = QuerySelectMultipleField('Select In_addresses',
                             query_factory=lambda : Address.query.filter(Address.is_active == True).all(),
                             get_label=lambda s: s.title_en_US,
                             allow_blank=True)

    # MANY-TO-MANY
    in_events = QuerySelectMultipleField('Select In_events',
                             query_factory=lambda : Event.query.filter(Event.is_active == True).all(),
                             get_label=lambda s: s.title_en_US,
                             allow_blank=True)

    is_active = BooleanField('is_active', default=True)
