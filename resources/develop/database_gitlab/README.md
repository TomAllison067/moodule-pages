# Course DB

An attempt at a database of programmes and modules, covering the
programme specs and the coursework grid.  The tables are described below.

It is SQLite 3. You can build the db with

    $ cat course.sql | sqlite3 course.db

Then use your favourite db browser. E.g.

    $ sqlitebrowser course.db
    $ sqlite3 course.db

## Years

There is a different version of the database for each year. This means
you get a snapshot of the regs etc for each year in different files.
This avoids having a tag in each row for each year and means that a
simple cp command can create a new year. However it does mean that
format may become inconsistent over time.

The current year is always course.sql. Older years are e.g.
course1819.sql.

## Tables

The programme tables are

* `programmes`: describes meta data for each programme
* `associated_awards`: pairs up programmes that are associated (i.e.
  appear in each other's "associated awards" section in the spec
* `option_rules`: specifies rules for module requirements for all years.
  Will eventually replace `core/non_condonable/non_options` i suppose.

The module tables are

* `modules`: describes meta data for each module
* `leaders`: leaders of each module for each academic year and term
* `people`: map from initials to full name and email address
* `coursework`: assignments associated to each module 
* `strands`: associate strands to each module
* `module_variants`: pair up variants of modules
* `assessment_components`: the components of the modules that are
  assessed and input on Banner
* `validation_year`: the year the module was first validated, if known
* `teaching_activities`: how a module is taught
* `formative_assessments`: the formative assessments of a module

The tables are described below.  All fields are text unless stated otherwise.

## Programme Tables

### Programmes

Contains an overview of each programme.

* `ucas_code`: the UCAS code for the programme
* `prog_code`: the programme code (different from UCAS somehow)
* `hecos_code`: because there aren't enough codes already
* `title`
* `level`: BSc or MSci
* `yini`: bool, true if is YINI
* `accreditation`: text describing how the programme is accredited
* `duration`: integer programme length in years
* `start_stage`: integer the first stage of the programme (usually 1, sometimes 0)
* `involved_depts`: text description of other departments responsible for
  the programme
* `options_text`: text describing particulars and restrictions on the
  electives of the programme
* `progression_text`: text describing particular progression
  requirements
* `aims`: text describing the aims of the programme
* `outcomes`: text describing the desired outcomes of the programme
* `costs`: text describing costs associated to the programme (usually
  "no cost over £50" except year in industry which adds "there may be
  costs associated with your YINI".
* `fheq_level`: the FHEQ levels (usually 4-6 or 4-7 depending on BSC or
  Masters).
* `status`: text field for anything useful e.g. DISCONTINUED. (will
  likely have a convention)
* `specialisation`: boolean, true if this is a specialisation of another
  degree.

### Option\_Rules

A table that lists which modules must be taken by students on each
degree by year of entry. The fields are

* `ucas_code`: the `ucas_code` from `programmes`
* `entry_year`: the year the student joined RHUL
* `stage`: the current stage (year) of the student
* `constraint_type`: one of CORE, OPTS, STRAND, DISC\_ALT, DISALLOWED,
  CREDITS, MAX\_STRAND (see below)
* `min_quantity`: how many modules / credits must match this rule
* `max_quantity`: how many modules / credits can at most match this rule
* `mod_code_pattern`: comma separated list of module codes or prefixes
  or strand name
* `condonable`: 1 if condonable, 0 if not
* `allow_project`: 1 if projects are allowed to satisfy

The types of rules are:

* CORE: the module is core and must be taken
* OPTS: pattern is a comma separated list of mod\_codes or prefixes of
  mod\_codes that are allowed. Quantity is how many modules must match
  this.
* STRAND: as above, but the pattern is strand,mod\_code\_pattern. That
  is choose a subset of modules matching the mod\_code\_pattern that are
  on the given strand.
* DISC\_ALT: discretionary alternative. A comma separated list of module
  codes. The first is the standard choices, others may be allowed at the
  discretion of the department.
* DISALLOWED: students cannot take this module
* CREDITS: the total number of credits that can match the pattern across
  all choices
* MAX\_STRAND: at most this many modules can be from the strand
  identified in the pattern field.

To check a selection against the rules, i would order the rules by
generality:

* CORE and DISC\_ALT matched first
* STRAND takes some more
* Leftovers are matched against OPTS rules, with most general pattern
  matched last
* Other rules checked globally

Example:

    ('G400','2017',3,'CORE,1,1,'CS3000',0,0)
    ('G400','2017',3,'OPTS',2,2,'CS3,IY3',1,0)
    ('G400','2017',3,'STRAND',1,1,'AS',1,0)

means a student on G400 who entered in 2017 and is a third year student:

* must take CS3000 which cannot be condoned,
* has to take two options from CS3xxx and IY3xxx (non-project),
* has to take three more options from the AS strand (non-project).

## Module Tables

### Modules

Contains an overview of each module.  Implicitly, the "level" of each
module is 4+`year`.  Similarly self study hours are 10\*`credits` -
`contact_hours`.

* `mod_code`: CSxxxx or IYxxxx
* `jacs_code`: the (old) JACS code of the module (hecos has replaced)
* `hecos_code`: because there aren't enough codes already
* `title`
* `short_title`
* `level`: integer -- level 4 is first year, level 6 is 3rd, etc
* `department`: the department who owns the module
* `credits`: integer, number of credits the module is worth
* `corequisites`: comma separated list of co-req module codes
* `prerequisites`: comma separated list of pre-req module codes
* `banned_combinations`: comma separated list of disallowed module code
  combos
* `learning_outcomes`: "\n" separated list of learning outcomes
* `summary`: text summary of module
* `notional_learning_hours`: int, the total learning hours of the module
* `books_to_purchase`: books the student should buy
* `core_reading`: books the module recommends as core
* `exam_format`: a text description of exam format
* `status`: text field for anything useful e.g. DISCONTINUED. ACTIVE for
  running modules.
* `project`: boolean, whether the module is a final year project
* `lab_hours`: int, number of lab hours per week per student
* `deg_progs`: which programmes this is a module for (mostly CS even
  for IY modules, only Maths for MT.... modules, DC for digital media)

### Teaching\_Activities

The list of ways in which a module is taught

* `mod_code`: the module code the method applies to
* `activity_name`: activity name: one of "Lectures", "Tutorials",
  "Laboratory Classes", "Practical Classes and Workshops", etc. (from
  module spec forms)
* `kis_category`: type of activity letter code
* `length_mins`: text (free form on spec)
* `num_weeks`: text
* `times_per_week`: text
* `total_hours`: integer

### Formative\_Assessments

The formative activities/feedback of the module

* `mod_code`: text,
* `set_order`: integer, ordering of list of activities
* `activity`: text, description of activity
* `length`: text
* `units_of_length`: text
* `must_pass`: text
* `marked_out_of`: text, usually 100
* `mode_of_feedback`: text

### Assessment\_Components

The summative assessment components of the module

* `mod_code`: text,
* `set_order`: integer, ordering of list of activities, 99 for exams
* `name`: text, name of the component -- usually CW1, CW2, EX the office
  has a fixed list of allowed names, used to associate courseworks
  (sub-components) with the component they contribute to
* `description`: text, more descriptive name (e.g. Written Assignments)
* `weight`: int, percentage contribution to module
* `length`: text
* `units_of_length`: text
* `must_pass`: text
* `marked_out_of`: text, usually 100
* `kis_category`, text: letter code of KIS category
* `final_assessment`: text, indication of whether this is final
  assessment

### Leaders

Who led a module and when.  There may be multiple leaders per academic
year.

* `mod_code`: the module being led
* `initials`: the initials of the leader
* `leader`: boolean, true if they are the main leader
* `term` : term the staff are teaching (leaders teach for whole duration
  of module)

### People

Who we are

* `id`: their initials
* `name`: full name
* `email`: their email address

### Coursework

The coursework for each module (a-la coursework grid).  Each record
contains the academic year, as it may change from year to year.

For coursework, only the "major" module is provided for.  Variants (e.g.
CS1830 (major) vs CS1831 (minor)) are not explicitly given entries
unless they differ from the major module.

* `mod_code`: the module the assignment is for
* `title`: the name of the assignment
* `term`: integer, which term it is set (1 or 2)
* `percent`: how much percent of the final grade, or `"MFA"` for
  mandatory formative assessment.
* `deadline`: text, when the assignment is due -- mainly in date format
  (ISO) but some have textual descriptions
* `feedback_deadline`: text, when the feedback is due -- mainly in date
  format (ISO) but some have textual descriptions
* `comment`: some description of the coursework (e.g. programming
  exercise)
* `anonymous`: bool, if the assignment is marked anonymously, NULL if
  unknown
* `mark_type`: N or G (numerical or grade), NULL if unknown
* `college_extension_permitted`: bool, if the assignment is under the college
  extensions policy, NULL if unknown
* `substantial`: bool, if the assignment is "substantial" according to
  college, NULL if unknown
* `set_order`: integer, relative ordering of assignments (1 is first, 2
  second...)
* `component`: name of component, refs name in assessment\_components
* `submission_time`: the time the coursework should be submitted

### Strands

Identify which modules belong to which strands.

* `mod_code`: the code from `modules`
* `strand`: text describing a strand it is in (e.g. AI or SE).
Note, modules can be in multiple strands by having multiple records.

### Module\_Variants

Associate modules that are variants of each other.  The LHS is always
the main variant, with the RHS the offshoot.  E.g. CS1830 Games and
CS1831 Games (for Digital Media).

* `major_code`: the `mod_code` from `modules` of the major module
* `minor_code`: the `mod_code` from `modules` of the minor module.

### Validation\_Year

If known, the year the module was first validated. Can be useful for
finding out if an exam should exist for a given year. To be more
precise, this is the first academic year the module could have run (the
documentation would have gone in the year before).

* `mod_code`: the `mod_code` from `modules`
* `year`: the year 2018/19 for example.
