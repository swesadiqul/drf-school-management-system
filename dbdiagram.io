Table auth.custom_users {
  id int [pk]
  email varchar [unique]
  is_staff boolean [default: true]
  is_active boolean [default: true]
  is_superuser boolean [default: false]
  date_joined datetime [default: `timezone.now()`]
}

Table auth.super_admins {
  id int [pk]
  business_id int
  user_id int [ref: > auth.custom_users.id] // Corrected the reference
  is_create_branch boolean [default: false]
  branch_limit int [default: 0]
  is_business_admin boolean [default: false]
  is_branch_admin boolean [default: false]
  date_joined datetime [default: `timezone.now()`]
}

Table business.businesses {
  id int [pk]
  name varchar
  slug varchar [unique]
  description text
  location varchar
  founded_year int
  industry varchar
  website varchar
  email varchar
  logo varchar
  social_media_facebook varchar
  social_media_twitter varchar
  social_media_linkedin varchar
  revenue decimal
  employee_count int
  address varchar
  parent_business_id int
  has_branch boolean [default: false]
  branch_num int [default: 0]
  ceo_name varchar
  created_at datetime [default: `now()`]
  updated_at datetime [default: `now()`]
}

Table school.sections {
  id int [pk]
  section_name varchar [unique]
}

Table school.subjects {
  id int [pk]
  subject_code varchar [unique]
  subject_name varchar [unique]
  subject_type varchar
}

Table school.classes {
  id int [pk]
  class_name varchar [unique]
}

Table school.student_admissions {
  admission_id int [pk]
  first_name varchar
  last_name varchar
  date_of_birth date
  gender varchar
  nationality varchar
  class_id int
  section_id int
  religion varchar
  address text
  city varchar
  state varchar
  country varchar
  email varchar
  contact_number varchar
  previous_school varchar
  admission_status varchar
  guardian_name varchar
  guardian_relationship varchar
  guardian_email varchar [unique]
  guardian_contact_number varchar
  admission_date datetime [default: `timezone.now()`]
}

Table school.students {
  id int [pk]
  user_id int [ref: > auth.custom_users.id]
  admission_history_id int [ref: > school.student_admissions.admission_id]
  current_class_id int
  current_section_id int
  is_disable boolean [default: false]
  date_joined datetime [default: `timezone.now()`]
}

Table school.student_categories {
  id int [pk]
  category_name varchar [unique]
}

Table school.disable_reasons {
  id int [pk]
  disable_name varchar [unique]
}

Table school.promote_students {
  promotion_id int [pk]
  student_id int
  from_class_id int
  to_class_id int
  from_section_id int
  to_section_id int
  promotion_date date [default: `timezone.now()`]
  remarks text
}

Table school.parents {
  id int [pk]
  user_id int [ref: > auth.custom_users.id]
  student_id int [ref: > school.students.id]
  date_joined datetime [default: `timezone.now()`]
}


Ref: auth.super_admins.business_id > business.businesses.id // many-to-one
Ref: business.businesses.parent_business_id > business.businesses.id // many-to-one
Ref: school.classes.id > school.students.current_class_id
Ref: school.sections.id > school.students.current_section_id

