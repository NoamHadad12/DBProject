-- הכנסת נתונים לטבלת TrainingProgram
INSERT INTO TrainingProgram (program_id, program_name, created_program, updated_program, goal, duration_weeks) 
VALUES 
(1, 'Beginner Strength', '2024-01-01', '2024-03-01', 'Build muscle and strength', 12),
(2, 'Weight Loss Plan', '2024-02-01', '2024-03-10', 'Lose weight effectively', 8),
(3, 'Endurance Training', '2024-03-01', '2024-04-01', 'Improve cardiovascular endurance', 10);

-- הכנסת נתונים לטבלת Workout
INSERT INTO Workout (workout_id, workout_name, day_number, date_scheduled, last_completed) 
VALUES 
(1, 'Leg Day', 1, '2024-03-15', '2024-03-20'),
(2, 'Upper Body', 2, '2024-03-16', '2024-03-21'),
(3, 'Full Body', 3, '2024-03-17', '2024-03-22');

-- הכנסת נתונים לטבלת Exercise
INSERT INTO Exercise (exercise_id, exercise_name, sets, reps, rest_time_seconds) 
VALUES 
(1, 'Squats', 4, 10, 60),
(2, 'Bench Press', 3, 8, 90),
(3, 'Deadlift', 5, 6, 120);

-- הכנסת נתונים לטבלת NutritionPlan
INSERT INTO NutritionPlan (plan_id, calories_per_day, protein_grams, carbs_grams, fats_grams, start_date, end_date) 
VALUES 
(1, 2000, 150, 250, 50, '2024-03-01', '2024-03-30'),
(2, 2500, 180, 300, 60, '2024-04-01', '2024-04-30'),
(3, 1800, 120, 200, 40, '2024-05-01', '2024-05-30');

-- הכנסת נתונים לטבלת UserProgress (תלויה ב-NutritionPlan)
INSERT INTO UserProgress (progress_id, user_id, weight_kg, fat_percentage, log_date, plan_id) 
VALUES 
(1, 101, 75, 15, '2024-03-10', 1),
(2, 102, 82, 18, '2024-03-15', 2),
(3, 103, 68, 12, '2024-03-20', 3);

-- הכנסת נתונים לטבלת Feedback
INSERT INTO Feedback (feedback_id, user_id, rating, comment, submitted_at) 
VALUES 
(1, 101, 5, 'Great program!', '2024-03-21'),
(2, 102, 4, 'Helped me stay on track', '2024-03-22'),
(3, 103, 3, 'Needs more meal variety', '2024-03-23');
