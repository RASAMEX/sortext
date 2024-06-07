from django import forms

class LotteryForm(forms.Form):
    """
    LotteryForm

    This form represents a lottery form in Django.

    Fields:
        title (CharField): The title field for the lottery.
        participant_file (FileField): The file field for uploading participants.
    """

    title = forms.CharField(max_length=100, help_text='Enter the title of the lottery.')
    participant_file = forms.FileField(help_text='Upload a file containing participants.')

