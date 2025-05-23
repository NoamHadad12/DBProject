# DBProject
DBProject - מערכת לניהול תוכניות אימון
1. עמוד שער
שם הפרויקט: מערכת לניהול תוכניות אימון
מפתחים: נועם חדד ועומר סטימקר
יחידה: עיצוב וניהול מסדי נתונים

מבוא
סקירת המערכת
מערכת ניהול תוכניות האימון נועדה למעקב וניהול של תוכניות אימונים, תרגילים, תוכניות תזונה והתקדמות משתמשים. המערכת מאחסנת מידע מובנה על תוכניות אימונים, תרגילים, מעקב אחר התקדמות המשתמשים ומשוב לשיפור התוכניות.

פונקציונליות עיקריות
יצירה וניהול של תוכניות אימון
שיוך אימונים ותרגילים לתוכניות
מעקב אחר התקדמות המשתמשים (משקל, אחוזי שומן וכו')
יצירה של תוכניות תזונה מותאמות אישית
קבלת משוב מהמשתמשים לשיפור התוכניות
שמירת נתונים היסטוריים על ביצוע אימונים

דיאגרמות ERD ו-DSD
דיאגרמת ישויות-קשרים (ERD)
![image (2)](https://github.com/user-attachments/assets/7ff037f2-947d-4840-8ff7-2902e2f0e55e)

סכמת מסד הנתונים (DSD)
![image (3)](https://github.com/user-attachments/assets/3b1e487c-00e7-4151-844b-8f9d1dcb19e7)

החלטות תכנון מסד הנתונים
נרמול: כל הטבלאות נורמלו לפחות עד 3NF כדי למנוע כפילויות ולשמור על עקביות הנתונים.
שדות תאריך: לכל ישות יש לפחות שני שדות DATE משמעותיים.
מפתחות ראשיים וזרים: נעשה שימוש בטיפוס serial למפתחות ראשיים ובמפתחות זרים לשמירה על תקינות הנתונים.


שיטות הזנת נתונים
שיטות שהשתמשנו בהן:
הזנת נתונים ידנית: ביצוע פקודות INSERT בקובץ insertTables.sql.
![image](https://github.com/user-attachments/assets/491b8667-381d-4360-a0e2-f8cb805249de)

הפקת נתונים מדומים: שימוש ב-[Mockaroo) ליצירת נתוני בדיקה ריאליסטיים.
![image](https://github.com/user-attachments/assets/245d7da0-e3ff-414d-af64-3f5332720f9c)

סקריפט Python: כתיבת סקריפט לאוטומציה של הזנת נתונים.
![image](https://github.com/user-attachments/assets/7c3da355-0374-476e-a6fe-3a78cb8a9d61)

גיבוי ושחזור
ביצוע גיבוי: נוצר גיבוי מלא של מסד הנתונים 
![image](https://github.com/user-attachments/assets/648f209d-62cb-4fed-9348-41addf9aec26)

בדיקת שחזור: הגיבוי שוחזר בהצלחה על המחשב.
![image](https://github.com/user-attachments/assets/eec6ef44-a439-4762-a29d-dc41a2a1a047)
