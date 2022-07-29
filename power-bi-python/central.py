from datetime import datetime
from numpy import product
# Importing the invoice fetching API function from invoices.py
from invoices import call_invoices
import asyncio
import time
import schedule
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import os

# Creating the main function
async def chain():
	def _handle_task_result(task: asyncio.Task) -> None:
		try:
				task.result()
		except asyncio.CancelledError:
				pass
		except Exception:
				logging.exception('Exception raised by task %r',task)
	start = time.perf_counter()
    # Creating task for the imported function from invoices.py
	invoice_task = asyncio.create_task(call_invoices())
    
    # Awaiting the task created
	await invoice_task
    # Keeping track of the task's times	
	end = time.perf_counter()-start
	l_time =  time.localtime()
	human_time = time.asctime(l_time)
	print (f"chained result took {end:0.2f} seconds")
	print(f"Current time is {human_time}")

if name == "main":
# Scheduler enables the code to loop forever and take sleep breaks between the loops.
    scheduler = AsyncIOScheduler()
scheduler.add_job(chain,'interval',seconds=1)
scheduler.start()
print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

try:
	asyncio.get_event_loop().run_forever()
except (KeyboardInterrupt,SystemExit):
    pass