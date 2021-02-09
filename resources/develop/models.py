# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AssessmentComponents(models.Model):
    mod_code = models.TextField(blank=True, null=True)
    set_order = models.IntegerField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    length = models.TextField(blank=True, null=True)
    units_of_length = models.TextField(blank=True, null=True)
    must_pass = models.TextField(blank=True, null=True)
    marked_out_of = models.TextField(blank=True, null=True)
    kis_category = models.TextField(blank=True, null=True)
    final_assessment = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'assessment_components'


class AssociatedAwards(models.Model):
    ucas_code1 = models.ForeignKey('Programmes', models.DO_NOTHING, db_column='ucas_code1', blank=True, null=True)
    ucas_code2 = models.ForeignKey('Programmes', models.DO_NOTHING, db_column='ucas_code2', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'associated_awards'


class Coursework(models.Model):
    mod_code = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    term = models.TextField(blank=True, null=True)
    percent = models.TextField(blank=True, null=True)
    deadline = models.TextField(blank=True, null=True)
    feedback_deadline = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    anonymous = models.BooleanField(blank=True, null=True)
    mark_type = models.TextField(blank=True, null=True)
    college_extension_permitted = models.BooleanField(blank=True, null=True)
    substantial = models.BooleanField(blank=True, null=True)
    set_order = models.IntegerField(blank=True, null=True)
    component = models.TextField(blank=True, null=True)
    submission_time = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'coursework'


class FormativeAssessments(models.Model):
    mod_code = models.TextField(blank=True, null=True)
    set_order = models.IntegerField(blank=True, null=True)
    activity = models.TextField(blank=True, null=True)
    length = models.TextField(blank=True, null=True)
    units_of_length = models.TextField(blank=True, null=True)
    must_pass = models.TextField(blank=True, null=True)
    marked_out_of = models.TextField(blank=True, null=True)
    mode_of_feedback = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'formative_assessments'


class Leaders(models.Model):
    mod_code = models.TextField(blank=True, null=True)
    initials = models.TextField(blank=True, null=True)
    leader = models.BooleanField(blank=True, null=True)
    term = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'leaders'


class ModuleOptionKeys(models.Model):
    mod_code = models.ForeignKey('Modules', models.DO_NOTHING, db_column='mod_code', blank=True, null=True)
    option_key = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'module_option_keys'


class ModuleVariants(models.Model):
    major_code = models.ForeignKey('Modules', models.DO_NOTHING, db_column='major_code', blank=True, null=True)
    minor_code = models.ForeignKey('Modules', models.DO_NOTHING, db_column='minor_code', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'module_variants'


class Modules(models.Model):
    mod_code = models.TextField(unique=True, blank=True, null=True)
    jacs_code = models.TextField(blank=True, null=True)
    hecos_code = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    short_title = models.TextField(blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    department = models.TextField(blank=True, null=True)
    with_effect_from = models.TextField(blank=True, null=True)
    availability_terms = models.TextField(blank=True, null=True)
    credits = models.IntegerField(blank=True, null=True)
    corequisites = models.TextField(blank=True, null=True)
    prerequisites = models.TextField(blank=True, null=True)
    banned_combinations = models.TextField(blank=True, null=True)
    learning_outcomes = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    notional_learning_hours = models.TextField(blank=True, null=True)
    books_to_purchase = models.TextField(blank=True, null=True)
    core_reading = models.TextField(blank=True, null=True)
    exam_format = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    project = models.BooleanField(blank=True, null=True)
    lab_hours = models.IntegerField(blank=True, null=True)
    deg_prog = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'modules'


class OptionRules(models.Model):
    rule_id = models.AutoField(blank=True, null=True)
    prog_code = models.ForeignKey('Programmes', models.DO_NOTHING, db_column='prog_code', blank=True, null=True)
    entry_year = models.TextField(blank=True, null=True)
    stage = models.IntegerField(blank=True, null=True)
    constraint_type = models.TextField(blank=True, null=True)
    min_quantity = models.IntegerField(blank=True, null=True)
    max_quantity = models.IntegerField(blank=True, null=True)
    mod_code_pattern = models.TextField(blank=True, null=True)
    condonable = models.IntegerField(blank=True, null=True)
    allow_project = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'option_rules'


class People(models.Model):
    id = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'people'


class ProgrammeOptionKeys(models.Model):
    prog_code = models.ForeignKey('Programmes', models.DO_NOTHING, db_column='prog_code', blank=True, null=True)
    option_key = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'programme_option_keys'


class Programmes(models.Model):
    ucas_code = models.TextField(unique=True, blank=True, null=True)
    prog_code = models.TextField(unique=True, blank=True, null=True)
    hecos_code = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    level = models.TextField(blank=True, null=True)
    yini = models.BooleanField(blank=True, null=True)
    accreditation = models.TextField(blank=True, null=True)
    involved_depts = models.TextField(blank=True, null=True)
    options_text = models.TextField(blank=True, null=True)
    progression_text = models.TextField(blank=True, null=True)
    aims = models.TextField(blank=True, null=True)
    outcomes = models.TextField(blank=True, null=True)
    costs = models.TextField(blank=True, null=True)
    fheq_level = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    start_stage = models.IntegerField(blank=True, null=True)
    specialisation = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'programmes'


class Strands(models.Model):
    mod_code = models.ForeignKey(Modules, models.DO_NOTHING, db_column='mod_code', blank=True, null=True)
    strand = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'strands'


class TeachingActivities(models.Model):
    mod_code = models.TextField(blank=True, null=True)
    activity_name = models.TextField(blank=True, null=True)
    kis_category = models.TextField(blank=True, null=True)
    length_mins = models.TextField(blank=True, null=True)
    num_weeks = models.TextField(blank=True, null=True)
    times_per_week = models.TextField(blank=True, null=True)
    total_hours = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'teaching_activities'


class ValidationYear(models.Model):
    mod_code = models.TextField(blank=True, null=True)
    year = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'validation_year'
