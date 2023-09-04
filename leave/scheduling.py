from apscheduler.schedulers.background import BackgroundScheduler
# from leave.views import schedular2
from .models import Leaves
from django.http import JsonResponse
from Email.email_sender import SendEmail
from datetime import datetime

def update_status_5min():
    approved_progress_leaves = Leaves.objects.filter(leave_status=1)
    delete_aproval_pending = Leaves.objects.filter(leave_status=5)
    # print("current 5 time",datetime.now())
    if approved_progress_leaves:
        for leave in approved_progress_leaves:
            leave.leave_status=2
            leave.save()
            SendEmail(str(leave.employee), leave)
    
    if delete_aproval_pending:
        for leave in delete_aproval_pending:
            leave.leave_status=6
            leave.save()
            SendEmail(str(leave.employee), leave)


def update_status_10min():
    # print("current 10 time",datetime.now())
    approved_updated_leaves = Leaves.objects.filter(leave_status=2)
    deleted_update_progress = Leaves.objects.filter(leave_status=6)
    if approved_updated_leaves:
        print("2to4")
        for leave in approved_updated_leaves:
            leave.leave_status=4
            leave.save()
            SendEmail(str(leave.employee), leave)

    if deleted_update_progress:
        print("6to7")
        for leave in deleted_update_progress:
            leave.leave_status=7
            leave.save()
            SendEmail(str(leave.employee), leave)
            leave.delete()

def test():
    print("Hello")
    

def update_scheduler():
    try:
        scheduler = BackgroundScheduler()
        scheduler.add_job(update_status_5min, 'cron', minute="*/1")
        scheduler.add_job(update_status_10min, 'cron', minute="*/2")
        # scheduler.add_job(test, 'cron', hour= 15,minute = 44,second=5)
        scheduler.start()
    except Exception as error:
        print("error: ",error)
        return JsonResponse({"error": str(error)},status=500)





# scheduler_obj1 = BackgroundScheduler()
# scheduler_obj2 = BackgroundScheduler()

# def cron_jobs(leave_id):
#     try:
#         leave = Leaves.objects.get(pk=leave_id)
#         # scheduler.add_job(display, 'cron', second="2")
#         scheduler_obj1.add_job(schedular1, 'cron', second="20" , args=[leave])
#         scheduler_obj1.add_job(schedular2, 'cron', second="55", args=[leave])
#         scheduler_obj1.start()
#     except Leaves.DoesNotExist:
#         return JsonResponse({"error" : "Leave does not exist"}, status=404)
#     except Exception as error:
#         print("error: ",error)
#         return JsonResponse({"error": str(error)},status=500)


# def cron_jobs_delete(leave_id):
#     try:
#         leave = Leaves.objects.get(pk=leave_id)
#         scheduler_obj2.add_job(schedular3, 'cron', second="20" , args=[leave])
#         scheduler_obj2.add_job(schedular4, 'cron', second="55", args=[leave])
#         scheduler_obj2.start()

#     except Leaves.DoesNotExist:
#         return JsonResponse({"error" : "Leave does not exist"}, status=404)   
#     except Exception as error:
#         print("error: ",error)
#         return JsonResponse({"error": str(error)},status=500)


# # To change status 1 to 2
# def schedular1(leave):
#     try:
#         leave.leave_status = 2
#         leave.save()
#         SendEmail(str(leave.employee), leave.leave_status_text)
#         print("from s1",leave.leave_status)   
#     except Exception as error:
#         return JsonResponse({"error" : str(error)}, status=500)

# # To change status 2 to 4 
# def schedular2(leave):
#     try:
#         leave.leave_status = 4
#         leave.save()
#         SendEmail(str(leave.employee), leave.leave_status_text)
#         print("from s2",leave.leave_status)
#         scheduler_obj1.shutdown(wait=False)
#     except Exception as error:
#         return JsonResponse({"error" : str(error)}, status=500)
    

# # To change status 5 to 6 
# def schedular3(leave):
#     try:
#         leave.leave_status = 6
#         leave.save()
#         SendEmail(str(leave.employee), leave.leave_status_text)
#         print("from s3",leave.leave_status)
#     except Exception as error:
#         return JsonResponse({"error" : str(error)}, status=500)


# # To change status 6 to 7 
# def schedular4(leave):
#     try:
#         leave.leave_status = 7
#         leave.save()
#         SendEmail(str(leave.employee), leave.leave_status_text)
#         print("from s4",leave.leave_status)
#         leave.delete()
#         scheduler_obj2.shutdown(wait=False)
#     except Exception as error:
#         return JsonResponse({"error" : str(error)}, status=500)
    





