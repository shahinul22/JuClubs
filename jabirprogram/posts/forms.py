
from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    content = forms.CharField(
        required=False,  # This line prevents <textarea required>
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': "What's on your mind?",
        })
    )

    class Meta:
        model = Post
        fields = ['content', 'location']
        widgets = {
            'location': forms.TextInput(attrs={
                'placeholder': 'Search or use current location'
            }),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
