import json

from django.db.models import Q
from django.http  import JsonResponse, Http404
from django.views import View

from .models import JobPosting
from users.models import UserJobApplication


def get_job_posting_or_404(posting_id: int):
    try:
        return JobPosting.objects.get(id=posting_id)
    except JobPosting.DoesNotExist as e:
        raise Http404("Job posting does not exist") from e

class JobPostingView(View):
    def get(self, request, posting_id):
        posting = get_job_posting_or_404(posting_id)
        data = {
            'posting_id'                : posting.id,
            'company_name'              : posting.company.name,
            'country_name'              : posting.country.name if posting.country else "정보 없음",
            'area_name'                 : posting.area.name if posting.area else "정보 없음",
            'position'                  : posting.position,
            'reward'                    : posting.reward,
            'tech'                      : posting.tech,
            'content'                   : posting.content,
            'posting_id_list_by_company': [item.id for item in posting.company.job_postings.all()],
        }
        return JsonResponse(data, status=200)

    def delete(self, request, posting_id):
        posting = get_job_posting_or_404(posting_id)
        posting.delete()
        return JsonResponse({'message': 'Posting deleted'}, status=200)

    def put(self, request, posting_id):
        data = json.loads(request.body)
        posting = get_job_posting_or_404(posting_id)

        for attr, value in data.items():
            if value:
                if hasattr(posting, attr):
                    setattr(posting, attr, value)
                else:
                    return JsonResponse({'message': 'Invalid input'}, status=400)
        posting.save()
        return JsonResponse({'message': 'Posting updated'}, status=200)


def create_job_posting(request):
    if request.method != 'POST':
        return JsonResponse({'message': 'Method not allowed'}, status=405)
    JobPosting.objects.create(**json.loads(request.body))
    return JsonResponse({'message': 'success'}, status=201)


def get_job_postings(request):
    if request.method != 'GET':
        return JsonResponse({'message': 'Method not allowed'}, status=405)

    q = Q()
    if (search := request.GET.get('search')):
        q &= Q(company__name__icontains=search) \
        | Q(position__icontains=search) \
        | Q(tech__icontains=search)
    
    postings = JobPosting.objects.filter(q)
    results = [{
        'posting_id'  : posting.id,
        'company_name': posting.company.name,
        'country_name': posting.country.name,
        'area_name'   : posting.area.name,
        'position'    : posting.position,
        'reward'      : posting.reward,
        'tech'        : posting.tech,
    } for posting in postings]

    return JsonResponse(results, status=200, safe=False)


def user_job_apply(request, posting_id):
    if request.method != 'POST':
        return JsonResponse({'message': 'Method not allowed'}, status=405)

    user_id = json.loads(request.body)['user_id']
    if UserJobApplication.objects.filter(user_id=user_id, job_posting_id=posting_id).exists():
        return JsonResponse({'message': 'You have already applied for this job'}, status=400)

    UserJobApplication.objects.create(
        user_id        = user_id,
        job_posting_id = posting_id
    )
    return JsonResponse({'message': 'success'}, status=201)
