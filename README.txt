To start project.
docker-compose up --build - for start project.
docker-compose down - for stop

Endpoints
http://127.0.0.1:8000/ - web starts on

http://127.0.0.1:8000/loan/ - create new loan with payments
loan_amount = цифра від 0,01 до 99999999,99
loan_start_date = дата в форматі 2023-07-10
periodicity_amount = цифра від 1 до 365
periodicity = цифра від 1 до 3 де 1 - день, 2 - тиждень, 3 - місяць
number_of_payments = цифра від 1 до 365
interest_rate = % від 0,01 до 99

http://127.0.0.1:8000/loan/<uuid4:contract>/ - view current loan with it payments

http://127.0.0.1:8000/loan/payment/<int:id>/ - update payment principal and recreate current and subsequent payments
subtract_sum = цифра від 0,01 до 99999999,99


Explanation of the test task and changes that have been made:
To complete the task, "redis" was not needed

Loans model
To be able to create multiple loans with it own payments, I added the "contract" field to the model
To be able to save loan history, I added the "is_active" field to the model
Also divided field "periodicity" into two fields "periodicity_amount" and "periodicity". Now we can specify any period
of time between payments.

Payments model
I also decided to save the history of changes for payments.
Add field "is_active"
Payments that need to be changed are disabling by "is_active=False". To replace them, new ones are created with the correct data
