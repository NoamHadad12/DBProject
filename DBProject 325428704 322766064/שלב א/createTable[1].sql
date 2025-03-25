CREATE TABLE TrainingProgram (
  program_id INT NOT NULL,
  program_name VARCHAR(50) NOT NULL,
  created_program DATE NOT NULL,
  updated_program DATE NOT NULL,
  goal VARCHAR(255) NOT NULL,
  duration_weeks INT NOT NULL,
  PRIMARY KEY (program_id)
);

CREATE TABLE Workout (
  workout_id INT NOT NULL,
  workout_name VARCHAR(50) NOT NULL,
  day_number INT NOT NULL,
  date_scheduled DATE NOT NULL,
  last_completed DATE NOT NULL,
  PRIMARY KEY (workout_id)
);

CREATE TABLE Exercise (
  exercise_id INT NOT NULL,
  exercise_name VARCHAR(50) NOT NULL,
  sets INT NOT NULL,
  reps INT NOT NULL,
  rest_time_seconds INT NOT NULL,
  PRIMARY KEY (exercise_id)
);

CREATE TABLE NutritionPlan (
  plan_id INT NOT NULL,
  calories_per_day INT NOT NULL,
  protein_grams INT NOT NULL,
  carbs_grams INT NOT NULL,
  fats_grams INT NOT NULL,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  PRIMARY KEY (plan_id)
);

CREATE TABLE UserProgress (
  progress_id INT NOT NULL,
  user_id INT NOT NULL,
  weight_kg INT NOT NULL,
  fat_percentage INT NOT NULL,
  log_date DATE NOT NULL,
  plan_id INT NOT NULL,
  PRIMARY KEY (progress_id),
  FOREIGN KEY (plan_id) REFERENCES NutritionPlan(plan_id)
);

CREATE TABLE Feedback (
  feedback_id INT NOT NULL,
  user_id INT NOT NULL,
  rating INT NOT NULL,
  comment VARCHAR(255) NOT NULL,
  submitted_at DATE NOT NULL,
  PRIMARY KEY (feedback_id)
);
