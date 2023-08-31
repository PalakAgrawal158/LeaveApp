from apscheduler.schedulers.background import BackgroundScheduler
# from leave.views import schedular2
from .models import Leaves
from django.http import JsonResponse
from Email.email_sender import SendEmail

scheduler = BackgroundScheduler()


def cron_jobs(leave_id):
    try:
        leave = Leaves.objects.get(pk=leave_id)
        # scheduler.add_job(display, 'cron', second="2")
        scheduler.add_job(schedular1, 'cron', second="20" , args=[leave])
        scheduler.add_job(schedular2, 'cron', second="55", args=[leave])
        scheduler.start()
    except Leaves.DoesNotExist:
        return JsonResponse({"error" : "Leave does not exist"}, status=404)
    except Exception as error:
        print("error: ",error)
        return JsonResponse({"error": str(error)},status=500)


def cron_jobs_delete(leave_id):
    try:
        leave = Leaves.objects.get(pk=leave_id)
        scheduler.add_job(schedular3, 'cron', second="20" , args=[leave])
        scheduler.add_job(schedular4, 'cron', second="55", args=[leave])
        scheduler.start()

    except Leaves.DoesNotExist:
        return JsonResponse({"error" : "Leave does not exist"}, status=404)   
    except Exception as error:
        print("error: ",error)
        return JsonResponse({"error": str(error)},status=500)


# To change status 1 to 2
def schedular1(leave):
    try:
        leave.leave_status = 2
        leave.save()
        SendEmail(str(leave.employee), leave.leave_status_text)
        print("from s1",leave.leave_status)   
    except Exception as error:
        return JsonResponse({"error" : str(error)}, status=500)

# To change status 2 to 4 
def schedular2(leave):
    try:
        leave.leave_status = 4
        leave.save()
        SendEmail(str(leave.employee), leave.leave_status_text)
        print("from s2",leave.leave_status)
        scheduler.shutdown(wait=False)
    except Exception as error:
        return JsonResponse({"error" : str(error)}, status=500)
    

# To change status 5 to 6 
def schedular3(leave):
    try:
        leave.leave_status = 6
        leave.save()
        SendEmail(str(leave.employee), leave.leave_status_text)
        print("from s3",leave.leave_status)
    except Exception as error:
        return JsonResponse({"error" : str(error)}, status=500)


# To change status 6 to 7 
def schedular4(leave):
    try:
        leave.leave_status = 7
        leave.save()
        SendEmail(str(leave.employee), leave.leave_status_text)
        print("from s4",leave.leave_status)
        leave.delete()
        scheduler.shutdown(wait=False)
    except Exception as error:
        return JsonResponse({"error" : str(error)}, status=500)


