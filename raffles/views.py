from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .forms import LotteryForm
from .lottery import LotteryDraw
from .models import Raffle, Participant
from .custom_logger import setup_logger

import pandas as pd

logger = setup_logger(__name__)

def main_page(request):
    """
    View for the main page displaying all raffles.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered main page with all raffles.
    """
    raffles = Raffle.objects.all()  # Get all raffles
    return render(request, 'index.html', {'raffles': raffles})

def raffle_details(request, raffle_id):
    """
    View for displaying the details of a specific raffle.

    Args:
        request (HttpRequest): The request object.
        raffle_id (int): The ID of the raffle to display.

    Returns:
        HttpResponse: The rendered raffle details page with participants.
    """
    raffle = get_object_or_404(Raffle, pk=raffle_id)
    participants = Participant.objects.filter(raffle=raffle)
    return render(request, 'raffle.html', {'raffle': raffle, 'participants': participants})

@login_required
def create_raffle(request):
    """
    View for creating a new raffle. Requires login.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered page for creating a raffle or a redirect to the main page after successful creation.
    """
    if request.method == 'POST':
        form = LotteryForm(request.POST, request.FILES)
        if form.is_valid():
            creator_user = request.user
            title = form.cleaned_data['title']
            file = request.FILES['participant_file']
            
            if file.name.endswith('.xlsx'):
                df = pd.read_excel(file)  # Read Excel file
                raffle = Raffle.objects.create(name=title, creator=creator_user)
                for index, row in df.iterrows():
                    participant_name = row['Name']
                    tickets = row['Tickets']
                    Participant.objects.create(
                        raffle=raffle, 
                        name=participant_name, 
                        valid_tickets=tickets
                    )
            logger.info("New raffle created")
            return redirect('main_page')  # Redirect to the main page after successful creation
    else:
        form = LotteryForm()
    return render(request, 'create_raffle.html', {'form': form})

def draw_raffle(request, id):
    """
    View for executing a raffle draw.

    Args:
        request (HttpRequest): The request object.
        id (int): The ID of the raffle.

    Returns:
        JsonResponse: The result of the draw including the participants and winner.
    """
    invested = request.GET.get('invested', 'false').lower() == 'true'
    two_three = request.GET.get('two_three', 'false').lower() == 'true'
    level = request.GET.get('level', 'soft')
    
    lotto = LotteryDraw(id)
    lotto.load_data()
    participants_list = lotto.sorter_list()
    
    if len(participants_list) <= 1:
        return JsonResponse({"legend": "No more participants left",
                             "list": participants_list,
                             "result": None}, safe=False)
    if level == 'soft':
        lotto_result = lotto.soft_draw_exec(invested=invested, two_three=two_three)
    elif level == 'half':
        lotto_result = lotto.half_draw_exec(invested=invested, two_three=two_three)
    elif level == 'hard':
        lotto_result = lotto.hard_draw_exec(invested=invested, two_three=two_three)
        
    return JsonResponse({
        "legend": f"Applied draw level: {level}, elimination type: {invested}, two out of three mode: {two_three}",
        "list": participants_list,
        "result": lotto_result
    }, safe=False)

def update_participants(request, raffle_id):
    """
    View for updating the participants of a specific raffle.

    Args:
        request (HttpRequest): The request object.
        raffle_id (int): The ID of the raffle.

    Returns:
        HttpResponse: The HTML table of participants.
    """
    raffle = get_object_or_404(Raffle, pk=raffle_id)
    participants = Participant.objects.filter(raffle=raffle)
    table_html = render_to_string('participants_table.html', {'participants': participants})
    return HttpResponse(table_html)
