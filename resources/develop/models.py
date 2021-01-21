from django.db import models


class AssociatedAwards(models.Model):
    ucas_code1 = models.ForeignKey('Programmes', models.DO_NOTHING, db_column='ucas_code1', blank=True, null=True, related_name='ucas_code1')
    ucas_code2 = models.ForeignKey('Programmes', models.DO_NOTHING, db_column='ucas_code2', blank=True, null=True, related_name='ucas_code2')

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


class Leaders(models.Model):
    mod_code = models.TextField(blank=True, null=True)
    initials = models.TextField(blank=True, null=True)
    leader = models.BooleanField(blank=True, null=True)
    term = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'leaders'


class ModuleVariants(models.Model):
    major_code = models.ForeignKey('Modules', models.DO_NOTHING, db_column='major_code', blank=True, null=True, related_name='major_code')
    minor_code = models.ForeignKey('Modules', models.DO_NOTHING, db_column='minor_code', blank=True, null=True, related_name='minor_code')

    class Meta:
        managed = False
        db_table = 'module_variants'


class Modules(models.Model):
    mod_code = models.TextField(blank=True, null=False, primary_key=True)
    hecos_code = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    department = models.TextField(blank=True, null=True)
    contact_hours = models.IntegerField(blank=True, null=True)
    exams = models.IntegerField(blank=True, null=True)
    practical = models.IntegerField(blank=True, null=True)
    coursework = models.IntegerField(blank=True, null=True)
    credits = models.IntegerField(blank=True, null=True)
    prerequisites = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    outcomes = models.TextField(blank=True, null=True)
    methods = models.TextField(blank=True, null=True)
    bibliography = models.TextField(blank=True, null=True)
    formative = models.TextField(blank=True, null=True)
    summative = models.TextField(blank=True, null=True)
    exam_format = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    project = models.BooleanField(blank=True, null=True)
    lab_hours = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'modules'

    def __str__(self):
        return self.mod_code


class OptionRules(models.Model):
    rule_id = models.IntegerField(blank=True, null=True)
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
    id = models.TextField(blank=True, null=False, primary_key=True)
    name = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'people'


class Programmes(models.Model):
    ucas_code = models.TextField(blank=True, null=True)
    prog_code = models.TextField(blank=True, null=True)
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


class AssessmentComponents(models.Model):
    mod_code = models.ForeignKey(Modules, models.DO_NOTHING, db_column='mod_code', blank=True, null=True)
    set_order = models.IntegerField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    pcnt = models.TextField(blank=True, null=True)
    len = models.TextField(blank=True, null=True)
    must_pass = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'assessment_components'


class Strands(models.Model):
    mod_code = models.ForeignKey(Modules, models.DO_NOTHING, db_column='mod_code', blank=True, null=True)
    strand = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'strands'


class ValidationYear(models.Model):
    mod_code = models.TextField(blank=True, null=True)
    year = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'validation_year'
