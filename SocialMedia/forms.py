from django import forms


from .models import Post, Comment

class PostForm(forms.ModelForm):
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control-file mb-4', 'multiple': True}), required=False)

    class Meta:
        model = Post
        fields = ('title', 'text', 'video')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control mb-4', 'placeholder': 'Enter title here...'}),
            'text': forms.Textarea(attrs={'class': 'form-control mb-4', 'placeholder': 'Write your post here...'}),
            'video': forms.ClearableFileInput(attrs={'class': 'form-control-file mb-4'}),
        }

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['images'] = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control-file mb-4', 'multiple': True}), required=False)

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)