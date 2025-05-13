plan = """To book a hotel on Mars, I need to gather some additional information from you. Here's my planned approach:

STEP 1:
Explanation: Since you have not mentioned which hotel you would like to book, I need to first gather the available hotel options on Mars.
Recommended Tool: functions.list_hotels
Suggested Input: { "location": "Mars" }

STEP 2:
Explanation: Once we have the list of available hotels, you can select your preferred hotel. I will need to ask you which hotel you would like to book.
Recommended Tool: functions.collect_information_from_the_user
Suggested Input: { "question": "Which hotel on Mars would you like to book?" }

STEP 3:
Explanation: After choosing a hotel, I'll need to know the check-in and check-out dates for your stay.
Recommended Tool (for check-in date): functions.collect_information_from_the_user
Suggested Input: { "question": "What is your check-in date? Please provide in format yyyy-mm-dd." }

Recommended Tool (for check-out date): functions.collect_information_from_the_user
Suggested Input: { "question": "What is your check-out date? Please provide in format yyyy-mm-dd." }

STEP 4:
Explanation: With the hotel's name and dates, I will proceed to book your hotel.
Recommended Tool: functions.book_hotel
Suggested Input: { "hotel_name": Output of Step 2, "check_in": Output of Step 3 for check-in date, "check_out": Output of Step 3 for check-out date }

Let's begin by listing the hotels available on Mars. I'll proceed to Step 1."""